from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt import (
    JwtAuthorizationCredentials,
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

from Model import access_security, CustomHTTPException, AuthCreate
from Routers import ComicRouter, PostRouter, CategoryRouter, TagRouter, IndexRouter, DatabaseConnect
from database import Database

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
    "http://sop.sakurakoi.top",
    "https://sop.sakurakoi.top",
    "https://www.fwgxt.top",
    "https://fwgxt.top",
    "http://www.fwgxt.top",
    "http://fwgxt.top",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:3001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse('{"status":"error","message":"' + str(exc.detail) + '"}', status_code=exc.status_code)
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


@app.post("/auth")
def auth(auth_data: AuthCreate):
    # subject (actual payload) is any json-able python dict
    subject = {"username": "username", "role": "user"}

    # Create new access/refresh tokens pair
    access_token = access_security.create_access_token(subject=subject)

    return {"access_token": access_token}


@app.get("/users/me")
def read_current_user(
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    # auto_error=False, fo we should check manually
    if not credentials:
        raise CustomHTTPException(detail='您并没有权限这样做')

    # now we can access Credentials object
    return {"username": credentials["username"], "role": credentials["role"]}
