from fastapi import FastAPI

from Routers import ComicRouter, PostRouter
from database import Database

app = FastAPI()
db = Database()
# 注册漫画分区的API路由
app.include_router(PostRouter.router)
app.include_router(ComicRouter.router)



###############
# on_event区
###############

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


###############
# get区
###############
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/db/check")
async def check_db_connection():
    try:
        temp_db = Database()
        await temp_db.connect()
        await temp_db.execute("SELECT 1")
        await temp_db.disconnect()
        return {"status": "success", "message": "数据库连接正常"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
