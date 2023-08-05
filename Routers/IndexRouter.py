from fastapi import APIRouter

from endpoints.page.index.GetMangaCalendar import get_manga_calendar
from endpoints.page.index.GetMangaList import get_manga_list
from endpoints.page.index.GetTopSwiper import get_top_swiper
from Routers.DatabaseConnect import db

router = APIRouter()


###############
# get区
###############

@router.get("/index/get_top_swiper")
async def top_swiper_route():
    """
    获取轮播图的文章信息以及列表
    """
    result = await get_top_swiper(db)
    return result


@router.get("/index/get_manga_list")
async def manga_list_route():
    """
    获取未来发行本的列表与信息
    """
    result = await get_manga_list(db)
    return result


@router.get("/index/calendar")
async def manga_calendar_route():
    """
    获取±90天的漫画发布日期及信息并以calendar数据返回
    """
    result = await get_manga_calendar(db)
    return result
