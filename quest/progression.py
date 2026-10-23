"""Prerequisite gating: which campaigns/missions are unlocked right now."""
from __future__ import annotations

from quest.model import Campaign, Mission, PlayerState, skill_level


def skills_satisfied(required: dict[str, int], player: PlayerState) -> bool:
    for skill, min_level in required.items():
        have = skill_level(player.skill_points.get(skill, 0))
        if have < min_level:
            return False
    return True


def mission_is_unlocked(mission: Mission, player: PlayerState) -> bool:
    if mission.id in player.completed_missions:
        return True
    for prereq_id in mission.prerequisites_missions:
        if prereq_id not in player.completed_missions:
            return False
    return skills_satisfied(mission.prerequisite_skills, player)


def campaign_is_unlocked(campaign: Campaign, player: PlayerState, all_missions: dict[str, Mission]) -> bool:
    if campaign.status != "available":
        return False
    for camp_id in campaign.prerequisite_campaigns:
        camp_missions = [m for m in all_missions.values() if m.campaign_id == camp_id]
        if camp_missions and not all(m.id in player.completed_missions for m in camp_missions):
            return False
    return True


def next_mission_for_campaign(missions: list[Mission], player: PlayerState) -> Mission | None:
    for mission in missions:
        if mission.id in player.completed_missions:
            continue
        if mission_is_unlocked(mission, player):
            return mission
    return None


def find_next_mission(
    campaigns: list[Campaign], missions_by_campaign: dict[str, list[Mission]], player: PlayerState
) -> tuple[Campaign, Mission] | None:
    all_missions = {m.id: m for ms in missions_by_campaign.values() for m in ms}
    for campaign in campaigns:
        if not campaign_is_unlocked(campaign, player, all_missions):
            continue
        missions = missions_by_campaign.get(campaign.id, [])
        candidate = next_mission_for_campaign(missions, player)
        if candidate is not None:
            return campaign, candidate
    return None
