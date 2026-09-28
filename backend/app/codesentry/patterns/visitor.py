"""
Pattern 2: Visitor Pattern (GoF Behavioral)
AST Visitor traversing syntax trees to gather metrics, detect code smells,
and flag dangerous function calls / SQL injection vulnerabilities.
"""
import ast
from typing import List, Dict, Any

class ASTMetricsVisitor(ast.NodeVisitor):
    """
    Traverses the Abstract Syntax Tree (AST) of the uploaded source code.
    Records branching decisions, function definitions, loop structures, and calls.
    """
    def __init__(self):
        self.functions_count = 0
        self.classes_count = 0
        self.decision_points = 0
        self.loop_count = 0
        self.function_details: List[Dict[str, Any]] = []
        self.dangerous_calls: List[Dict[str, Any]] = []
        self.sql_injection_patterns: List[Dict[str, Any]] = []
        self.current_function: Optional[str] = None
        self.current_func_depth = 0
        self.max_nesting_observed = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions_count += 1
        func_name = node.name
        start_line = node.lineno
        end_line = getattr(node, 'end_lineno', start_line)
        length = end_line - start_line + 1
        args_count = len(node.args.args)

        func_visitor = FunctionComplexityVisitor()
        for stmt in node.body:
            func_visitor.visit(stmt)

        self.function_details.append({
            "name": func_name,
            "line": start_line,
            "length": length,
            "param_count": args_count,
            "cyclomatic_complexity": func_visitor.complexity + 1,
            "nesting_depth": func_visitor.max_depth
        })

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.functions_count += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes_count += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        self.decision_points += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.decision_points += 1
        self.loop_count += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.decision_points += 1
        self.loop_count += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Detect security risks: eval, exec, os.system, raw SQL queries
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in {"eval", "exec", "__import__", "system", "popen"}:
            self.dangerous_calls.append({
                "function": func_name,
                "line": node.lineno,
                "description": f"Dangerous dynamic execution call '{func_name}' detected."
            })

        # Detect SQL string concatenation vulnerabilities
        if func_name in {"execute", "raw", "select"}:
            for arg in node.args:
                if isinstance(arg, ast.BinOp) and isinstance(arg.op, (ast.Add, ast.Mod)):
                    self.sql_injection_patterns.append({
                        "line": node.lineno,
                        "description": "Possible SQL injection: SQL query dynamically formatted via concatenation/interpolation."
                    })

        self.generic_visit(node)


class FunctionComplexityVisitor(ast.NodeVisitor):
    """Auxiliary visitor to calculate local function cyclomatic complexity and nesting."""
    def __init__(self):
        self.complexity = 0
        self.depth = 0
        self.max_depth = 0

    def visit_If(self, node):
        self.complexity += 1
        self._visit_branch(node)

    def visit_For(self, node):
        self.complexity += 1
        self._visit_branch(node)

    def visit_While(self, node):
        self.complexity += 1
        self._visit_branch(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self._visit_branch(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def _visit_branch(self, node):
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)
        self.generic_visit(node)
        self.depth -= 1
