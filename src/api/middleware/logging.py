import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):
    """Middleware для логирования"""

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start = time.time()
    client_ip = request.get("x-forwarded-for", request.client.host)

    logger.info(f"UUID [{request_id}] {request.method} {request.url.path} from {client_ip}")
    response = await call_next(request)

    process_time_ms = (time.time() - start) * 1000

    logger.info(f"UUID [{request_id}] {request.method} {request.url.path} "
                f"status={response.status_code} time={process_time_ms:.2f}ms")

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time_ms:.2f}ms"

    return response