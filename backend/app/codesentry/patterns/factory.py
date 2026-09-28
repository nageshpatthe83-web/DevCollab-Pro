"""
Pattern 5: Factory Pattern (GoF Creational)
Instantiates appropriate language-specific code analyzers based on file extension.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLanguageAnalyzer(ABC):
    @abstractmethod
    def analyze(self, code: str) -> Dict[str, Any]:
        pass


class PythonLanguageAnalyzer(BaseLanguageAnalyzer):
    def analyze(self, code: str) -> Dict[str, Any]:
        from ..analyzer_service import CodeSentryAnalyzer
        return CodeSentryAnalyzer().run_full_analysis(code, filename="code.py")


class GenericLanguageAnalyzer(BaseLanguageAnalyzer):
    def analyze(self, code: str) -> Dict[str, Any]:
        lines = code.splitlines()
        loc = len(lines)
        return {
            "language": "generic",
            "loc": loc,
            "code_quality_score": 85.0,
            "status": "Basic structural scan performed (Full AST supported for Python)."
        }


class AnalyzerFactory:
    """Factory creating the appropriate analyzer instance."""
    @staticmethod
    def get_analyzer(file_extension: str) -> BaseLanguageAnalyzer:
        ext = file_extension.lower().strip('.')
        if ext in {"py", "python"}:
            return PythonLanguageAnalyzer()
        else:
            return GenericLanguageAnalyzer()
