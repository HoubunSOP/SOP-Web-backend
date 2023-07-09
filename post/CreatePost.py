import aiomysql
from fastapi import HTTPException

from Model import PostCreate
from database import Database


# {"comic_name":"slow loop","comic_date":"2023-01-01","comic_intro":"qwq","comic_cover":"qwq.jpg",
# "comic_magazine":"kirara","categories":["分类1","分类2"],"tags":["标签1","标签2"]}
async def create_post(post_data: PostCreate, db: Database):
    try:
        # 解析POST请求中的JSON数据
        post_name = post_data.post_name
        post_date = post_data.post_date
        post_content = post_data.post_content
        post_cover = post_data.post_cover
        post_comic = post_data.post_comic
        categories = post_data.categories
        tags = post_data.tags
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"缺少必要字段：{str(e)}")
    try:
        # 在事务中执行数据库操作
        post_id = await db.execute(
            "INSERT INTO articles (title, date, content, cover, comic) VALUES (%s, %s, %s, %s, %s)",
            post_name, post_date, post_content, post_cover, post_comic
        )
        post_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
        print("New comic ID is: %s" % post_id)
        category_ids = []
        for category in categories:
            category_id = await db.execute(
                "SELECT id FROM categories WHERE name = %s AND category = '文章'",
                category
            )

            if not category_id:
                category_id = await db.execute(
                    "INSERT INTO categories (name,category) VALUES (%s,'文章')",
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
                "SELECT id FROM tags WHERE name = %s AND tag = '文章'",
                tag
            )

            if not tag_id:
                tag_id = await db.execute(
                    "INSERT INTO tags (name,tag) VALUES (%s,'文章')",
                    tag
                )
                tag_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
                print("New tag ID is: %s" % tag_id)
            else:
                tag_id = tag_id[0].get("id")
            if tag_id not in tag_ids:
                tag_ids.append(tag_id)
        for category_id in category_ids:
            await db.execute(
                "INSERT INTO article_category_map (article_id, category_id) VALUES (%s, %s)",
                post_id, category_id
            )
        for tag_id in tag_ids:
            await db.execute(
                "INSERT INTO article_tag_map (article_id, tag_id) VALUES (%s, %s)",
                post_id, tag_id
            )
    except aiomysql.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误：{str(e)}")

    return {"message": "文章已成功创建！"}
