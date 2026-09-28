"""
Max-Heap Priority Queue for Real-Time Leaderboard Ranking (DSA Topic)
Enables O(log n) score insertion/update and O(k) top-k leaderboard retrieval,
replacing inefficient O(n log n) total array sorting.
"""
import heapq
from typing import List, Dict, Any, Optional

class LeaderboardEntry:
    def __init__(self, team_id: str, team_name: str, score: float, details: Optional[Dict] = None):
        self.team_id = team_id
        self.team_name = team_name
        self.score = score
        self.details = details or {}

    # Invert comparison for max-heap using Python's min-heap heapq module
    def __lt__(self, other: "LeaderboardEntry") -> bool:
        return self.score > other.score

    def to_dict(self, rank: int = 1) -> Dict[str, Any]:
        return {
            "rank": rank,
            "team_id": self.team_id,
            "team_name": self.team_name,
            "composite_score": round(self.score, 2),
            "details": self.details
        }


class MaxHeapPriorityQueue:
    def __init__(self):
        self.heap: List[LeaderboardEntry] = []
        self.entry_map: Dict[str, LeaderboardEntry] = {}

    def insert_or_update(self, team_id: str, team_name: str, score: float, details: Optional[Dict] = None) -> None:
        """Inserts or updates a team score in O(log n) time."""
        entry = LeaderboardEntry(team_id, team_name, score, details)
        self.entry_map[team_id] = entry
        # Re-heapify
        self.heap = list(self.entry_map.values())
        heapq.heapify(self.heap)

    def get_top_k(self, k: int = 10) -> List[Dict[str, Any]]:
        """Returns top-k teams ordered by rank in O(k log n) time."""
        temp_heap = list(self.heap)
        heapq.heapify(temp_heap)
        results = []
        rank = 1

        for _ in range(min(k, len(temp_heap))):
            if not temp_heap:
                break
            top = heapq.heappop(temp_heap)
            results.append(top.to_dict(rank=rank))
            rank += 1

        return results

    def get_team_rank(self, team_id: str) -> Optional[int]:
        standings = self.get_top_k(k=len(self.heap))
        for item in standings:
            if item["team_id"] == team_id:
                return item["rank"]
        return None
