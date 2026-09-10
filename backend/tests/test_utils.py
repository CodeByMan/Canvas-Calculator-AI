import unittest

from constants import MAX_AI_ANSWERS, MAX_AI_RESPONSE_CHARS
from src.calculator.utils import AIResponseError, parse_model_answers


class ModelResponseValidationTests(unittest.TestCase):
    def test_parses_valid_model_response(self):
        answers = parse_model_answers("[{'expr': '2 + 2', 'result': 4}]")

        self.assertEqual(
            answers,
            [{"expr": "2 + 2", "result": 4, "assign": False}],
        )

    def test_rejects_invalid_model_response(self):
        with self.assertRaises(AIResponseError):
            parse_model_answers("not structured data")

    def test_rejects_unexpected_fields(self):
        with self.assertRaises(AIResponseError):
            parse_model_answers("[{'expr': '2 + 2', 'result': 4, 'extra': 'value'}]")

    def test_rejects_oversized_response(self):
        with self.assertRaises(AIResponseError):
            parse_model_answers("x" * (MAX_AI_RESPONSE_CHARS + 1))

    def test_rejects_too_many_answers(self):
        answers = str([{"expr": str(index), "result": index} for index in range(MAX_AI_ANSWERS + 1)])

        with self.assertRaises(AIResponseError):
            parse_model_answers(answers)


if __name__ == "__main__":
    unittest.main()
