"""Ties together evaluator, XP, achievements and persistence for one
`quest check` invocation. This is the only place that mutates PlayerState
as a result of a mission attempt."""
from __future__ import annotations

from dataclasses import dataclass

from quest.achievements import maybe_unlock
from quest.evaluator import CheckResult, run_mission_check
from quest.model import AttemptRecord, Mission, PlayerState, utc_now_iso
from quest.state import append_history, save_player


@dataclass
class AttemptOutcome:
    result: CheckResult
    xp_awarded: int
    newly_unlocked_achievement: str | None
    already_completed: bool


def attempt_mission(mission: Mission, player: PlayerState) -> AttemptOutcome:
    result = run_mission_check(mission)
    already_completed = mission.id in player.completed_missions

    xp_awarded = 0
    unlocked = None

    if result.passed and result.score >= mission.min_pass_ratio:
        if not already_completed:
            xp_awarded = mission.xp_reward
            player.total_xp += xp_awarded
            player.completed_missions.append(mission.id)
            for skill, points in mission.skills.items():
                player.skill_points[skill] = player.skill_points.get(skill, 0) + points
            unlocked = maybe_unlock(mission.grants_achievement, player)
    elif result.score > 0 and not already_completed and mission.id not in player.partial_credit_missions:
        # Partial credit for a serious but incomplete attempt -- granted once per
        # mission, not on every retry, otherwise repeated `check` calls without
        # progress would farm XP indefinitely.
        partial = round(mission.xp_reward * result.score * 0.5)
        if partial > 0:
            xp_awarded = partial
            player.total_xp += partial
            player.partial_credit_missions.append(mission.id)

    player.current_mission = mission.id if not (result.passed and result.score >= mission.min_pass_ratio) else None

    record = AttemptRecord(
        mission_id=mission.id,
        timestamp=utc_now_iso(),
        passed=result.passed,
        score=result.score,
        xp_awarded=xp_awarded,
        detail=result.detail[:4000],
    )
    append_history(record)
    save_player(player)

    return AttemptOutcome(
        result=result,
        xp_awarded=xp_awarded,
        newly_unlocked_achievement=unlocked,
        already_completed=already_completed,
    )
