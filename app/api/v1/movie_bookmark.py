from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, UUID4

router = APIRouter()


class MovieBookmark(BaseModel):
    """Модель закладкок фильмов пользователя"""
    user_id: UUID4
    list_movie_id: set[UUID4]


@router.patch(path="/{movie_id:uuid}/add_movie_bookmark/")
async def add_movie_bookmark(movie_id: UUID):
    return f"add movie {movie_id} to movie bookmark"


@router.delete(path="/{movie_id:uuid}/delete_movie_bookmark/")
async def delete_movie_bookmark(movie_id: UUID):
    return f"delete movie {movie_id} from movie bookmark"


@router.get(path="/list_movie_bookmark/")
async def list_movie_bookmark():
    return "list movie bookmark [1, 2, 3, 4, 5]"
