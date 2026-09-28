"""
CodeSentry: Automated Code Quality and Security Analyzer
Part of DevCollab Pro (OOP Pillar)
Demonstrating 5 Gang of Four (GoF) Design Patterns:
1. Strategy Pattern
2. Visitor Pattern
3. Factory Pattern
4. Observer Pattern
5. Singleton Pattern
"""
from .analyzer_service import CodeSentryAnalyzer
from .patterns.singleton import ConfigurationManager
from .patterns.factory import AnalyzerFactory

__all__ = ["CodeSentryAnalyzer", "ConfigurationManager", "AnalyzerFactory"]
