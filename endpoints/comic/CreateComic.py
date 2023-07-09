import aiomysql
from fastapi import HTTPException

from Model import ComicCreate
from database import Database


# {"comic_name":"slow loop","comic_date":"2023-01-01","comic_intro":"qwq","comic_cover":"qwq.jpg",
# "comic_magazine":"kirara","categories":["分类1","分类2"],"tags":["标签1","标签2"]}
async def create_comic(comic_data: ComicCreate, db: Database):
    try:
        # 解析POST请求中的JSON数据
        comic_name = comic_data.comic_name
        comic_date = comic_data.comic_date
        comic_intro = comic_data.comic_intro
        comic_cover = comic_data.comic_cover
        comic_magazine = comic_data.comic_magazine
        categories = comic_data.categories
        tags = comic_data.tags
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
        category_ids = []
        for category in categories:
            category_id = await db.execute(
                "SELECT id FROM categories WHERE name = %s AND category = '漫画'",
                category
            )

            if not category_id:
                category_id = await db.execute(
                    "INSERT INTO categories (name,category) VALUES (%s,'漫画')",
                    category
                )
                category_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
                print("New category ID is: %s" % category_id)
            else:
                category_id = category_id[0].get("id")
            if category_id not in category_ids:
                category_ids.append(category_id)
        tag_ids = []
        for tag in tags:
            tag_id = await db.execute(
                "SELECT id FROM tags WHERE name = %s AND tag = '漫画'",
                tag
            )

            if not tag_id:
                tag_id = await db.execute(
                    "INSERT INTO tags (name,tag) VALUES (%s,'漫画')",
                    tag
                )
                tag_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
                print("New tag ID is: %s" % tag_id)
            else:
                tag_id = tag_id[0].get("id")
            if tag_id not in tag_ids:
                tag_ids.append(tag_id)
        for category_id in category_ids:
            print("INSERT INTO comic_category_map (comic_id, category_id) VALUES (%s, %s)" % (comic_id, category_id))

            await db.execute(
                "INSERT INTO comic_category_map (comic_id, category_id) VALUES (%s, %s)",
                comic_id, category_id
            )
        for tag_id in tag_ids:
            await db.execute(
                "INSERT INTO comic_tag_map (comic_id, tag_id) VALUES (%s, %s)",
                comic_id, tag_id
            )
    except aiomysql.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误：{str(e)}")

    return {"status": "success","message": "漫画已成功创建！"}
