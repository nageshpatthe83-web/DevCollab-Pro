"""
Pattern 4: Observer Pattern (GoF Behavioral)
Event-driven notification system reporting analysis progress, completed rule evaluations,
and audit summaries to listening subscribers.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AnalysisObserver(ABC):
    """Observer interface for CodeSentry analysis events."""
    @abstractmethod
    def on_event(self, event_type: str, data: Dict[str, Any]) -> None:
        pass


class MetricsCollectorObserver(AnalysisObserver):
    """Gathers event telemetry for real-time reporting."""
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def on_event(self, event_type: str, data: Dict[str, Any]) -> None:
        self.events.append({
            "event": event_type,
            "data": data
        })

    def get_summary(self) -> List[Dict[str, Any]]:
        return self.events


class AnalysisSubject:
    """Subject maintaining a list of active observers."""
    def __init__(self):
        self._observers: List[AnalysisObserver] = []

    def attach(self, observer: AnalysisObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: AnalysisObserver) -> None:
        self._observers.remove(observer)

    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.on_event(event_type, data)
