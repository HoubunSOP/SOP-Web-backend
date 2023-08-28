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


class PostCreate(BaseModel):
    post_name: str
    post_date: date
    post_content: str
    post_cover: str
    post_comic: List[int]
    categories: List[str]
    tags: List[str]


class RenameCat(BaseModel):
    new_name: str
    category_id: int
