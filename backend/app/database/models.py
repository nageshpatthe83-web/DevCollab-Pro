"""
9 Core Database Tables normalized in Third Normal Form (3NF)
1. Users
2. Teams
3. TeamMembers
4. Contests
5. Problems
6. Submissions
7. EvaluationScores
8. LeaderboardEntries
9. GitRepositories
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
import datetime
from .connection import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(20), default="STUDENT") # STUDENT, JUDGE, ORGANIZER
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(100), unique=True, nullable=False)
    leader_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TeamMember(Base):
    __tablename__ = "team_members"
    membership_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    roll_number = Column(String(20))
    role_description = Column(String(100))

class Contest(Base):
    __tablename__ = "contests"
    contest_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Problem(Base):
    __tablename__ = "problems"
    problem_id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey("contests.contest_id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    time_limit_ms = Column(Integer, default=2000)

class Submission(Base):
    __tablename__ = "submissions"
    submission_id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey("contests.contest_id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    language = Column(String(20), default="python")
    code_content = Column(Text, nullable=False)
    status = Column(String(20), default="PENDING")
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

class EvaluationScore(Base):
    __tablename__ = "evaluation_scores"
    score_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id"), unique=True, nullable=False)
    correctness_score = Column(Float, default=0.0)
    code_quality_score = Column(Float, default=0.0)
    performance_score = Column(Float, default=0.0)
    security_score = Column(Float, default=0.0)
    innovation_score = Column(Float, default=0.0)
    collaboration_score = Column(Float, default=0.0)
    final_composite_score = Column(Float, default=0.0)

class LeaderboardEntryModel(Base):
    __tablename__ = "leaderboard_entries"
    entry_id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey("contests.contest_id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    rank = Column(Integer, nullable=False)
    total_score = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class GitRepositoryModel(Base):
    __tablename__ = "git_repositories"
    repo_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    repo_name = Column(String(100), nullable=False)
    total_commits = Column(Integer, default=0)
    storage_saved_pct = Column(Float, default=0.0)
