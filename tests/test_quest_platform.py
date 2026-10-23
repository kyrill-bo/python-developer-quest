"""Tests for the quest platform itself (not for mission content)."""
from pathlib import Path

from quest import engine, registry, state
from quest.evaluator import CheckResult, run_mission_check
from quest.model import Mission, PlayerState, rank_for_xp, skill_level
from quest.progression import mission_is_unlocked

# --- model.py --------------------------------------------------------------

def test_rank_for_xp_boundaries():
    assert rank_for_xp(0) == (1, "Python Initiate")
    assert rank_for_xp(149) == (1, "Python Initiate")
    assert rank_for_xp(150) == (2, "Code Explorer")
    assert rank_for_xp(8500) == (10, "Senior Backend Candidate")
    assert rank_for_xp(999999) == (10, "Senior Backend Candidate")


def test_skill_level_scale():
    assert skill_level(0) == 0
    assert skill_level(14) == 0
    assert skill_level(15) == 1
    assert skill_level(1000) == 5  # capped at 5


def test_player_state_roundtrip():
    player = PlayerState(name="Test", total_xp=42, completed_missions=["a/b"])
    restored = PlayerState.from_dict(player.to_dict())
    assert restored.name == "Test"
    assert restored.total_xp == 42
    assert restored.completed_missions == ["a/b"]


# --- state.py ---------------------------------------------------------------

def test_save_and_load_player_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "project_root", lambda: tmp_path)
    player = PlayerState(name="Kyrill", total_xp=100)
    state.save_player(player)
    loaded = state.load_player()
    assert loaded.warning is None
    assert loaded.player.total_xp == 100
    assert loaded.player.name == "Kyrill"


def test_load_player_handles_corrupt_file_safely(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "project_root", lambda: tmp_path)
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "player.json").write_text("{not valid json", encoding="utf-8")

    result = state.load_player()

    assert result.warning is not None
    assert result.player.total_xp == 0  # fresh player, did not crash
    assert (state_dir / "player.json.corrupt").exists()


def test_history_append_and_load(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "project_root", lambda: tmp_path)
    from quest.model import AttemptRecord

    record = AttemptRecord(mission_id="m1", timestamp="t", passed=True, score=1.0, xp_awarded=10, detail="ok")
    state.append_history(record)
    history = state.load_history()
    assert len(history) == 1
    assert history[0].mission_id == "m1"


# --- registry.py -------------------------------------------------------------

def test_all_campaigns_load_in_order():
    campaigns = registry.load_campaigns()
    assert len(campaigns) == 15
    orders = [c.order for c in campaigns]
    assert orders == sorted(orders)
    assert campaigns[0].id == "campaign-00-onboarding"
    assert campaigns[0].status == "available"


def test_onboarding_missions_load_in_order():
    campaigns = registry.load_campaigns()
    onboarding = next(c for c in campaigns if c.id == "campaign-00-onboarding")
    missions = registry.load_missions_for_campaign(onboarding)
    assert len(missions) == 7
    assert [m.order for m in missions] == list(range(1, 8))
    assert missions[0].id == "campaign-00-onboarding/mission-01-recon"


def test_achievements_catalog_loads():
    catalog = registry.load_achievements_catalog()
    assert "first_python_function" in catalog
    assert "title" in catalog["first_python_function"]


# --- progression.py -----------------------------------------------------------

def test_mission_locked_until_prerequisite_completed():
    mission = Mission(
        id="camp/m2", campaign_id="camp", order=2, title="m2", difficulty=1,
        estimated_minutes=10, xp_reward=10, type="check_script", dir="/tmp",
        prerequisites_missions=["camp/m1"],
    )
    player = PlayerState()
    assert mission_is_unlocked(mission, player) is False
    player.completed_missions.append("camp/m1")
    assert mission_is_unlocked(mission, player) is True


def test_mission_without_prerequisites_is_unlocked():
    mission = Mission(
        id="camp/m1", campaign_id="camp", order=1, title="m1", difficulty=1,
        estimated_minutes=10, xp_reward=10, type="check_script", dir="/tmp",
    )
    assert mission_is_unlocked(mission, PlayerState()) is True


# --- evaluator.py (check_script dispatch) -------------------------------------

def test_check_script_dispatch_runs_real_check_function():
    campaigns = registry.load_campaigns()
    onboarding = next(c for c in campaigns if c.id == "campaign-00-onboarding")
    missions = registry.load_missions_for_campaign(onboarding)
    recon = next(m for m in missions if m.id.endswith("mission-01-recon"))

    recon_json = Path(recon.dir) / "workspace" / "recon.json"
    existed_before = recon_json.exists()
    try:
        if recon_json.exists():
            recon_json.unlink()
        result = run_mission_check(recon)
        assert result.passed is False
    finally:
        if not existed_before and recon_json.exists():
            recon_json.unlink()


def test_partial_xp_is_granted_only_once_per_mission(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "project_root", lambda: tmp_path)
    monkeypatch.setattr(engine, "run_mission_check", lambda m: CheckResult(False, 0.5, "half done"))

    mission = Mission(
        id="camp/m1", campaign_id="camp", order=1, title="m1", difficulty=1,
        estimated_minutes=10, xp_reward=10, type="check_script", dir="/tmp",
    )
    player = PlayerState()

    first = engine.attempt_mission(mission, player)
    assert first.xp_awarded == 2  # round(10 * 0.5 * 0.5) == round(2.5) == 2 (banker's rounding)
    assert player.total_xp == 2

    second = engine.attempt_mission(mission, player)
    assert second.xp_awarded == 0  # no repeat credit for an unchanged retry
    assert player.total_xp == 2


def test_check_script_unknown_function_fails_gracefully():
    mission = Mission(
        id="camp/x", campaign_id="camp", order=1, title="x", difficulty=1,
        estimated_minutes=10, xp_reward=10, type="check_script", dir="/tmp",
        check_function="this_function_does_not_exist",
    )
    result = run_mission_check(mission)
    assert result.passed is False
    assert "not" in result.detail.lower() or "nicht" in result.detail.lower()
