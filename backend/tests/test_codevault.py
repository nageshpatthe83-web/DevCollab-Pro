import pytest
from app.codevault.delta_engine import DeltaEngine
from app.codevault.three_way_merge import ThreeWayMerge
from app.codevault.repository_service import RepositoryService

def test_delta_compression_and_reconstruction():
    base = "def add(a, b):\n    return a + b\n"
    target = "def add(a, b):\n    # optimized addition\n    return a + b\n"

    delta = DeltaEngine.generate_delta(base, target)
    assert delta["savings_percentage"] >= 0.0
    reconstructed = DeltaEngine.apply_delta(base, delta)
    assert reconstructed == target

def test_three_way_merge_clean():
    base = "line1\nline2\nline3"
    ours = "line1\nline2_edited\nline3"
    theirs = "line1\nline2\nline3"

    res = ThreeWayMerge.merge(base, ours, theirs)
    assert res["conflict"] is False
    assert "line2_edited" in res["merged_text"]

def test_three_way_merge_conflict():
    base = "line1\nline2\nline3"
    ours = "line1\nline2_ours\nline3"
    theirs = "line1\nline2_theirs\nline3"

    res = ThreeWayMerge.merge(base, ours, theirs)
    assert "<<<<<<< OURS" in res["merged_text"]
    assert ">>>>>>> THEIRS" in res["merged_text"]

def test_repository_service_commits():
    service = RepositoryService()
    service.create_repository("repo-1", "TestRepo", "Nagesh")
    c1 = service.commit("repo-1", "Nagesh", "Initial commit", {"main.py": "print('hello')"})
    assert c1.commit_id is not None
    history = service.get_commit_history("repo-1")
    assert len(history) == 1
