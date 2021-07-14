from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, UUID4

router = APIRouter()


class MovieRatingModel(BaseModel):
    """Модель рейтинга фильма"""
    value: int
    user_id: UUID4
    movie_id: UUID4

    # TODO может быть валидатор поля value (от 0 до 10)


@router.get(path="/{movie_id:uuid}/count_ratings/")
async def count_movie_rating(movie_id: UUID):
    return f"{movie_id} count ratings - 1000"


@router.get(path="/{movie_id:uuid}/avg_rating/")
async def avg_movie_rating(movie_id: UUID):
    return f"{movie_id} avg ratings - 8.8"


@router.post(path="/{movie_id:uuid}/add_rating/")
async def add_movie_rating(movie_id: UUID, rating: int):
    return f"add movie {movie_id} rating {rating}"


@router.patch(path="/{movie_id:uuid}/change_rating/")
async def change_movie_rating(movie_id: UUID):
    return f"change movie rating {movie_id}"


@router.delete(path="/{movie_id:uuid}/change_rating/")
async def delete_movie_rating(movie_id: UUID):
    return f"delete movie rating {movie_id}"
