"""
CodeVault Repository Service
Manages high-level version control operations: committing, branching, history traversal,
and space-saving analytics.
"""
from typing import Dict, List, Optional, Any
from .vcs_models import Repository, Commit, Branch, FileDelta
from .delta_engine import DeltaEngine
from .three_way_merge import ThreeWayMerge

class RepositoryService:
    def __init__(self):
        self.repositories: Dict[str, Repository] = {}

    def create_repository(self, repo_id: str, name: str, owner: str) -> Repository:
        repo = Repository.create(repo_id, name, owner)
        self.repositories[repo_id] = repo
        return repo

    def get_repository(self, repo_id: str) -> Optional[Repository]:
        return self.repositories.get(repo_id)

    def commit(self, repo_id: str, author: str, message: str, files: Dict[str, str], branch_name: Optional[str] = None) -> Commit:
        repo = self.repositories[repo_id]
        target_branch = branch_name or repo.current_branch
        branch = repo.branches.get(target_branch)

        if not branch:
            branch = Branch(name=target_branch)
            repo.branches[target_branch] = branch

        parent_commit = repo.commits.get(branch.head_commit_id) if branch.head_commit_id else None
        new_commit = Commit.create(message=message, author=author, parent_id=parent_commit.commit_id if parent_commit else None)

        # Store delta compression against parent
        for path, content in files.items():
            new_commit.full_snapshots[path] = content
            if parent_commit and path in parent_commit.full_snapshots:
                base_content = parent_commit.full_snapshots[path]
                delta_info = DeltaEngine.generate_delta(base_content, content)
                new_commit.deltas[path] = FileDelta(
                    file_path=path,
                    base_hash=delta_info["base_hash"],
                    target_hash=delta_info["target_hash"],
                    operations=delta_info["operations"],
                    raw_size_bytes=delta_info["raw_size_bytes"],
                    delta_size_bytes=delta_info["delta_size_bytes"],
                    savings_percentage=delta_info["savings_percentage"]
                )
            else:
                raw_bytes = len(content.encode('utf-8'))
                new_commit.deltas[path] = FileDelta(
                    file_path=path,
                    base_hash="",
                    target_hash=DeltaEngine.compute_hash(content),
                    operations=[{"op": "insert", "lines": content.splitlines(keepends=True)}],
                    raw_size_bytes=raw_bytes,
                    delta_size_bytes=raw_bytes,
                    savings_percentage=0.0
                )

        repo.commits[new_commit.commit_id] = new_commit
        branch.head_commit_id = new_commit.commit_id
        return new_commit

    def get_commit_history(self, repo_id: str, branch_name: Optional[str] = None) -> List[Dict[str, Any]]:
        repo = self.repositories[repo_id]
        target_branch = branch_name or repo.current_branch
        branch = repo.branches.get(target_branch)
        if not branch or not branch.head_commit_id:
            return []

        history = []
        curr_id = branch.head_commit_id
        while curr_id:
            c = repo.commits[curr_id]
            history.append({
                "commit_id": c.commit_id,
                "author": c.author,
                "message": c.message,
                "timestamp": c.timestamp,
                "parent_id": c.parent_id,
                "files_count": len(c.full_snapshots),
                "deltas_saved_avg": round(
                    sum(d.savings_percentage for d in c.deltas.values()) / max(1, len(c.deltas)), 2
                )
            })
            curr_id = c.parent_id
        return history

    def calculate_total_savings(self, repo_id: str) -> Dict[str, Any]:
        """Calculates total disk storage saved across all commits via delta compression."""
        repo = self.repositories.get(repo_id)
        if not repo:
            return {"raw_bytes": 0, "delta_bytes": 0, "saved_bytes": 0, "savings_percentage": 0.0}

        raw_total = 0
        delta_total = 0

        for commit in repo.commits.values():
            for d in commit.deltas.values():
                raw_total += d.raw_size_bytes
                delta_total += d.delta_size_bytes

        saved = max(0, raw_total - delta_total)
        pct = round((saved / raw_total) * 100, 2) if raw_total > 0 else 0.0

        return {
            "raw_bytes": raw_total,
            "delta_bytes": delta_total,
            "saved_bytes": saved,
            "savings_percentage": pct
        }
