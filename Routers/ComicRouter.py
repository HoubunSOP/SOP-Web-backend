from fastapi import APIRouter
from endpoints.comic.CreateComic import create_comic
from endpoints.comic.GetComic import get_comic_info
from Model import ComicCreate
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

@router.get("/comic/{comic_id}")
async def get_comic_info_route(comic_id: int):
    """
    根据漫画ID获取漫画信息。

    Args:
        comic_id (int): 漫画ID。

    Returns:
        dict: 包含漫画信息的json。
    """
    result = await get_comic_info(comic_id, db)
    return result


###############
# post区 需要添加验证
###############
@router.post("/comic/new")
async def create_comic_route(comic_data: ComicCreate):
    """
    创建新漫画。

    Args:
        comic_data (ComicCreate): 包含漫画信息的对象。

    Returns:
        dict: 包含是否创建成功的json。
    """
    result = await create_comic(comic_data, db)
    return result
