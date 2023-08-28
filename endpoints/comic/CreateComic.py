import aiomysql
from fastapi import HTTPException

from Model import ComicCreate
from database import Database


async def create_comic(comic_data: ComicCreate, db: Database):
    try:
        # 解析POST请求中的JSON数据
        comic_id = comic_data.comic_id  # 获取漫画ID
        comic_name = comic_data.name
        comic_date = comic_data.time
        comic_intro = comic_data.content
        comic_cover = comic_data.cover
        comic_magazine = comic_data.magazine
        category_id = comic_data.magazine
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"缺少必要字段：{str(e)}")
    if comic_magazine == 1:
        comic_magazine = "kirara"
    if comic_magazine == 2:
        comic_magazine = "MAX"
    if comic_magazine == 3:
        comic_magazine = "Carat"
    if comic_magazine == 4:
        comic_magazine = "Forward"
    try:
        if comic_id == 0:
            # 创建新漫画
            comic_id = await db.execute(
                "INSERT INTO comics (name, date, intro, cover, magazine) VALUES (%s, %s, %s, %s, %s)",
                comic_name, comic_date, comic_intro, comic_cover, comic_magazine
            )
            comic_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
            print("New comic ID is: %s" % comic_id)
        else:
            # 更新现有漫画
            existing_comic = await db.execute(
                "SELECT id FROM comics WHERE id = %s",
                comic_id
            )
            if not existing_comic:
                raise HTTPException(status_code=404, detail=f"找不到ID为 {comic_id} 的漫画")

            await db.execute(
                "UPDATE comics SET name = %s, date = %s, intro = %s, cover = %s, magazine = %s WHERE id = %s",
                comic_name, comic_date, comic_intro, comic_cover, comic_magazine, comic_id
            )

        category = await db.execute(
            "SELECT id FROM categories WHERE id = %s AND category = '漫画'",
            category_id
        )
        if not category:
            raise HTTPException(status_code=400, detail=f"无效的分类ID: {category_id}")

        await db.execute(
            "INSERT INTO comic_category_map (comic_id, category_id) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE category_id = %s",
            comic_id, category_id, category_id
        )

    except aiomysql.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误：{str(e)}")

    return {"status": "success", "message": "漫画已成功创建/更新！"}