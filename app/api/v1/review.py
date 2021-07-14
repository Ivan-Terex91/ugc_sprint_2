from datetime import datetime
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, UUID4

router = APIRouter()


class ReviewModel(BaseModel):
    """Модель рецензии к фильму"""
    id: UUID4
    text: str
    created_at: datetime
    user_id: UUID4
    movie_id: UUID4
    rating_review: int  # TODO вот тут просто лайк дизлайк или 2 поля хранить лайки дизлайки
    rating_movie: int


# TODO отдельная модель на добавление рецензии либо лайки и дизлайки сначала по нулям!!!


@router.post(path="/{movie_id:uuid}/add_review/")
async def add_movie_review(movie_id: UUID, review: str):
    return f"add movie {movie_id} review {review}"


# TODO может передам всё в теле!!! фильм и лайк или дизлайк
@router.patch(path="/{movie_id:uuid}/add_review_rating/")
async def add_review_rating(movie_id: UUID, movie_review_id: UUID, rating_review: int):
    return f"add movie {movie_id} review {movie_review_id} rating review {rating_review}"


# TODO возможность гибкой сортировки при выдаче списка
@router.get(path="/{movie_id:uuid}/list_review/")
async def list_movie_review(movie_id: UUID):
    return f"list review to movie {movie_id}"
