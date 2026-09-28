import pytest
from app.codesentry.analyzer_service import CodeSentryAnalyzer
from app.codesentry.patterns.singleton import ConfigurationManager
from app.codesentry.patterns.factory import AnalyzerFactory

def test_singleton_configuration():
    c1 = ConfigurationManager()
    c2 = ConfigurationManager()
    assert c1 is c2
    c1.set("test_key", 999)
    assert c2.get("test_key") == 999

def test_ast_analysis_clean_code():
    code = """
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total += n
    return total
"""
    analyzer = CodeSentryAnalyzer()
    res = analyzer.run_full_analysis(code)
    assert res["success"] is True
    assert res["code_quality_score"] > 80.0
    assert len(res["patterns_demonstrated"]) == 5

def test_ast_analysis_security_flags():
    bad_code = """
def unsafe_run(user_input):
    eval(user_input)
    query = "SELECT * FROM users WHERE id = " + user_input
    execute(query)
"""
    analyzer = CodeSentryAnalyzer()
    res = analyzer.run_full_analysis(bad_code)
    assert res["success"] is True
    assert any(v["severity"] == "CRITICAL" for v in res["violations"])
    assert res["component_breakdown"]["security"] < 80.0

def test_factory_pattern():
    analyzer = AnalyzerFactory.get_analyzer("test.py")
    assert analyzer is not None
