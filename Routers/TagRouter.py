from fastapi import APIRouter,Query
from Routers.DatabaseConnect import db
from endpoints.tag.GetTag import get_comics_by_tag, get_posts_by_tag

router = APIRouter()


@router.get("/tag/{tag_id}")
async def get_tag_info_route(tag_id: int, num: int = Query(10, ge=0, le=100), types: str = Query('comic')):
    """
    根据分类ID获取漫画/文章列表。

    Args:
        category_id (int): 分类ID。


    Returns:
        dict: 包含漫画/文章列表的json。
    :param tag_id:
    :param types:
    :param num:
    """
    if types == 'comic':
        result = await get_comics_by_tag(db, tag_id, num)
    else:
        result = await get_posts_by_tag(db, tag_id, num)
    return result
