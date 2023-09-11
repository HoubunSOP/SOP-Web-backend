from fastapi import APIRouter, Query, HTTPException, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from Model import CustomHTTPException
from Model import RenameCat, CategoryCreate, access_security
from Routers.DatabaseConnect import db
from endpoints.category.CreateCategory import create_category
from endpoints.category.DelChangeCategory import delete_empty_category, update_category_name
from endpoints.category.GetCategory import get_comics_by_category, get_posts_by_category
from endpoints.category.GetCategoryList import get_category_list

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
async def del_category_route(category_id: int, credentials: JwtAuthorizationCredentials = Security(access_security)):
    """
    删除文章分类。
    """
    if not credentials:
        raise CustomHTTPException(detail='您并没有权限这样做')
    result = await delete_empty_category(db, category_id)
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


@router.put("/category/rename/")
async def rename_category_route(rename_data: RenameCat,
                                credentials: JwtAuthorizationCredentials = Security(access_security)):
    """
    重命名分类。
    """
    if not credentials:
        raise CustomHTTPException(detail='您并没有权限这样做')
    result = await update_category_name(db, rename_data.category_id, rename_data.new_name)
    return result


@router.post("/category/new/")
async def rename_category_route(new_cat_data: CategoryCreate,
                                credentials: JwtAuthorizationCredentials = Security(access_security)):
    """
    新建分类。
    """
    if not credentials:
        raise HTTPException(status_code=401, detail='您并没有权限这样做')
    result = await create_category(new_cat_data, db)
    return result
