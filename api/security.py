from collections import defaultdict, deque
from time import monotonic

from fastapi import (
    Header,
    HTTPException,
    Request
)

from config import settings


request_history = defaultdict(deque)


async def verify_api_access(
    request: Request,
    x_api_key: str | None = Header(default=None)
):

    if settings.API_ACCESS_KEY:

        if x_api_key != settings.API_ACCESS_KEY:

            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )

    client = request.client

    client_id = (
        client.host if client else "unknown"
    )

    now = monotonic()

    history = request_history[client_id]

    while history and now - history[0] >= 60:

        history.popleft()

    if len(history) >= settings.MAX_REQUESTS_PER_MINUTE:

        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

    history.append(now)
