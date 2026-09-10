from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "127.0.0.1").strip()
PORT = int(os.getenv("PORT", "8000"))
ENV = os.getenv("ENV", "dev").strip().lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def _read_frontend_origins() -> list[str]:
    origins = [
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]
    if not origins:
        raise RuntimeError("FRONTEND_ORIGINS must contain at least one origin")

    for origin in origins:
        parsed = urlparse(origin)
        if origin == "*" or parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise RuntimeError("FRONTEND_ORIGINS must contain explicit HTTP(S) origins")

    return origins


FRONTEND_ORIGINS = _read_frontend_origins()
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_IMAGE_BASE64_CHARS = 12_000_000
MAX_IMAGE_PIXELS = 16_000_000
MAX_VARIABLES = 50
MAX_VARIABLE_KEY_LENGTH = 64
MAX_VARIABLE_VALUE_LENGTH = 256
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW_SECONDS = 60
MAX_RATE_LIMIT_CLIENTS = 1024
MAX_CONCURRENT_AI_REQUESTS = 4
AI_QUEUE_TIMEOUT_SECONDS = 5
MAX_AI_RESPONSE_CHARS = 20_000
MAX_AI_ANSWERS = 50
MAX_RESULT_TEXT_LENGTH = 2_000
