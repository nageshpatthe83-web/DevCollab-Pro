import pytest
from app.scoring.scoring_engine import MultiCriteriaScoringEngine
from app.scoring.contribution_tracker import ContributionTracker

def test_weighted_scoring_engine():
    engine = MultiCriteriaScoringEngine()
    metrics = {
        "code_quality": 90.0,
        "performance": 85.0,
        "repo_cleanliness": 80.0,
        "innovation": 90.0,
        "collaboration": 95.0,
        "documentation": 85.0,
        "security": 100.0
    }
    score_res = engine.calculate_score(metrics)
    assert 85.0 <= score_res["final_score"] <= 95.0
    assert "breakdown" in score_res

def test_contribution_tracker():
    commits = [
        {"author": "Nagesh", "commits": 10, "lines_added": 200, "lines_removed": 20, "prs_reviewed": 3},
        {"author": "Kunal", "commits": 12, "lines_added": 250, "lines_removed": 30, "prs_reviewed": 4},
        {"author": "Shantanu", "commits": 8, "lines_added": 180, "lines_removed": 15, "prs_reviewed": 2},
        {"author": "Jagdish", "commits": 9, "lines_added": 190, "lines_removed": 20, "prs_reviewed": 2}
    ]
    res = ContributionTracker.analyze_team_contributions(commits)
    assert res["total_commits"] == 39
    assert len(res["member_breakdown"]) == 4
    assert res["team_collaboration_score"] > 80.0
