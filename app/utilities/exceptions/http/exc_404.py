"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

import fastapi
from fastapi.responses import JSONResponse
from app.schema.response import Response

from app.utilities.messages.exceptions.http.exc_details import (
    http_404_email_details,
    http_404_id_details,
    http_404_username_details,
    http_404_book_details,
)


def http_404_exc_email_not_found_request(email: str) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content=Response(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            message=http_404_email_details(email=email),
            success=False,
        ).model_dump()
    )


def http_404_exc_id_not_found_request(id: int) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content=Response(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            message=http_404_id_details(id=id),
            success=False,
        ).model_dump()
    )


def http_404_exc_username_not_found_request(username: str) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content=Response(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            message=http_404_username_details(username=username),
            success=False,
        ).model_dump()
    )


def http_404_exc_book_not_found_request(string: str) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content=Response(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            message=http_404_book_details(string=string),
            success=False,
        ).model_dump()
    )
