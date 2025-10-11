"""
The HyperText Transfer Protocol (HTTP) 400 Bad Request response status code indicates that the server
cannot or will not process the request due to something that is perceivedto be a client error
(for example, malformed request syntax, invalid request message framing, or deceptive request routing).
"""

import fastapi
from fastapi.responses import JSONResponse
from app.schema.response import Response

from app.utilities.messages.exceptions.http.exc_details import (
    http_400_email_details,
    http_400_sigin_credentials_details,
    http_400_signup_credentials_details,
    http_400_username_details,
    http_400_book_details,
)


def http_exc_400_credentials_bad_signup_request() -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content=Response(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            message=http_400_signup_credentials_details(),
            success=False,
        ).model_dump()
    )


def http_exc_400_credentials_bad_signin_request() -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content=Response(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            message=http_400_sigin_credentials_details(),
            success=False,
        ).model_dump()
    )


def http_400_exc_bad_username_request(username: str) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content=Response(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            message=http_400_username_details(username=username),
            success=False,
        ).model_dump()
    )


def http_400_exc_bad_email_request(email: str) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content=Response(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            message=http_400_email_details(email=email),
            success=False,
        ).model_dump()
    )


def http_400_exc_bad_book_request(slug: str) -> JSONResponse:
    return JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content=Response(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            message=http_400_book_details(string=slug),
            success=False,
        ).model_dump()
    )
