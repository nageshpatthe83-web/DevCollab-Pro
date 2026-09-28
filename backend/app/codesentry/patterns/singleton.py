"""
Pattern 1: Singleton Pattern (GoF Creational)
Thread-safe Configuration Manager for CodeSentry analysis thresholds and global settings.
"""
import threading
from typing import Dict, Any

class ConfigurationManager:
    """
    Thread-safe Singleton Configuration Manager.
    Ensures that analyzer rules, severity weights, and threshold limits are globally consistent.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigurationManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        self._config: Dict[str, Any] = {
            "max_cyclomatic_complexity": 10,
            "max_function_lines": 35,
            "max_parameters_per_func": 5,
            "max_nesting_depth": 3,
            "enable_security_checks": True,
            "enable_smell_detection": True,
            "weights": {
                "complexity": 0.30,
                "security": 0.35,
                "code_smells": 0.20,
                "maintainability": 0.15
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        return dict(self._config)
