"""
AlgoPro Empirical Big-O Complexity Fitter
Runs an algorithm on increasing problem sizes (n) and determines whether its
computational complexity conforms to O(1), O(log n), O(n), O(n log n), O(n^2), or O(2^n).
"""
import math
import time
from typing import List, Dict, Tuple, Any, Callable

class EmpiricalBigOFitter:
    """
    Fits empirical execution times against theoretical algorithmic growth curves using
    least-squares regression analysis.
    """

    SUPPORTED_COMPLEXITIES = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(2^n)"]

    @classmethod
    def fit(cls, n_values: List[int], times_ms: List[float]) -> Dict[str, Any]:
        if len(n_values) != len(times_ms) or len(n_values) < 3:
            return {"verdict": "Unknown", "r_squared": 0.0, "fits": {}}

        # Prevent zero / negative times
        clean_times = [max(0.0001, t) for t in times_ms]

        fits = {}
        for comp in cls.SUPPORTED_COMPLEXITIES:
            r2 = cls._calculate_r_squared(n_values, clean_times, comp)
            fits[comp] = round(r2, 4)

        # Select highest correlation coefficient (R^2 closest to 1.0)
        best_fit = max(fits.items(), key=lambda item: item[1])

        # If highest R^2 is below 0.6, fallback to sensible approximation
        verdict = best_fit[0]
        if best_fit[1] < 0.6:
            verdict = "O(n)" # default fallback if noise is high

        return {
            "verdict": verdict,
            "best_r_squared": best_fit[1],
            "correlation_scores": fits,
            "data_points": [{"n": n, "time_ms": round(t, 4)} for n, t in zip(n_values, times_ms)]
        }

    @classmethod
    def _calculate_r_squared(cls, n_vals: List[int], times: List[float], complexity_type: str) -> float:
        try:
            x_transformed = []
            for n in n_vals:
                if complexity_type == "O(1)":
                    x_transformed.append(1.0)
                elif complexity_type == "O(log n)":
                    x_transformed.append(math.log2(max(2, n)))
                elif complexity_type == "O(n)":
                    x_transformed.append(float(n))
                elif complexity_type == "O(n log n)":
                    x_transformed.append(float(n) * math.log2(max(2, n)))
                elif complexity_type == "O(n^2)":
                    x_transformed.append(float(n ** 2))
                elif complexity_type == "O(2^n)":
                    x_transformed.append(2.0 ** min(25, n))

            # Linear regression: times = slope * x_transformed + intercept
            n_pts = len(n_vals)
            sum_x = sum(x_transformed)
            sum_y = sum(times)
            sum_xy = sum(x * y for x, y in zip(x_transformed, times))
            sum_xx = sum(x * x for x in x_transformed)

            denom = (n_pts * sum_xx - sum_x ** 2)
            if denom == 0:
                return 0.0

            slope = (n_pts * sum_xy - sum_x * sum_y) / denom
            intercept = (sum_y - slope * sum_x) / n_pts

            # Compute R^2
            mean_y = sum_y / n_pts
            ss_tot = sum((y - mean_y) ** 2 for y in times)
            ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_transformed, times))

            if ss_tot == 0:
                return 1.0 if complexity_type == "O(1)" else 0.0

            r2 = 1.0 - (ss_res / ss_tot)
            return max(0.0, min(1.0, r2))
        except Exception:
            return 0.0
