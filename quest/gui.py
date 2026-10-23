"""Local web GUI for the Quest CLI.

stdlib-only (http.server), consistent with the CLI's own dependency-free
design (see quest/model.py). Wraps the same engine/registry/state functions
the CLI uses -- no separate logic, no access to solution/ directories.
"""
from __future__ import annotations

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from quest import achievements as ach
from quest import progression
from quest.engine import attempt_mission
from quest.model import SKILL_TRACKS, rank_for_xp, skill_level, xp_to_next_rank
from quest.registry import load_achievements_catalog, load_campaigns, load_missions_for_campaign
from quest.state import load_history, load_player, save_player

WEBUI_DIR = Path(__file__).resolve().parent / "webui"

STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}


def _load_world():
    campaigns = load_campaigns()
    missions_by_campaign = {c.id: load_missions_for_campaign(c) for c in campaigns}
    all_missions = {m.id: m for ms in missions_by_campaign.values() for m in ms}
    return campaigns, missions_by_campaign, all_missions


def _mission_summary(mission, player, unlocked: bool) -> dict:
    return {
        "id": mission.id,
        "title": mission.title,
        "difficulty": mission.difficulty,
        "estimated_minutes": mission.estimated_minutes,
        "xp_reward": mission.xp_reward,
        "done": mission.id in player.completed_missions,
        "unlocked": unlocked,
        "is_active": mission.id == player.current_mission,
    }


def build_state_payload() -> dict:
    lr = load_player()
    player = lr.player
    campaigns, missions_by_campaign, all_missions = _load_world()
    level, rank = rank_for_xp(player.total_xp)
    to_next, into_current = xp_to_next_rank(player.total_xp)

    campaign_payload = []
    for campaign in campaigns:
        unlocked = progression.campaign_is_unlocked(campaign, player, all_missions)
        missions = missions_by_campaign.get(campaign.id, [])
        done = sum(1 for m in missions if m.id in player.completed_missions)
        campaign_payload.append(
            {
                "id": campaign.id,
                "title": campaign.title,
                "summary": campaign.summary,
                "status": campaign.status,
                "unlocked": unlocked,
                "boss_fight": campaign.boss_fight,
                "topics": campaign.topics,
                "done": done,
                "total": len(missions),
                "missions": [
                    _mission_summary(m, player, unlocked and progression.mission_is_unlocked(m, player))
                    for m in missions
                ],
            }
        )

    history = load_history()
    skill_tree = [
        {
            "key": key,
            "label": label,
            "points": player.skill_points.get(key, 0),
            "level": skill_level(player.skill_points.get(key, 0)),
        }
        for key, label in SKILL_TRACKS.items()
    ]

    return {
        "player": {
            "name": player.name,
            "xp": player.total_xp,
            "level": level,
            "rank": rank,
            "xp_to_next": to_next,
            "xp_into_current": into_current,
            "completed_count": len(player.completed_missions),
            "achievements_count": len(player.achievements),
            "current_mission": player.current_mission,
            "weaknesses": player.weaknesses,
        },
        "campaigns": campaign_payload,
        "skill_tree": skill_tree,
        "history": list(reversed([vars(h) for h in history[-20:]])),
        "warning": lr.warning,
    }


def build_mission_payload(mission_id: str) -> dict | None:
    _, _, all_missions = _load_world()
    mission = all_missions.get(mission_id)
    if mission is None:
        return None
    player = load_player().player
    scenario_path = Path(mission.dir) / "scenario.md"
    scenario = scenario_path.read_text(encoding="utf-8") if scenario_path.exists() else ""
    used = player.hints_used.get(mission.id, 0)
    return {
        "id": mission.id,
        "title": mission.title,
        "difficulty": mission.difficulty,
        "estimated_minutes": mission.estimated_minutes,
        "xp_reward": mission.xp_reward,
        "scenario": scenario,
        "done": mission.id in player.completed_missions,
        "is_active": mission.id == player.current_mission,
        "hints_total": len(mission.hints),
        "hints_used": used,
        "hints_revealed": mission.hints[:used],
        "workspace_dir": str(Path(mission.dir) / "workspace"),
    }


def do_start(mission_id: str) -> dict:
    _, _, all_missions = _load_world()
    mission = all_missions.get(mission_id)
    if mission is None:
        return {"error": f"Mission '{mission_id}' nicht gefunden."}
    player = load_player().player
    player.current_mission = mission.id
    save_player(player)
    return build_mission_payload(mission_id)


