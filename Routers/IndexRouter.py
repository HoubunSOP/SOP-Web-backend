from fastapi import APIRouter
from endpoints.page.index.get_top_swiper import get_top_swiper
from Routers.DatabaseConnect import db

router = APIRouter()


###############
# get区
###############

@router.get("/index/get_top_swiper")
async def top_swiper():
    """
    根据漫画ID获取漫画信息。
    """
    result = await get_top_swiper(db)
    return result
