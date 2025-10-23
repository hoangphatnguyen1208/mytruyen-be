"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

import fastapi
from fastapi import HTTPException

from app.utilities.messages.exceptions.http.exc_details import (
    http_404_chapter_details,
    http_404_email_details,
    http_404_id_details,
    http_404_username_details,
    http_404_book_details,
    http_404_genre_details,
    http_404_chapter_content_details,
    http_404_tag_details,
)


def http_404_exc_email_not_found_request(email: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_email_details(email=email),
    )


def http_404_exc_id_not_found_request(id: int):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(id=id),
    )


def http_404_exc_username_not_found_request(username: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_username_details(username=username),
    )


def http_404_exc_book_not_found_request(string: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_book_details(string=string),
    )


def http_404_exc_genre_not_found(genre_id: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_genre_details(genre_id=genre_id),
    )

def http_404_exc_chapter_not_found_request(chapter_id: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_chapter_details(chapter_id=chapter_id),
    )

def http_404_exc_chapter_content_not_found_request(chapter_id: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_chapter_content_details(chapter_id=chapter_id),
    )

def http_404_exc_tag_not_found_request(string: str):
    raise HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_tag_details(string=string),
    )
