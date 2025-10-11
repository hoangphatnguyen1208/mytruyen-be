"""
The HyperText Transfer Protocol (HTTP) 401 Unauthorized response status code indicates that the client
request has not been completed because it lacks valid authentication credentials for the requested resource.
"""

import fastapi
from fastapi.responses import JSONResponse
from app.schema.response import Response

from app.utilities.messages.exceptions.http.exc_details import http_401_unauthorized_details


def http_exc_401_cunauthorized_request() -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        content=Response(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            message=http_401_unauthorized_details(),
            success=False,
        ).model_dump()
    )
