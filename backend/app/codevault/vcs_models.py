"""
CodeVault VCS Data Models
Represents in-memory and database mappings for commits, branches, and repositories.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import hashlib

@dataclass
class FileDelta:
    file_path: str
    base_hash: str
    target_hash: str
    operations: List[Dict]
    raw_size_bytes: int
    delta_size_bytes: int
    savings_percentage: float

@dataclass
class Commit:
    commit_id: str
    message: str
    author: str
    timestamp: float = field(default_factory=time.time)
    parent_id: Optional[str] = None
    deltas: Dict[str, FileDelta] = field(default_factory=dict)
    full_snapshots: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def create(cls, message: str, author: str, parent_id: Optional[str] = None) -> "Commit":
        payload = f"{message}:{author}:{time.time()}:{parent_id}"
        commit_id = hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12]
        return cls(commit_id=commit_id, message=message, author=author, parent_id=parent_id)

@dataclass
class Branch:
    name: str
    head_commit_id: Optional[str] = None

@dataclass
class Repository:
    repo_id: str
    name: str
    owner: str
    branches: Dict[str, Branch] = field(default_factory=dict)
    commits: Dict[str, Commit] = field(default_factory=dict)
    current_branch: str = "main"

    @classmethod
    def create(cls, repo_id: str, name: str, owner: str) -> "Repository":
        repo = cls(repo_id=repo_id, name=name, owner=owner)
        repo.branches["main"] = Branch(name="main", head_commit_id=None)
        return repo
