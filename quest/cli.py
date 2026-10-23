"""python -m quest <command> -- see docs/progression-system.md for the full
command reference. All argparse subcommands live here; each `cmd_*`
function returns an int exit code."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from quest import achievements as ach
from quest import progression
from quest import render as r
from quest.engine import attempt_mission
from quest.model import SKILL_TRACKS, rank_for_xp, skill_level, xp_to_next_rank
from quest.registry import load_achievements_catalog, load_campaigns, load_missions_for_campaign
from quest.state import load_history, load_player, save_player


def _load_world():
    campaigns = load_campaigns()
    missions_by_campaign = {c.id: load_missions_for_campaign(c) for c in campaigns}
    all_missions = {m.id: m for ms in missions_by_campaign.values() for m in ms}
    return campaigns, missions_by_campaign, all_missions


def _load_player_or_warn():
    lr = load_player()
    if lr.warning:
        print(r.yellow(f"[WARNUNG] {lr.warning}"))
    return lr.player


def _find_mission(mission_id: str, all_missions: dict):
    return all_missions.get(mission_id)


def cmd_status(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    campaigns, missions_by_campaign, all_missions = _load_world()
    level, rank = rank_for_xp(player.total_xp)
    to_next, into_current = xp_to_next_rank(player.total_xp)

    print(r.header(f"{player.name} -- Level {level}: {rank}"))
    print(f"XP: {r.bold(str(player.total_xp))}")
    if to_next is not None:
        print(f"Naechster Rank in {to_next} XP  {r.bar(into_current, into_current + to_next)}")
    else:
        print(r.green("Maximaler Rank erreicht."))

    print(f"\nAbgeschlossene Missionen: {len(player.completed_missions)}")
    print(f"Achievements: {len(player.achievements)}")

    nxt = progression.find_next_mission(campaigns, missions_by_campaign, player)
    print()
    if player.current_mission and player.current_mission in all_missions:
        m = all_missions[player.current_mission]
        print(f"Aktive Mission: {r.bold(m.title)} ({m.id})")
        print(r.dim("  -> `python -m quest check` wenn du bereit bist, oder `python -m quest hint`."))
    elif nxt:
        _, mission = nxt
        print(f"Naechste verfuegbare Mission: {r.bold(mission.title)} ({mission.id})")
        print(r.dim("  -> `python -m quest start`"))
    else:
        print(r.green("Alle verfuegbaren Missionen abgeschlossen. Pruefe `python -m quest map`."))

    history = load_history()
    if history:
        print(f"\n{r.bold('Letzte Versuche:')}")
        for rec in history[-5:]:
            icon = r.status_icon(rec.passed)
            print(f"  {icon} {rec.mission_id}  score={rec.score:.2f}  +{rec.xp_awarded} XP  ({rec.timestamp})")
    return 0


def cmd_map(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    campaigns, missions_by_campaign, all_missions = _load_world()
    print(r.header("CAMPAIGN MAP"))
    for campaign in campaigns:
        unlocked = progression.campaign_is_unlocked(campaign, player, all_missions)
        missions = missions_by_campaign.get(campaign.id, [])
        done = sum(1 for m in missions if m.id in player.completed_missions)
        status_txt = {
            "available": r.green("VERFUEGBAR") if unlocked else r.dim("GESPERRT"),
            "planned": r.dim("GEPLANT"),
        }.get(campaign.status, campaign.status)
        print(f"\n{r.bold(campaign.title)}  [{status_txt}]")
        print(f"  {campaign.summary}")
        if missions:
            print(f"  Fortschritt: {done}/{len(missions)} Missionen  {r.bar(done, len(missions), 20)}")
            for m in missions:
                is_done = m.id in player.completed_missions
                is_unlocked = unlocked and progression.mission_is_unlocked(m, player)
                icon = r.lock_icon(is_unlocked, is_done)
                print(f"    {icon} {m.title}  (+{m.xp_reward} XP)")
        elif campaign.status == "planned":
            print(r.dim(f"  Themen: {', '.join(campaign.topics[:6])}{'...' if len(campaign.topics) > 6 else ''}"))
    return 0


def cmd_campaign(args: argparse.Namespace) -> int:
    campaigns, missions_by_campaign, _all_missions = _load_world()
    player = _load_player_or_warn()
    if args.campaign_id:
        matches = [c for c in campaigns if c.id == args.campaign_id or args.campaign_id in c.id]
        if not matches:
            print(r.red(f"Campaign '{args.campaign_id}' nicht gefunden."))
            return 1
        campaigns = matches
    for campaign in campaigns:
        print(r.header(campaign.title))
        print(campaign.summary)
        print(f"\nStatus: {campaign.status}")
        if campaign.prerequisite_campaigns:
            print(f"Voraussetzungen: {', '.join(campaign.prerequisite_campaigns)}")
        print(f"Skill-Tracks: {', '.join(SKILL_TRACKS.get(s, s) for s in campaign.skill_tracks)}")
        print("\nThemen:")
        for t in campaign.topics:
            print(f"  - {t}")
        if campaign.boss_fight:
            print(f"\n{r.bold('Boss Fight:')} {campaign.boss_fight}")
        missions = missions_by_campaign.get(campaign.id, [])
        if missions:
            print(f"\n{r.bold('Missionen:')}")
            for m in missions:
                is_done = m.id in player.completed_missions
                print(f"  {r.lock_icon(True, is_done)} {m.title} (+{m.xp_reward} XP, Schwierigkeit {m.difficulty}/5)")
    return 0


def _print_mission_brief(mission) -> None:
    scenario_path = Path(mission.dir) / "scenario.md"
    print(r.header(f"MISSION: {mission.title}"))
    print(f"ID: {mission.id}")
    print(f"Schwierigkeit: {mission.difficulty}/5   Geschaetzte Zeit: {mission.estimated_minutes} min   XP: {mission.xp_reward}")
    print()
    if scenario_path.exists():
        print(scenario_path.read_text(encoding="utf-8"))
    else:
        print(r.yellow("(Keine scenario.md fuer diese Mission gefunden.)"))
    print(r.dim(f"\nBefehle: `python -m quest hint {mission.id}` | `python -m quest check {mission.id}`"))


def cmd_start(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    campaigns, missions_by_campaign, all_missions = _load_world()

    if args.mission_id:
        mission = _find_mission(args.mission_id, all_missions)
        if mission is None:
            print(r.red(f"Mission '{args.mission_id}' nicht gefunden."))
            return 1
    else:
        nxt = progression.find_next_mission(campaigns, missions_by_campaign, player)
        if nxt is None:
            print(r.green("Keine weiteren Missionen verfuegbar. Siehe `python -m quest map`."))
            return 0
        _, mission = nxt

    player.current_mission = mission.id
    save_player(player)
    _print_mission_brief(mission)
    return 0


def cmd_hint(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    _, _, all_missions = _load_world()
    mission_id = args.mission_id or player.current_mission
    if not mission_id:
        print(r.red("Keine aktive Mission. Nutze `python -m quest start` zuerst."))
        return 1
    mission = _find_mission(mission_id, all_missions)
    if mission is None:
        print(r.red(f"Mission '{mission_id}' nicht gefunden."))
        return 1
    if not mission.hints:
        print(r.yellow("Diese Mission hat keine Hints -- du bist auf dich allein gestellt."))
        return 0

    used = player.hints_used.get(mission.id, 0)
    if used >= len(mission.hints):
        print(r.yellow(f"Alle {len(mission.hints)} Hints fuer diese Mission wurden bereits gezeigt."))
        for i, h in enumerate(mission.hints, start=1):
            print(f"  Hint {i}: {h}")
        return 0

    hint_text = mission.hints[used]
    player.hints_used[mission.id] = used + 1
    save_player(player)
    print(f"{r.bold(f'Hint {used + 1}/{len(mission.hints)}:')} {hint_text}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    _, _, all_missions = _load_world()
    mission_id = args.mission_id or player.current_mission
    if not mission_id:
        print(r.red("Keine aktive Mission. Nutze `python -m quest start` zuerst."))
        return 1
    mission = _find_mission(mission_id, all_missions)
    if mission is None:
        print(r.red(f"Mission '{mission_id}' nicht gefunden."))
        return 1

    outcome = attempt_mission(mission, player)
    res = outcome.result
    print(r.header(f"CHECK: {mission.title}"))
    print(res.detail)
    print()
    if res.passed and res.score >= mission.min_pass_ratio:
        if outcome.already_completed:
            print(r.green("Bestanden (bereits vorher abgeschlossen, keine erneute XP)."))
        else:
            print(r.green(f"BESTANDEN -- +{outcome.xp_awarded} XP"))
        if outcome.newly_unlocked_achievement:
            info = ach.describe(outcome.newly_unlocked_achievement)
            print(r.magenta(f"Achievement freigeschaltet: {info.get('title')} -- {info.get('description')}"))
    else:
        print(r.red(f"NICHT BESTANDEN  (score={res.score:.2f})"))
        if outcome.xp_awarded:
            print(r.yellow(f"Teil-XP fuer ernsthaften Versuch: +{outcome.xp_awarded} XP"))
    return 0 if res.passed else 2


def cmd_progress(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    campaigns, missions_by_campaign, _all_missions = _load_world()
    print(r.header("PROGRESS REPORT"))
    for campaign in campaigns:
        missions = missions_by_campaign.get(campaign.id, [])
        if not missions:
            continue
        done = sum(1 for m in missions if m.id in player.completed_missions)
        pct = 100 * done / len(missions) if missions else 0
        print(f"{campaign.title}: {done}/{len(missions)} ({pct:.0f}%)  {r.bar(done, len(missions), 20)}")

    print(f"\n{r.bold('Skill Tree:')}")
    for key, label in SKILL_TRACKS.items():
        pts = player.skill_points.get(key, 0)
        lvl = skill_level(pts)
        print(f"  {label:<32} Lv.{lvl}/5  {r.bar(lvl, 5, 10)}  ({pts} pts)")

    if player.weaknesses:
        print(f"\n{r.bold('Schwachstellen:')}")
        for topic, note in player.weaknesses.items():
            print(f"  - {topic}: {note}")
    return 0


def cmd_achievements(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    catalog = load_achievements_catalog()
    print(r.header("ACHIEVEMENTS"))
    for aid, info in catalog.items():
        if aid in player.achievements:
            print(f"{r.green('[x]')} {r.bold(info['title'])} -- {info['description']}")
        else:
            print(f"{r.dim('[ ]')} {r.dim(info['title'])}")
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    player = _load_player_or_warn()
    print(r.header("REVIEW"))
    strong, developing, weak = [], [], []
    for key, label in SKILL_TRACKS.items():
        pts = player.skill_points.get(key, 0)
        lvl = skill_level(pts)
        if lvl >= 3:
            strong.append(label)
        elif lvl >= 1:
            developing.append(label)
        elif pts > 0:
            weak.append(label)

    if strong:
        print(f"{r.green('Stark:')} {', '.join(strong)}")
    if developing:
        print(f"{r.yellow('Im Aufbau:')} {', '.join(developing)}")
    if weak:
        print(f"{r.red('Schwach:')} {', '.join(weak)}")
    if not (strong or developing or weak):
        print(r.dim("Noch keine Missionen abgeschlossen -- starte mit `python -m quest start`."))

    if player.weaknesses:
        print(f"\n{r.bold('Empfohlene Wiederholung:')}")
        for topic, note in player.weaknesses.items():
            print(f"  - {topic}: {note}")

    history = load_history()
    failed_recent = [h for h in history[-15:] if not h.passed]
    if failed_recent:
        print(f"\n{r.bold('Zuletzt gescheiterte Versuche:')}")
        for h in failed_recent:
            print(f"  - {h.mission_id} (score={h.score:.2f})")
    return 0


def cmd_gui(args: argparse.Namespace) -> int:
    from quest.gui import run

    run(port=args.port, open_browser=not args.no_browser)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="quest", description="Python Developer Quest CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Rank, XP, aktive Mission, letzte Versuche").set_defaults(func=cmd_status)
    sub.add_parser("map", help="Campaign-Map mit Lock-Status").set_defaults(func=cmd_map)

    p = sub.add_parser("campaign", help="Details zu einer oder allen Campaigns")
    p.add_argument("campaign_id", nargs="?", default=None)
    p.set_defaults(func=cmd_campaign)

    p = sub.add_parser("start", help="Naechste Mission anzeigen (oder per ID)")
    p.add_argument("mission_id", nargs="?", default=None)
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("hint", help="Naechsten Hint fuer die aktive Mission zeigen")
    p.add_argument("mission_id", nargs="?", default=None)
    p.set_defaults(func=cmd_hint)

    p = sub.add_parser("check", help="Mission evaluieren")
    p.add_argument("mission_id", nargs="?", default=None)
    p.set_defaults(func=cmd_check)

    sub.add_parser("progress", help="Completion %% und Skill-Tree").set_defaults(func=cmd_progress)
    sub.add_parser("achievements", help="Erreichte und gesperrte Achievements").set_defaults(func=cmd_achievements)
    sub.add_parser("review", help="Staerken/Schwaechen-Zusammenfassung").set_defaults(func=cmd_review)

    p = sub.add_parser("gui", help="Lokale Web-GUI starten (Browser-basiertes Dashboard)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-browser", action="store_true", help="Browser nicht automatisch oeffnen")
    p.set_defaults(func=cmd_gui)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
