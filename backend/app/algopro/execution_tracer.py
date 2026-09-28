"""
AlgoPro Execution Tracer
Safely executes target algorithms and collects runtime, peak memory, and operation statistics.
"""
import time
import tracemalloc
import sys
from typing import Dict, Any, Callable

class ExecutionTracer:
    """
    Profiles CPU execution time and peak memory consumption for given callable tasks.
    """

    @staticmethod
    def trace(target_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        tracemalloc.start()
        start_time = time.perf_counter()
        error = None
        result = None

        try:
            result = target_func(*args, **kwargs)
        except Exception as e:
            error = str(e)

        end_time = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        duration_ms = (end_time - start_time) * 1000.0

        return {
            "success": error is None,
            "error": error,
            "execution_time_ms": round(duration_ms, 4),
            "peak_memory_kb": round(peak_mem / 1024.0, 2),
            "current_memory_kb": round(current_mem / 1024.0, 2),
            "result_summary": str(result)[:100] if result is not None else None
        }
