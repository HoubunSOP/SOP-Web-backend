from fastapi import APIRouter
from endpoints.post.CreatePost import create_post
from endpoints.post.GetPost import get_post_info
from Model import PostCreate
from Routers.DatabaseConnect import db

router = APIRouter()


###############
# get区
###############

@router.get("/post/{post_id}")
async def get_post_info_route(post_id: int):
    """
    根据漫画ID获取漫画信息。

    Args:
        post_id (int): 漫画ID。

    Returns:
        dict: 包含漫画信息的json。
    """
    result = await get_post_info(post_id, db)
    return result


###############
# post区 需要添加验证
###############
@router.post("/post/new")
async def create_post_route(post_data: PostCreate):
    """
    创建新文章。

    Args:
        post_data (PostCreate): 包含文章信息的对象。

    Returns:
        dict: 包含是否创建成功的json。
    """
    result = await create_post(post_data, db)
    return result
