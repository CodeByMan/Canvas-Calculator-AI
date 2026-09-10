import base64
import asyncio
from io import BytesIO
from threading import Lock
import time

from fastapi import APIRouter, HTTPException, Request
from PIL import Image, UnidentifiedImageError

from constants import (
    AI_QUEUE_TIMEOUT_SECONDS,
    MAX_CONCURRENT_AI_REQUESTS,
    MAX_IMAGE_PIXELS,
    MAX_RATE_LIMIT_CLIENTS,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)
from schema import ImageData
from src.calculator.utils import analyze_image
from src.calculator.utils import AIConfigurationError, AIResponseError, AIServiceError

router = APIRouter()

_request_times: dict[str, list[float]] = {}
_request_times_lock = Lock()
_ai_slots = asyncio.Semaphore(MAX_CONCURRENT_AI_REQUESTS)


def _check_rate_limit(client_id: str) -> int | None:
    now = time.monotonic()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    with _request_times_lock:
        timestamps = [timestamp for timestamp in _request_times.get(client_id, []) if timestamp > window_start]
        if len(timestamps) >= RATE_LIMIT_REQUESTS:
            _request_times[client_id] = timestamps
            retry_after = max(1, int(RATE_LIMIT_WINDOW_SECONDS - (now - timestamps[0])))
            return retry_after

        timestamps.append(now)
        _request_times[client_id] = timestamps

        if len(_request_times) > MAX_RATE_LIMIT_CLIENTS:
            oldest_client = min(
                _request_times,
                key=lambda client: _request_times[client][-1] if _request_times[client] else 0,
            )
            if oldest_client != client_id:
                _request_times.pop(oldest_client, None)

    return None


@router.post("")
async def calculate_results(data: ImageData, request: Request):
    client_id = request.client.host if request.client else "unknown"
    retry_after = _check_rate_limit(client_id)
    if retry_after is not None:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )

    try:
        encoded_image = data.image.partition(",")[2]
        image_bytes = BytesIO(base64.b64decode(encoded_image, validate=True))
        image = Image.open(image_bytes)
        width, height = image.size
        if width * height > MAX_IMAGE_PIXELS:
            raise HTTPException(status_code=413, detail="Image dimensions are too large")
        image.load()
    except HTTPException:
        raise
    except (OSError, ValueError, UnidentifiedImageError) as error:
        raise HTTPException(status_code=422, detail="The supplied image could not be processed") from error

    try:
        try:
            await asyncio.wait_for(_ai_slots.acquire(), timeout=AI_QUEUE_TIMEOUT_SECONDS)
        except asyncio.TimeoutError as error:
            raise HTTPException(
                status_code=503,
                detail="AI service is busy. Please try again later.",
                headers={"Retry-After": str(AI_QUEUE_TIMEOUT_SECONDS)},
            ) from error

        try:
            responses = await asyncio.to_thread(
                analyze_image,
                image,
                dict_of_vars=data.dict_of_vars,
            )
        finally:
            _ai_slots.release()
    except AIConfigurationError as error:
        raise HTTPException(status_code=503, detail="AI service is not configured") from error
    except (AIResponseError, AIServiceError) as error:
        raise HTTPException(status_code=502, detail="AI analysis failed") from error

    return {
        "message": "Image processed",
        "data": responses,
        "status": "success",
        "success": True,
    }
