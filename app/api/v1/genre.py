import uuid
from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.models import Genre
from app.api.deps import SessionDep, CurrentAdmin
from app.schema.genre import GenreCreate, GenreUpdate, GenrePublic
from app.crud import genre as genre_crud

from app.utilities.exceptions.http.exc_404 import http_404_exc_genre_not_found
from app.utilities.exceptions.http.exc_400 import http_exc_400_genre_bad_request

router = APIRouter(prefix="/genres", tags=["Genre"])

@router.post("", response_model=GenrePublic, status_code=201)
async def create_genre(session: SessionDep, genre_in: GenreCreate, current_admin: CurrentAdmin):
    existing_genre_slug = await genre_crud.get_genre_by_slug(session, genre_in.slug)
    if existing_genre_slug:
        raise http_exc_400_genre_bad_request(slug=genre_in.slug)
    return await genre_crud.create_genre(session, genre_in)

@router.get("", response_model=list[GenrePublic])
async def read_genres(session: SessionDep):
    return await genre_crud.get_genres(session)

@router.get("/{slug}", response_model=GenrePublic)
async def read_genre(session: SessionDep, slug: str):
    genre_db =  await genre_crud.get_genre_by_slug(session, slug)
    if not genre_db:
        raise http_404_exc_genre_not_found(genre_id=slug)
    return genre_db

@router.put("/update/{genre_id}", response_model=GenrePublic)
async def update_genre(session: SessionDep, genre_id: int, genre_in: GenreUpdate, current_admin: CurrentAdmin):
    genre_db = await genre_crud.get_genre_by_id(session, genre_id)
    if not genre_db:
        raise http_404_exc_genre_not_found(genre_id=genre_id)
    genre = await genre_crud.update_genre(session, genre_id, genre_in)
    return genre

@router.delete("/delete/{genre_id}", response_model=dict)
async def delete_genre(session: SessionDep, genre_id: int, current_admin: CurrentAdmin):
    print(genre_id)
    genre_db = await genre_crud.get_genre_by_id(session, genre_id)
    if not genre_db:
        raise http_404_exc_genre_not_found(genre_id=genre_id)
    await genre_crud.delete_genre(session, genre_id)
    return {"message": "Genre deleted successfully"}
