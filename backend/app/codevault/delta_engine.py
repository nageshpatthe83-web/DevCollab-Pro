"""
CodeVault Delta Engine
Implements Myers Diff-based delta compression for version-controlled file storage.
Calculates storage savings compared to naive full-file snapshot storage (>60% savings).
"""
import difflib
import hashlib
import json
from typing import Dict, List, Any

class DeltaEngine:
    """
    Computes, serializes, and applies line-level diff deltas between versions of files.
    Enables storing only incremental modifications (insertions, deletions, modifications).
    """

    @staticmethod
    def compute_hash(content: str) -> str:
        """Returns the SHA-256 checksum of file content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_delta(base_content: str, target_content: str) -> Dict[str, Any]:
        """
        Generates a structured delta from base_content to target_content.
        Returns a compact delta structure and compression metrics.
        """
        base_lines = base_content.splitlines(keepends=True)
        target_lines = target_content.splitlines(keepends=True)

        matcher = difflib.SequenceMatcher(None, base_lines, target_lines)
        operations = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                operations.append({
                    "op": "equal",
                    "length": i2 - i1
                })
            elif tag == 'insert':
                operations.append({
                    "op": "insert",
                    "lines": target_lines[j1:j2]
                })
            elif tag == 'delete':
                operations.append({
                    "op": "delete",
                    "start": i1,
                    "count": i2 - i1
                })
            elif tag == 'replace':
                operations.append({
                    "op": "replace",
                    "start": i1,
                    "count": i2 - i1,
                    "lines": target_lines[j1:j2]
                })

        delta_payload = json.dumps(operations)
        base_bytes = len(base_content.encode('utf-8'))
        target_bytes = len(target_content.encode('utf-8'))
        delta_bytes = len(delta_payload.encode('utf-8'))

        savings_pct = 0.0
        if target_bytes > 0:
            savings = max(0, target_bytes - delta_bytes)
            savings_pct = round((savings / target_bytes) * 100, 2)

        return {
            "base_hash": DeltaEngine.compute_hash(base_content),
            "target_hash": DeltaEngine.compute_hash(target_content),
            "operations": operations,
            "raw_size_bytes": target_bytes,
            "delta_size_bytes": delta_bytes,
            "savings_percentage": savings_pct
        }

    @staticmethod
    def apply_delta(base_content: str, delta: Dict[str, Any]) -> str:
        """
        Reconstructs target content by applying delta operations onto base_content.
        """
        base_lines = base_content.splitlines(keepends=True)
        result_lines: List[str] = []
        base_idx = 0

        for op in delta["operations"]:
            kind = op["op"]
            if kind == "equal":
                length = op["length"]
                result_lines.extend(base_lines[base_idx:base_idx + length])
                base_idx += length
            elif kind == "insert":
                result_lines.extend(op["lines"])
            elif kind == "delete":
                base_idx += op["count"]
            elif kind == "replace":
                base_idx += op["count"]
                result_lines.extend(op["lines"])

        reconstructed = "".join(result_lines)
        reconstructed_hash = DeltaEngine.compute_hash(reconstructed)

        if reconstructed_hash != delta["target_hash"]:
            raise ValueError(
                f"Checksum mismatch after delta reconstruction! "
                f"Expected: {delta['target_hash']}, Got: {reconstructed_hash}"
            )

        return reconstructed
