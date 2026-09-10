import unittest
import uuid

from constants import RATE_LIMIT_REQUESTS
from src.calculator.route import _check_rate_limit


class RateLimitTests(unittest.TestCase):
    def test_rate_limit_rejects_requests_after_threshold(self):
        client_id = f"test-{uuid.uuid4()}"

        for _ in range(RATE_LIMIT_REQUESTS):
            self.assertIsNone(_check_rate_limit(client_id))

        retry_after = _check_rate_limit(client_id)

        self.assertIsNotNone(retry_after)
        self.assertGreaterEqual(retry_after, 1)


if __name__ == "__main__":
    unittest.main()
