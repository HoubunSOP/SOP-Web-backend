from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials

from Model import access_security, CustomHTTPException, SettingsChange
from Routers.DatabaseConnect import db
from endpoints.page.index.GetMangaCalendar import get_manga_calendar
from endpoints.page.index.GetMangaList import get_manga_list
from endpoints.page.index.GetRecommendedArticles import get_recommended_articles
from endpoints.page.index.GetTopSwiper import get_top_swiper
from endpoints.page.index.Settings import change_settings, get_settings, get_stats

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


@router.get("/index/recommended")
async def recommended_articles_route():
    result = await get_recommended_articles(db)
    return result

@router.get("/index/stats")
async def get_stats_route():
    result = await get_stats(db)
    return result

@router.get("/index/settings")
async def get_settings_route():
    result = await get_settings(db)
    return result


###############
# post区 需要添加验证
###############
@router.post("/index/settings")
async def change_settings_route(settings_change: SettingsChange,
                                credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials:
        raise CustomHTTPException(detail='您并没有权限这样做')
    result = await change_settings(settings_change, db)
    return result
