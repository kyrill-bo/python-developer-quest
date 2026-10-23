"""Loads campaign and mission metadata from curriculum/*.json files."""
from __future__ import annotations

import json
from pathlib import Path

from quest.model import Campaign, Mission
from quest.state import project_root

CURRICULUM_DIR_NAME = "curriculum"


def curriculum_dir() -> Path:
    return project_root() / CURRICULUM_DIR_NAME


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_campaigns() -> list[Campaign]:
    campaigns: list[Campaign] = []
    base = curriculum_dir()
    if not base.exists():
        return campaigns
    for camp_dir in sorted(base.iterdir()):
        meta_path = camp_dir / "campaign.json"
        if not camp_dir.is_dir() or not meta_path.exists():
            continue
        data = _read_json(meta_path)
        campaigns.append(
            Campaign(
                id=data["id"],
                order=data["order"],
                title=data["title"],
                summary=data["summary"],
                topics=data.get("topics", []),
                skill_tracks=data.get("skill_tracks", []),
                status=data.get("status", "planned"),
                prerequisite_campaigns=data.get("prerequisite_campaigns", []),
                boss_fight=data.get("boss_fight"),
                dir=str(camp_dir),
            )
        )
    campaigns.sort(key=lambda c: c.order)
    return campaigns


def load_missions_for_campaign(campaign: Campaign) -> list[Mission]:
    missions: list[Mission] = []
    camp_path = Path(campaign.dir)
    for mission_dir in sorted(camp_path.iterdir()):
        meta_path = mission_dir / "mission.json"
        if not mission_dir.is_dir() or not meta_path.exists():
            continue
        data = _read_json(meta_path)
        prereq = data.get("prerequisites", {})
        missions.append(
            Mission(
                id=data["id"],
                campaign_id=campaign.id,
                order=data["order"],
                title=data["title"],
                difficulty=data.get("difficulty", 1),
                estimated_minutes=data.get("estimated_minutes", 30),
                xp_reward=data.get("xp_reward", 10),
                type=data["type"],
                dir=str(mission_dir),
                prerequisites_missions=prereq.get("missions", []),
                prerequisite_skills=prereq.get("skills", {}),
                skills=data.get("skills", {}),
                grants_achievement=data.get("grants_achievement"),
                check_function=data.get("check_function"),
                submission=data.get("submission"),
                test_path=data.get("test_path"),
                hints=data.get("hints", []),
                min_pass_ratio=data.get("min_pass_ratio", 1.0),
            )
        )
    missions.sort(key=lambda m: m.order)
    return missions


def load_all_missions() -> dict[str, Mission]:
    result: dict[str, Mission] = {}
    for campaign in load_campaigns():
        for mission in load_missions_for_campaign(campaign):
            result[mission.id] = mission
    return result


def load_achievements_catalog() -> dict[str, dict]:
    path = curriculum_dir() / "achievements.json"
    if not path.exists():
        return {}
    return _read_json(path)
