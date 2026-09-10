import unittest

from src.calculator.verification import verify_simple_arithmetic_answers


class ArithmeticVerificationTests(unittest.TestCase):
    def test_accepts_correct_numeric_expression(self):
        verify_simple_arithmetic_answers([
            {"expr": "2 + 3 * 4", "result": "14", "assign": False}
        ])

    def test_rejects_incorrect_numeric_expression(self):
        with self.assertRaises(ValueError):
            verify_simple_arithmetic_answers([
                {"expr": "2 + 3 * 4", "result": "15", "assign": False}
            ])

    def test_skips_equations_and_conceptual_answers(self):
        verify_simple_arithmetic_answers([
            {"expr": "x", "result": 4, "assign": True},
            {"expr": "x + 1 = 2", "result": "x is 1", "assign": False},
            {"expr": "a drawing of a cricket match", "result": "sport", "assign": False},
        ])


if __name__ == "__main__":
    unittest.main()
