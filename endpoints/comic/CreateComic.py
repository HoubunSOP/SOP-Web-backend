import aiomysql
from fastapi import HTTPException

from Model import ComicCreate
from database import Database


async def create_comic(comic_data: ComicCreate, db: Database):
    try:
        # 解析POST请求中的JSON数据
        comic_name = comic_data.comic_name
        comic_date = comic_data.comic_date
        comic_intro = comic_data.comic_intro
        comic_cover = comic_data.comic_cover
        comic_magazine = comic_data.comic_magazine
        category_id = comic_data.category_id
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"缺少必要字段：{str(e)}")
    try:
        # 在事务中执行数据库操作
        comic_id = await db.execute(
            "INSERT INTO comics (name, date, intro, cover, magazine) VALUES (%s, %s, %s, %s, %s)",
            comic_name, comic_date, comic_intro, comic_cover, comic_magazine
        )
        comic_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
        print("New comic ID is: %s" % comic_id)

        category = await db.execute(
            "SELECT id FROM categories WHERE id = %s AND category = '漫画'",
            category_id
        )
        if not category:
            raise HTTPException(status_code=400, detail=f"无效的分类ID: {category_id}")

        await db.execute(
            "INSERT INTO comic_category_map (comic_id, category_id) VALUES (%s, %s)",
            comic_id, category_id
        )

    except aiomysql.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误：{str(e)}")

    return {"status": "success", "message": "漫画已成功创建！"}