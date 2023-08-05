from fastapi import FastAPI

from Routers import ComicRouter, PostRouter, CategoryRouter, TagRouter, IndexRouter, DatabaseConnect
from database import Database

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db = Database()
# 注册API路由
app.include_router(PostRouter.router)
app.include_router(ComicRouter.router)
app.include_router(CategoryRouter.router)
app.include_router(TagRouter.router)
app.include_router(IndexRouter.router)
# 这不是路由，而是让其他路由连接的数据库控件
app.include_router(DatabaseConnect.router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
