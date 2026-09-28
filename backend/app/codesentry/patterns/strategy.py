"""
Pattern 3: Strategy Pattern (GoF Behavioral)
Defines an interchangeable family of inspection algorithms.
Enables pluggable rules without modifying the analyzer pipeline.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .visitor import ASTMetricsVisitor
from .singleton import ConfigurationManager

class AnalysisStrategy(ABC):
    """Abstract Strategy interface for all code quality and security inspection rules."""
    @abstractmethod
    def evaluate(self, code: str, visitor_metrics: ASTMetricsVisitor) -> Dict[str, Any]:
        pass


class ComplexityStrategy(AnalysisStrategy):
    """Evaluates cyclomatic complexity and function nesting depth."""
    def evaluate(self, code: str, visitor: ASTMetricsVisitor) -> Dict[str, Any]:
        config = ConfigurationManager()
        max_allowed_cc = config.get("max_cyclomatic_complexity", 10)
        violations = []
        total_cc = 0

        for func in visitor.function_details:
            total_cc += func["cyclomatic_complexity"]
            if func["cyclomatic_complexity"] > max_allowed_cc:
                violations.append({
                    "severity": "HIGH",
                    "type": "HighCyclomaticComplexity",
                    "line": func["line"],
                    "function": func["name"],
                    "value": func["cyclomatic_complexity"],
                    "threshold": max_allowed_cc,
                    "message": f"Function '{func['name']}' has high cyclomatic complexity ({func['cyclomatic_complexity']} > {max_allowed_cc}). Refactor into smaller sub-methods."
                })
            if func["nesting_depth"] > config.get("max_nesting_depth", 3):
                violations.append({
                    "severity": "MEDIUM",
                    "type": "DeepNesting",
                    "line": func["line"],
                    "function": func["name"],
                    "value": func["nesting_depth"],
                    "threshold": config.get("max_nesting_depth", 3),
                    "message": f"Function '{func['name']}' exceeds safe nesting depth ({func['nesting_depth']} levels)."
                })

        avg_cc = round(total_cc / max(1, len(visitor.function_details)), 2)
        score = max(0, 100 - (len(violations) * 15))
        return {
            "name": "Complexity Analysis",
            "score": score,
            "average_complexity": avg_cc,
            "violations": violations
        }


class SecurityVulnerabilityStrategy(AnalysisStrategy):
    """Scans for dangerous functions, execution calls, and SQL injection risks."""
    def evaluate(self, code: str, visitor: ASTMetricsVisitor) -> Dict[str, Any]:
        violations = []

        for item in visitor.dangerous_calls:
            violations.append({
                "severity": "CRITICAL",
                "type": "DangerousExecutionCall",
                "line": item["line"],
                "message": item["description"],
                "recommendation": "Avoid eval() or os.system(); use safe parameterized alternatives."
            })

        for item in visitor.sql_injection_patterns:
            violations.append({
                "severity": "CRITICAL",
                "type": "SQLInjectionRisk",
                "line": item["line"],
                "message": item["description"],
                "recommendation": "Use parameterized queries or ORM models instead of string concatenation."
            })

        # Check for hardcoded secret patterns
        lines = code.splitlines()
        for idx, line in enumerate(lines, 1):
            lower_line = line.lower()
            if any(k in lower_line for k in ["password =", "secret_key =", "jwt_secret =", "api_key ="]):
                if not any(placeholder in lower_line for placeholder in ["os.getenv", "env", "config"]):
                    violations.append({
                        "severity": "HIGH",
                        "type": "HardcodedSecret",
                        "line": idx,
                        "message": "Potential hardcoded secret or credential detected in source code.",
                        "recommendation": "Store credentials in environment variables."
                    })

        penalty = sum(25 if v["severity"] == "CRITICAL" else 15 for v in violations)
        score = max(0, 100 - penalty)
        return {
            "name": "Security & Vulnerability Audit",
            "score": score,
            "violations": violations
        }


class CodeSmellStrategy(AnalysisStrategy):
    """Detects function bloat, parameter list sprawl, and bad naming practices."""
    def evaluate(self, code: str, visitor: ASTMetricsVisitor) -> Dict[str, Any]:
        config = ConfigurationManager()
        max_lines = config.get("max_function_lines", 35)
        max_params = config.get("max_parameters_per_func", 5)
        violations = []

        for func in visitor.function_details:
            if func["length"] > max_lines:
                violations.append({
                    "severity": "LOW",
                    "type": "LongFunction",
                    "line": func["line"],
                    "function": func["name"],
                    "value": func["length"],
                    "threshold": max_lines,
                    "message": f"Function '{func['name']}' is {func['length']} lines long (limit {max_lines}). Consider splitting into focused functions."
                })
            if func["param_count"] > max_params:
                violations.append({
                    "severity": "MEDIUM",
                    "type": "TooManyParameters",
                    "line": func["line"],
                    "function": func["name"],
                    "value": func["param_count"],
                    "threshold": max_params,
                    "message": f"Function '{func['name']}' takes {func['param_count']} parameters (limit {max_params}). Encapsulate arguments into a dataclass/object."
                })

        score = max(0, 100 - (len(violations) * 10))
        return {
            "name": "Code Smells & Hygiene",
            "score": score,
            "violations": violations
        }
