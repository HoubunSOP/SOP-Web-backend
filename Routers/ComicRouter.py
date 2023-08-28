from fastapi import APIRouter, Query
from endpoints.comic.CreateComic import create_comic
from endpoints.comic.DelComic import delete_comic
from endpoints.comic.GetComic import get_comic_info
from Model import ComicCreate
from Routers.DatabaseConnect import db
from endpoints.comic.GetComicList import get_comic_list

router = APIRouter()


###############
# get区
###############
@router.get("/comic/list")
async def get_comic_list_route(limit: int = Query(10, gt=0), page: int = Query(1, gt=0),
                               category_id: int = Query(None, gt=0)):
    """
    根据limit与page参数获取漫画列表。
    """
    result = await get_comic_list(db, limit, page, category_id)
    return result
@router.get("/comic/del/{comic_id}")
async def del_comic_route(comic_id: int):
    """
    删除漫画。
    """
    result = await delete_comic(comic_id, db)
    return result


@router.get("/comic/{comic_id}")
async def get_comic_info_route(comic_id: int, md: int = Query(None, gt=0)):
    """
    根据漫画ID获取漫画信息。

    Args:
        comic_id (int): 漫画ID。

    Returns:
        dict: 包含漫画信息的json。
    """
    result = await get_comic_info(comic_id, md, db)
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
