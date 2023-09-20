from datetime import date

from fastapi import HTTPException
from fastapi_jwt import JwtAccessBearerCookie
from pydantic import BaseModel


class ComicCreate(BaseModel):
    comic_id: int
    name: str
    time: date
    content: str
    author: str
    cover: str
    magazine: int
    auto: bool


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


class AuthCreate(BaseModel):
    user_name: str
    password: str


# 一些其他的函数
access_security = JwtAccessBearerCookie(
    secret_key="secret_key",
    auto_error=False,
)


# 自定义 HTTPException 类
class CustomHTTPException(HTTPException):
    def __init__(self, detail: str, status_code: int = 401):
        self.status_code = status_code
        self.detail = detail
