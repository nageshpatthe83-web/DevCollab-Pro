"""
CodeVault Three-Way Merge Engine
Detects merge conflicts and performs automated branch reconciliation
using common ancestor baseline.
"""
import difflib
from typing import Dict, List, Any

class ThreeWayMerge:
    """
    Performs 3-way merge between base (ancestor), ours (target branch), and theirs (source branch).
    Generates standard Git merge conflict markers (<<<<<<< OURS, =======, >>>>>>> THEIRS).
    """

    @staticmethod
    def merge(base_text: str, ours_text: str, theirs_text: str) -> Dict[str, Any]:
        base_lines = base_text.splitlines()
        ours_lines = ours_text.splitlines()
        theirs_lines = theirs_text.splitlines()

        # If either branch has no change compared to base
        if ours_lines == base_lines:
            return {"conflict": False, "merged_text": theirs_text, "conflicts_count": 0}
        if theirs_lines == base_lines:
            return {"conflict": False, "merged_text": ours_text, "conflicts_count": 0}
        if ours_lines == theirs_lines:
            return {"conflict": False, "merged_text": ours_text, "conflicts_count": 0}

        # Line-by-line 3-way reconciliation
        diff_ours = list(difflib.ndiff(base_lines, ours_lines))
        diff_theirs = list(difflib.ndiff(base_lines, theirs_lines))

        merged: List[str] = []
        conflicts = 0
        has_conflict = False

        # Simple block-based reconciliation
        ours_added = [line[2:] for line in diff_ours if line.startswith('+ ')]
        theirs_added = [line[2:] for line in diff_theirs if line.startswith('+ ')]

        # Check for collision
        if set(ours_added).intersection(set(theirs_added)) or (ours_added and not theirs_added) or (theirs_added and not ours_added):
            # Combine non-colliding
            combined = []
            for line in ours_lines:
                combined.append(line)
            for line in theirs_lines:
                if line not in combined:
                    combined.append(line)
            return {
                "conflict": False,
                "merged_text": "\n".join(combined),
                "conflicts_count": 0
            }

        # Otherwise mark conflict
        has_conflict = True
        conflicts = 1
        conflict_result = [
            "<<<<<<< OURS (Target Branch)",
            ours_text,
            "=======",
            theirs_text,
            ">>>>>>> THEIRS (Incoming Branch)"
        ]

        return {
            "conflict": has_conflict,
            "merged_text": "\n".join(conflict_result),
            "conflicts_count": conflicts
        }
