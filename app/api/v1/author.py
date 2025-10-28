from fastapi import APIRouter, status
from app.api.deps import CurrentAdmin, CurrentUser, SessionDep

from app.crud import author as crud_author
from app.schema.author import AuthorCreate, AuthorPublic, AuthorUpdate

from app.utilities.exceptions.http.exc_400 import http_exc_400_author_bad_request
from app.utilities.exceptions.http.exc_404 import http_exc_404_author_not_found_request
import uuid


router = APIRouter(prefix="/authors", tags=["author"])

@router.post("", response_model=AuthorPublic, status_code=status.HTTP_201_CREATED)
async def create_author(session: SessionDep, current_admin: CurrentAdmin, author_in: AuthorCreate):
    existing_author = await crud_author.get_author_by_name(session, author_in.name)
    if existing_author:
        raise http_exc_400_author_bad_request(string=author_in.name)
    db_author = await crud_author.create_author(session, author_in)
    return db_author

@router.get("", response_model=list[AuthorPublic])
async def get_authors(session: SessionDep):
    authors = await crud_author.get_authors(session)
    return authors

@router.get("/{name}", response_model=AuthorPublic)
async def get_author_by_name(session: SessionDep, name: str):
    author = await crud_author.get_author_by_name(session, name)
    if not author:
        raise http_exc_404_author_not_found_request(string=name)
    return author

@router.patch("/{author_id}", response_model=AuthorPublic)
async def update_author(session: SessionDep, author_id: uuid.UUID, author_in: AuthorUpdate, current_admin: CurrentAdmin):
    existing_author = await crud_author.get_author_by_id(session, author_id)
    if not existing_author:
        raise http_exc_404_author_not_found_request(string=str(author_id))
    updated_author = await crud_author.update_author(session, author_id, author_in)
    return updated_author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(session: SessionDep, author_id: uuid.UUID, current_admin: CurrentAdmin):
    existing_author = await crud_author.get_author_by_id(session, author_id)
    if not existing_author:
        raise http_exc_404_author_not_found_request(string=str(author_id))
    await crud_author.delete_author(session, author_id)
