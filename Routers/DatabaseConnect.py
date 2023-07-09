from fastapi import APIRouter
from database import Database

router = APIRouter()
db = Database()


@router.on_event("startup")
async def startup():
    await db.connect()


@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()
