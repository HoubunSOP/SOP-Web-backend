from fastapi import APIRouter, Query
from Routers.DatabaseConnect import db

from endpoints.category.GetCategory import get_comics_by_category, get_posts_by_category
from endpoints.category.GetCategoryList import get_category_list

router = APIRouter()


@router.get("/category/list")
async def get_category_list_route(type: str = Query(None, description="分类类型（可选）")):
    result = await get_category_list(type, db)
    return result


@router.get("/category/{category_id}")
async def get_category_info_route(category_id: int, num: int = Query(10, ge=0, le=100), types: str = Query('comic')):
    """
    根据分类ID获取漫画/文章列表。

    Args:
        category_id (int): 分类ID。


    Returns:
        dict: 包含漫画/文章列表的json。
    :param types:
    :param category_id:
    :param num:
    """
    if types == 'comic':
        result = await get_comics_by_category(db, category_id, num)
    else:
        result = await get_posts_by_category(db, category_id, num)
    return result
