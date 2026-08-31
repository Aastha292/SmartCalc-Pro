"""Safe scientific expression evaluation for SmartCalc Pro."""

import ast
import math
import operator
import re


class CalculationError(ValueError):
    """Raised when an expression is invalid or unsafe."""


class CalculationEngine:
    def evaluate(self, expression, angle_mode="DEG"):
        normalized = self._normalize(expression)
        try:
            tree = ast.parse(normalized, mode="eval")
            result = self._evaluate_node(tree.body, angle_mode)
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError) as error:
            raise CalculationError(str(error)) from error

        if not math.isfinite(float(result)):
            raise CalculationError("Result is not finite")
        return self._format_number(result)

    def _normalize(self, expression):
        expression = str(expression).strip()
        if not expression:
            raise CalculationError("Expression is empty")
        expression = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        expression = re.sub(r"(\d+(?:\.\d+)?)!", r"factorial(\1)", expression)
        if "!" in expression:
            raise CalculationError("Factorial requires a non-negative integer")
        return expression.replace("^", "**")

    def _evaluate_node(self, node, angle_mode):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in {ast.UAdd, ast.USub}:
            value = self._evaluate_node(node.operand, angle_mode)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left = self._evaluate_node(node.left, angle_mode)
            right = self._evaluate_node(node.right, angle_mode)
            return _OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.Name) and node.id in {"pi", "e"}:
            return {"pi": math.pi, "e": math.e}[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = node.func.id
            if function not in _FUNCTIONS or len(node.args) != 1 or node.keywords:
                raise CalculationError("Unsupported function")
            value = self._evaluate_node(node.args[0], angle_mode)
            return _FUNCTIONS[function](value, angle_mode)
        raise CalculationError("Unsupported expression")

    @staticmethod
    def _format_number(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return round(value, 10) if isinstance(value, float) else value


def _trig(function):
    def wrapped(value, angle_mode):
        return function(math.radians(value)) if angle_mode == "DEG" else function(value)
    return wrapped


_FUNCTIONS = {
    "sin": _trig(math.sin),
    "cos": _trig(math.cos),
    "tan": _trig(math.tan),
    "sqrt": lambda value, _: math.sqrt(value),
    "log": lambda value, _: math.log10(value),
    "ln": lambda value, _: math.log(value),
    "factorial": lambda value, _: math.factorial(value) if value >= 0 and float(value).is_integer() else (_ for _ in ()).throw(ValueError("Factorial requires a non-negative integer")),
}

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}