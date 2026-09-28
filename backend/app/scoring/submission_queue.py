"""
Concurrent Submission Queue & Worker Dispatcher (DSA Topic)
Simulates handling peak concurrent hackathon submissions without server bottlenecks.
"""
import queue
import threading
import time
from typing import Dict, List, Any, Optional

class SubmissionTask:
    def __init__(self, submission_id: str, team_id: str, code: str, language: str):
        self.submission_id = submission_id
        self.team_id = team_id
        self.code = code
        self.language = language
        self.submitted_at = time.time()
        self.status = "QUEUED"
        self.result: Optional[Dict[str, Any]] = None


class SubmissionQueue:
    def __init__(self, num_workers: int = 2):
        self._queue = queue.Queue()
        self._tasks: Dict[str, SubmissionTask] = {}
        self.num_workers = num_workers

    def enqueue(self, task: SubmissionTask) -> str:
        self._tasks[task.submission_id] = task
        self._queue.put(task)
        return task.submission_id

    def get_task_status(self, submission_id: str) -> Optional[Dict[str, Any]]:
        task = self._tasks.get(submission_id)
        if not task:
            return None
        return {
            "submission_id": task.submission_id,
            "team_id": task.team_id,
            "status": task.status,
            "submitted_at": task.submitted_at,
            "result": task.result
        }

    def process_next_sync(self) -> Optional[SubmissionTask]:
        """Synchronously processes one task from queue for testing/demo."""
        try:
            task = self._queue.get_nowait()
            task.status = "PROCESSING"
            # Simulate evaluation
            from ..codesentry.analyzer_service import CodeSentryAnalyzer
            from ..algopro.profiler_service import ProfilerService

            analysis = CodeSentryAnalyzer().run_full_analysis(task.code)
            perf = ProfilerService.profile_algorithm("TaskAlgorithm")

            task.result = {
                "quality": analysis,
                "performance": perf,
                "verdict": "ACCEPTED"
            }
            task.status = "COMPLETED"
            self._queue.task_done()
            return task
        except queue.Empty:
            return None
