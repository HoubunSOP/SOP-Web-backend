from fastapi import APIRouter
from comic.CreateComic import create_comic
from comic.GetComic import get_comic_info
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
    result = await get_comic_info(comic_id, db)
    return result


###############
# post区 需要添加验证
###############
@router.post("/comic/new")
async def create_comic_route(comic_data: ComicCreate):
    result = await create_comic(comic_data, db)
    return result
