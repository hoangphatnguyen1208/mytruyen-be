"""
The HTTP 403 Forbidden response status code indicates that the server understands the request but refuses to authorize it.
"""

import fastapi
from fastapi.responses import JSONResponse
from app.schema.response import Response

from app.utilities.messages.exceptions.http.exc_details import http_403_forbidden_details


def http_403_exc_forbidden_request() -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        content=Response(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            message=http_403_forbidden_details(),
            success=False,
        ).model_dump()
    )
