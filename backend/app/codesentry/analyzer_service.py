"""
CodeSentry Unified Analyzer Service
Orchestrates AST parsing, 5 GoF design patterns, metric calculations,
and composite Code Quality scoring (0-100).
"""
import ast
import math
from typing import Dict, List, Any
from .patterns.visitor import ASTMetricsVisitor
from .patterns.strategy import ComplexityStrategy, SecurityVulnerabilityStrategy, CodeSmellStrategy
from .patterns.observer import AnalysisSubject, MetricsCollectorObserver
from .patterns.singleton import ConfigurationManager

class CodeSentryAnalyzer(AnalysisSubject):
    def __init__(self):
        super().__init__()
        self.config = ConfigurationManager()
        self.strategies = [
            ComplexityStrategy(),
            SecurityVulnerabilityStrategy(),
            CodeSmellStrategy()
        ]

    def run_full_analysis(self, source_code: str, filename: str = "source.py") -> Dict[str, Any]:
        collector = MetricsCollectorObserver()
        self.attach(collector)

        self.notify("ANALYSIS_START", {"filename": filename, "chars": len(source_code)})

        # 1. AST Parsing via Visitor Pattern
        visitor = ASTMetricsVisitor()
        parse_error = None
        try:
            tree = ast.parse(source_code)
            visitor.visit(tree)
        except SyntaxError as e:
            parse_error = f"Syntax Error at line {e.lineno}: {e.msg}"

        if parse_error:
            return {
                "success": False,
                "error": parse_error,
                "code_quality_score": 0.0,
                "composite_grade": "F (Syntax Error)",
                "violations": [{"severity": "CRITICAL", "type": "SyntaxError", "message": parse_error}]
            }

        # 2. Execute Pluggable Rules via Strategy Pattern
        strategy_results = []
        all_violations = []

        for strat in self.strategies:
            res = strat.evaluate(source_code, visitor)
            strategy_results.append(res)
            all_violations.extend(res.get("violations", []))
            self.notify("RULE_EVALUATED", {"rule": res["name"], "score": res["score"]})

        # 3. Calculate Maintainability Index (MI)
        loc = len([l for l in source_code.splitlines() if l.strip()])
        avg_cc = max(1.0, strategy_results[0].get("average_complexity", 1.0))
        # Standard software engineering Maintainability Index formula (scaled 0-100)
        halstead_volume = max(1.0, loc * math.log2(max(2, loc)))
        raw_mi = 171 - (5.2 * math.log(halstead_volume)) - (0.23 * avg_cc) - (16.2 * math.log(max(1, loc)))
        normalized_mi = max(0.0, min(100.0, round((raw_mi / 171.0) * 100, 2)))

        # 4. Composite Quality Score
        weights = self.config.get("weights", {})
        comp_score = (
            strategy_results[0]["score"] * weights.get("complexity", 0.30) +
            strategy_results[1]["score"] * weights.get("security", 0.35) +
            strategy_results[2]["score"] * weights.get("code_smells", 0.20) +
            normalized_mi * weights.get("maintainability", 0.15)
        )
        final_quality = round(max(0.0, min(100.0, comp_score)), 2)

        # Grade assignment
        if final_quality >= 90:
            grade = "A+ (Excellent)"
        elif final_quality >= 80:
            grade = "A (High Quality)"
        elif final_quality >= 70:
            grade = "B (Good / Acceptable)"
        elif final_quality >= 50:
            grade = "C (Needs Refactoring)"
        else:
            grade = "D (Poor / High Risk)"

        self.notify("ANALYSIS_COMPLETE", {"score": final_quality, "grade": grade})

        return {
            "success": True,
            "code_quality_score": final_quality,
            "composite_grade": grade,
            "maintainability_index": normalized_mi,
            "lines_of_code": loc,
            "functions_count": visitor.functions_count,
            "classes_count": visitor.classes_count,
            "decision_points": visitor.decision_points,
            "component_breakdown": {
                "complexity": strategy_results[0]["score"],
                "security": strategy_results[1]["score"],
                "code_smells": strategy_results[2]["score"],
                "maintainability": normalized_mi
            },
            "violations": all_violations,
            "functions_detail": visitor.function_details,
            "patterns_demonstrated": [
                "Singleton Pattern (ConfigurationManager)",
                "Visitor Pattern (ASTMetricsVisitor)",
                "Strategy Pattern (Complexity, Security, CodeSmell strategies)",
                "Observer Pattern (AnalysisSubject / MetricsCollectorObserver)",
                "Factory Pattern (AnalyzerFactory)"
            ]
        }
