from fastapi import APIRouter, Query, HTTPException, Depends

from Model import RenameCat
from Routers.DatabaseConnect import db

from endpoints.category.GetCategory import get_comics_by_category, get_posts_by_category
from endpoints.category.GetCategoryList import get_category_list
from endpoints.category.DelChangeCategory import delete_empty_category, update_category_name

router = APIRouter()


async def validate_type(type: str = Query(None, description="分类类型（漫画/文章/Null）")):
    if type is None:
        return None
    if type not in ["漫画", "文章"]:
        raise HTTPException(status_code=400, detail="类型错误")
    return type


@router.get("/category/list")
async def get_category_list_route(type: str = Depends(validate_type)):
    """
    根据获取分类列表。

    Args:
        type (str): 分类类型(漫画/文章/空)。


    Returns:
        dict: 包含分类列表的json。
    :param type:
    """
    result = await get_category_list(type, db)
    return result


@router.get("/category/del/{category_id}")
async def del_category_route(category_id: int):
    """
    删除文章分类。
    """
    result = await delete_empty_category(db, category_id)
    return result


@router.put("/category/rename/")
async def rename_category_route(rename_data: RenameCat):
    """
    重命名分类。
    """
    result = await update_category_name(db, rename_data.category_id, rename_data.new_name)
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
