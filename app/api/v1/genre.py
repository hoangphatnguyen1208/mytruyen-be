from fastapi import APIRouter

from app.models import Genre
from app.api.deps import SessionDep
from app.schema.genre import GenreCreate, GenreUpdate, GenrePublic
from app.crud import genre as genre_crud

router = APIRouter(prefix="/genre", tags=["Genre"])

@router.post("", response_model=GenrePublic)
async def create_genre(session: SessionDep, genre_in: GenreCreate):
    return await genre_crud.create_genre(session, genre_in)

@router.get("s", response_model=list[GenrePublic])
async def read_genres(session: SessionDep):
    return await genre_crud.get_genres(session)

@router.get("/{slug}", response_model=GenrePublic)
async def read_genre(session: SessionDep, slug: str):
    return await genre_crud.get_genre_by_slug(session, slug)

@router.get("/{genre_id}", response_model=GenrePublic)
async def read_genre_by_id(session: SessionDep, genre_id: str):
    return await genre_crud.get_genre(session, genre_id)

@router.put("/{genre_id}", response_model=GenrePublic)
async def update_genre(session: SessionDep, genre_id: str, genre_in: GenreUpdate):
    genre = await genre_crud.update_genre(session, genre_id, genre_in)
    if not genre:
        return {"error": "Genre not found"}
    return genre
