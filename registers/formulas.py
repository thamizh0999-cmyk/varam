import ast
import operator
import re
from decimal import Decimal, InvalidOperation


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_formula(formula, values):
    """
    Safely evaluate arithmetic using numeric register field keys.
    Supported: +, -, *, /, unary +/- and parentheses.
    """
    if not formula or len(formula) > 255:
        raise ValueError("Formula is empty or too long.")

    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid formula syntax.") from exc

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))

        if isinstance(node, ast.Name):
            key = node.id
            raw = values.get(key, "")
            if raw in ("", None, False):
                raise ValueError(f"Missing numeric value for '{key}'.")
            try:
                number = Decimal(str(raw))
            except (InvalidOperation, TypeError):
                raise ValueError(f"'{key}' must contain a number.")
            if not number.is_finite():
                raise ValueError(f"'{key}' must be finite.")
            return number

        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
            left = calculate(node.left)
            right = calculate(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero is not allowed.")
            result = _ALLOWED_OPERATORS[type(node.op)](left, right)
            if not result.is_finite():
                raise ValueError("Formula result must be finite.")
            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
            result = _ALLOWED_OPERATORS[type(node.op)](calculate(node.operand))
            if not result.is_finite():
                raise ValueError("Formula result must be finite.")
            return result

        raise ValueError("Only arithmetic operators and numeric field keys are allowed.")

    result = calculate(tree)
    if not result.is_finite():
        raise ValueError("Formula result must be finite.")
    return result
