"""Data-driven achievements: a mission declares `grants_achievement`, and
completing it (first time, passing) unlocks that id. The catalog in
curriculum/achievements.json supplies the display title/description.
"""
from __future__ import annotations

from quest.model import PlayerState
from quest.registry import load_achievements_catalog


def maybe_unlock(mission_grants: str | None, player: PlayerState) -> str | None:
    if not mission_grants:
        return None
    if mission_grants in player.achievements:
        return None
    catalog = load_achievements_catalog()
    if mission_grants not in catalog:
        return None
    player.achievements.append(mission_grants)
    return mission_grants


def describe(achievement_id: str) -> dict:
    catalog = load_achievements_catalog()
    return catalog.get(achievement_id, {"title": achievement_id, "description": ""})
