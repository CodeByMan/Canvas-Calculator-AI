"""Safe, limited verification for simple arithmetic answers.

The image model still handles equations, diagrams, and abstract concepts. This
module only verifies answers whose expression is an ordinary numeric arithmetic
expression; unsupported expressions are deliberately left for human/model
review rather than being evaluated unsafely.
"""
from __future__ import annotations

import ast
import math
import re
from numbers import Real


_SIMPLE_EXPRESSION = re.compile(r"^[0-9\s+\-*/^().]+$")
_MAX_ABS_VALUE = 1_000_000_000_000.0
_MAX_POWER = 12


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        value = float(node.value)
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = _evaluate(node.operand)
        value = operand if isinstance(node.op, ast.UAdd) else -operand
    elif isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Add):
            value = left + right
        elif isinstance(node.op, ast.Sub):
            value = left - right
        elif isinstance(node.op, ast.Mult):
            value = left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ValueError("division by zero")
            value = left / right
        elif isinstance(node.op, ast.Pow):
            if abs(right) > _MAX_POWER:
                raise ValueError("exponent is too large")
            value = left**right
        else:
            raise ValueError("operator is not supported")
    else:
        raise ValueError("expression contains unsupported syntax")

    if not math.isfinite(value) or abs(value) > _MAX_ABS_VALUE:
        raise ValueError("arithmetic result is outside the safe range")
    return value


def _numeric_result(value) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, Real):
        return float(value)
    if isinstance(value, str):
        try:
            parsed = float(value.strip())
        except ValueError:
            return None
        return parsed if math.isfinite(parsed) else None
    return None


def verify_simple_arithmetic_answers(answers: list[dict]) -> None:
    """Reject a wrong result when an answer is safely verifiable.

    Non-arithmetic expressions are skipped intentionally. The function raises
    ``ValueError`` only when a simple arithmetic answer is parseable and its
    numeric result does not agree with the model response.
    """
    for answer in answers:
        if answer.get("assign"):
            continue

        expression = answer.get("expr")
        if not isinstance(expression, str):
            continue
        normalized = expression.replace("^", "**")
        if not _SIMPLE_EXPRESSION.fullmatch(expression):
            continue

        try:
            tree = ast.parse(normalized, mode="eval")
            expected = _evaluate(tree.body)
        except (SyntaxError, ValueError, TypeError):
            continue

        actual = _numeric_result(answer.get("result"))
        if actual is None or not math.isclose(
            actual,
            expected,
            rel_tol=1e-4,
            abs_tol=1e-6,
        ):
            raise ValueError(
                f"Result does not match simple arithmetic expression: {expression}"
            )