def do_hint(mission_id: str) -> dict:
    _, _, all_missions = _load_world()
    mission = all_missions.get(mission_id)
    if mission is None:
        return {"error": f"Mission '{mission_id}' nicht gefunden."}
    player = load_player().player
    if mission.hints:
        used = player.hints_used.get(mission.id, 0)
        if used < len(mission.hints):
            player.hints_used[mission.id] = used + 1
            save_player(player)
    return build_mission_payload(mission_id)


def do_check(mission_id: str) -> dict:
    _, _, all_missions = _load_world()
    mission = all_missions.get(mission_id)
    if mission is None:
        return {"error": f"Mission '{mission_id}' nicht gefunden."}
    player = load_player().player
    outcome = attempt_mission(mission, player)
    res = outcome.result
    passed_full = res.passed and res.score >= mission.min_pass_ratio
    achievement = None
    if outcome.newly_unlocked_achievement:
        info = ach.describe(outcome.newly_unlocked_achievement)
        achievement = {"id": outcome.newly_unlocked_achievement, **info}
    return {
        "mission_id": mission.id,
        "passed": passed_full,
        "score": res.score,
        "detail": res.detail,
        "xp_awarded": outcome.xp_awarded,
        "already_completed": outcome.already_completed,
        "achievement": achievement,
    }


def build_achievements_payload() -> dict:
    player = load_player().player
    catalog = load_achievements_catalog()
    return {
        "achievements": [
            {
                "id": aid,
                "title": info.get("title", aid),
                "description": info.get("description", ""),
                "unlocked": aid in player.achievements,
            }
            for aid, info in catalog.items()
        ]
    }


def build_review_payload() -> dict:
    player = load_player().player
    skill_rows = []
    for key, label in SKILL_TRACKS.items():
        pts = player.skill_points.get(key, 0)
        lvl = skill_level(pts)
        bucket = "strong" if lvl >= 3 else "developing" if lvl >= 1 else "weak" if pts > 0 else "untouched"
        skill_rows.append({"key": key, "label": label, "points": pts, "level": lvl, "bucket": bucket})

    history = load_history()
    failed_recent = [vars(h) for h in history[-15:] if not h.passed]

    return {
        "skills": skill_rows,
        "weaknesses": player.weaknesses,
        "failed_recent": list(reversed(failed_recent)),
    }


class QuestHandler(BaseHTTPRequestHandler):
    server_version = "QuestGUI/1.0"

    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        pass  # keep the terminal quiet; errors still surface via HTTP status

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, filename: str, content_type: str) -> None:
        path = WEBUI_DIR / filename
        try:
            body = path.read_bytes()
        except OSError:
            self.send_error(404, "Not Found")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _mission_id_from_query(self, query: str) -> str | None:
        for part in query.split("&"):
            if part.startswith("id="):
                return unquote(part[3:])
        return None

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler name
        parsed = urlparse(self.path)
        path = parsed.path

        if path in STATIC_FILES:
            filename, content_type = STATIC_FILES[path]
            self._send_static(filename, content_type)
            return

        if path == "/api/state":
            self._send_json(build_state_payload())
            return

        if path == "/api/mission":
            mission_id = self._mission_id_from_query(parsed.query)
            payload = build_mission_payload(mission_id) if mission_id else None
            if payload is None:
                self._send_json({"error": "Mission nicht gefunden."}, status=404)
            else:
                self._send_json(payload)
            return

        if path == "/api/achievements":
            self._send_json(build_achievements_payload())
            return

        if path == "/api/review":
            self._send_json(build_review_payload())
            return

        self.send_error(404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler name
        parsed = urlparse(self.path)
        path = parsed.path
        mission_id = self._mission_id_from_query(parsed.query)

        if path == "/api/start" and mission_id:
            self._send_json(do_start(mission_id))
            return
        if path == "/api/hint" and mission_id:
            self._send_json(do_hint(mission_id))
            return
        if path == "/api/check" and mission_id:
            self._send_json(do_check(mission_id))
            return

        self.send_error(400, "Bad Request")


def run(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), QuestHandler)
    url = f"http://{host}:{port}/"
    print(f"Quest GUI laeuft auf {url}  (Strg+C zum Beenden)")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
