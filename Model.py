from typing import List
from datetime import date

from pydantic import BaseModel


class ComicCreate(BaseModel):
    comic_name: str
    comic_date: date
    comic_intro: str
    comic_cover: str
    comic_magazine: str
    categories: List[str]
    tags: List[str]


class Category(BaseModel):
    id: int
    label: str


class PostCreate(BaseModel):
    post_id: int
    name: str
    time: date
    content: str
    cover: str
    category: Category


class RenameCat(BaseModel):
    new_name: str
    category_id: int
