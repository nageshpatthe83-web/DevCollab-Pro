"""
Multi-Criteria Weighted Scoring Engine
Computes transparent composite score across 7 key dimensions:
Score = 0.25(Quality) + 0.20(Perf) + 0.15(Repo) + 0.15(Innovation) + 0.10(Collab) + 0.10(Docs) + 0.05(Security)
"""
from typing import Dict, Any

class MultiCriteriaScoringEngine:
    DEFAULT_WEIGHTS = {
        "code_quality": 0.25,
        "performance": 0.20,
        "repo_cleanliness": 0.15,
        "innovation": 0.15,
        "collaboration": 0.10,
        "documentation": 0.10,
        "security": 0.05
    }

    def __init__(self, custom_weights: Optional[Dict[str, float]] = None):
        self.weights = custom_weights or self.DEFAULT_WEIGHTS

    def calculate_score(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates the composite score and returns a transparent breakdown for explainability.
        """
        weighted_breakdown = {}
        total_score = 0.0

        for dimension, weight in self.weights.items():
            raw_value = metrics.get(dimension, 75.0)
            # Bound value between 0 and 100
            bounded_val = max(0.0, min(100.0, float(raw_value)))
            contribution = round(bounded_val * weight, 2)
            weighted_breakdown[dimension] = {
                "raw_score": bounded_val,
                "weight": weight,
                "weighted_contribution": contribution
            }
            total_score += contribution

        final_composite = round(total_score, 2)
        return {
            "final_score": final_composite,
            "weights_used": self.weights,
            "breakdown": weighted_breakdown,
            "explainability_summary": (
                f"Composite {final_composite}/100 based on Quality ({weighted_breakdown['code_quality']['weighted_contribution']} pts), "
                f"Performance ({weighted_breakdown['performance']['weighted_contribution']} pts), "
                f"Repository ({weighted_breakdown['repo_cleanliness']['weighted_contribution']} pts), "
                f"Innovation ({weighted_breakdown['innovation']['weighted_contribution']} pts), "
                f"Collaboration ({weighted_breakdown['collaboration']['weighted_contribution']} pts), "
                f"Docs ({weighted_breakdown['documentation']['weighted_contribution']} pts), and "
                f"Security ({weighted_breakdown['security']['weighted_contribution']} pts)."
            )
        }
