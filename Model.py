from typing import List
from datetime import date

from pydantic import BaseModel


class ComicCreate(BaseModel):
    comic_id: int
    name: str
    time: date
    content: str
    author: str
    cover: str
    magazine: int


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

class CategoryCreate(BaseModel):
    type: str
    name: str