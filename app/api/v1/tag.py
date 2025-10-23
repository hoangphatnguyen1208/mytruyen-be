from fastapi import APIRouter
from app.api.deps import SessionDep, CurrentAdmin, CurrentUser

from app.crud import tag as tag_crud
from app.schema.tag import TagCreate, TagPublic, TagUpdate

from app.utilities.exceptions.http.exc_400 import http_exc_400_tag_bad_request
from app.utilities.exceptions.http.exc_404 import http_404_exc_tag_not_found_request


router = APIRouter(prefix="/tags", tags=["tag"])

@router.post("", response_model=TagPublic)
async def create_tag(session: SessionDep, current_admin: CurrentAdmin, tag_in: TagCreate):
    existing_tag = await tag_crud.get_tag_by_name(session, tag_in.name)
    if existing_tag:
        raise http_exc_400_tag_bad_request(name=tag_in.name)
    tag = await tag_crud.create_tag(session, tag_in)
    return tag

@router.get("", response_model=list[TagPublic])
async def get_tags(session: SessionDep):
    tags = await tag_crud.get_tags(session)
    return tags

@router.get("/{slug}", response_model=TagPublic)
async def get_tag_by_slug(session: SessionDep, slug: str):
    tag = await tag_crud.get_tag_by_slug(session, slug)
    if not tag:
        raise http_404_exc_tag_not_found_request(string=slug)
    return tag

@router.put("/{slug}", response_model=TagPublic)
async def update_tag(session: SessionDep, slug: str, tag_in: TagUpdate):
    existing_tag = await tag_crud.get_tag_by_slug(session, slug)
    if not existing_tag:
        raise http_404_exc_tag_not_found_request(string=slug)
    updated_tag = await tag_crud.update_tag(session, existing_tag.id, tag_in)
    return updated_tag

@router.delete("/{slug}", response_model=dict)
async def delete_tag(session: SessionDep, slug: str, current_admin: CurrentAdmin):
    existing_tag = await tag_crud.get_tag_by_slug(session, slug)
    if not existing_tag:
        raise http_404_exc_tag_not_found_request(string=slug)
    await tag_crud.delete_tag(session, existing_tag.id)
    return {"message": "Tag deleted successfully"}

