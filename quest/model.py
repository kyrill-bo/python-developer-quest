"""Dataclasses for campaigns, missions and player state.

Kept dependency-free (stdlib only) so the quest CLI runs before any
virtualenv exists -- the CLI itself is part of Campaign 0's bootstrap story.
"""
from __future__ import annotations

import getpass
from dataclasses import dataclass, field
from datetime import UTC, datetime


def _default_player_name() -> str:
    try:
        return getpass.getuser() or "Player"
    except Exception:
        return "Player"

RANKS: list[tuple[int, str]] = [
    (0, "Python Initiate"),
    (150, "Code Explorer"),
    (400, "Python Apprentice"),
    (800, "Backend Builder"),
    (1400, "API Engineer"),
    (2200, "Database Specialist"),
    (3200, "Microservices Engineer"),
    (4500, "Data Pipeline Engineer"),
    (6200, "Production Engineer"),
    (8500, "Senior Backend Candidate"),
]

SKILL_TRACKS: dict[str, str] = {
    "python_core": "Python Core",
    "python_advanced": "Python Advanced",
    "fastapi": "FastAPI",
    "django": "Django REST Framework",
    "databases": "Databases",
    "testing": "Testing and Quality",
    "async": "Asynchronous Programming",
    "microservices": "Microservices",
    "messaging": "Messaging and Event-Driven Architecture",
    "data_engineering": "Data Engineering",
    "containers": "Docker and Kubernetes",
    "security": "Security",
    "observability": "Observability and Reliability",
    "system_design": "System Design",
}


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass
class Mission:
    id: str  # e.g. "campaign-00/mission-01-recon"
    campaign_id: str
    order: int
    title: str
    difficulty: int
    estimated_minutes: int
    xp_reward: int
    type: str  # "check_script" | "pytest"
    dir: str  # absolute path to mission directory
    prerequisites_missions: list[str] = field(default_factory=list)
    prerequisite_skills: dict[str, int] = field(default_factory=dict)
    skills: dict[str, int] = field(default_factory=dict)
    grants_achievement: str | None = None
    check_function: str | None = None  # for check_script missions
    submission: str | None = None  # relative path, for pytest missions
    test_path: str | None = None  # relative path, for pytest missions
    hints: list[str] = field(default_factory=list)
    min_pass_ratio: float = 1.0  # fraction of tests that must pass for full XP


@dataclass
class Campaign:
    id: str
    order: int
    title: str
    summary: str
    topics: list[str]
    skill_tracks: list[str]
    status: str  # "available" | "planned"
    prerequisite_campaigns: list[str] = field(default_factory=list)
    boss_fight: str | None = None
    dir: str = ""


@dataclass
class AttemptRecord:
    mission_id: str
    timestamp: str
    passed: bool
    score: float
    xp_awarded: int
    detail: str


@dataclass
class PlayerState:
    name: str = field(default_factory=_default_player_name)
    total_xp: int = 0
    completed_missions: list[str] = field(default_factory=list)
    hints_used: dict[str, int] = field(default_factory=dict)
    achievements: list[str] = field(default_factory=list)
    skill_points: dict[str, int] = field(default_factory=dict)
    partial_credit_missions: list[str] = field(default_factory=list)
    current_mission: str | None = None
    weaknesses: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "total_xp": self.total_xp,
            "completed_missions": self.completed_missions,
            "hints_used": self.hints_used,
            "achievements": self.achievements,
            "skill_points": self.skill_points,
            "partial_credit_missions": self.partial_credit_missions,
            "current_mission": self.current_mission,
            "weaknesses": self.weaknesses,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> PlayerState:
        return cls(
            name=data.get("name") or _default_player_name(),
            total_xp=data.get("total_xp", 0),
            completed_missions=list(data.get("completed_missions", [])),
            hints_used=dict(data.get("hints_used", {})),
            achievements=list(data.get("achievements", [])),
            skill_points=dict(data.get("skill_points", {})),
            partial_credit_missions=list(data.get("partial_credit_missions", [])),
            current_mission=data.get("current_mission"),
            weaknesses=dict(data.get("weaknesses", {})),
            created_at=data.get("created_at", utc_now_iso()),
            updated_at=data.get("updated_at", utc_now_iso()),
        )


def rank_for_xp(xp: int) -> tuple[int, str]:
    """Return (level 1-10, rank title) for a given XP total."""
    level = 1
    title = RANKS[0][1]
    for idx, (threshold, name) in enumerate(RANKS, start=1):
        if xp >= threshold:
            level = idx
            title = name
        else:
            break
    return level, title


def xp_to_next_rank(xp: int) -> tuple[int | None, int]:
    """Return (xp needed for next rank, xp into current rank). None if max rank."""
    level, _ = rank_for_xp(xp)
    if level >= len(RANKS):
        return None, 0
    next_threshold = RANKS[level][0]
    return next_threshold - xp, xp - RANKS[level - 1][0]


def skill_level(points: int) -> int:
    """0-5 scale, 15 points per level."""
    return min(5, points // 15)
