from fastapi import APIRouter
from post.CreatePost import create_post
from post.GetPost import get_post_info
from Model import PostCreate
from database import Database

router = APIRouter()
db = Database()


@router.on_event("startup")
async def startup():
    await db.connect()


@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()


###############
# get区
###############

@router.get("/post/{post_id}")
async def get_post_info_route(post_id: int):
    result = await get_post_info(post_id, db)
    return result


###############
# post区 需要添加验证
###############
@router.post("/post/new")
async def create_post_route(post_data: PostCreate):
    result = await create_post(post_data, db)
    return result
