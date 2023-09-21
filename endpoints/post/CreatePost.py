import aiomysql
from fastapi import HTTPException

from Model import CustomHTTPException
from Model import PostCreate
from database import Database


async def create_post(post_data: PostCreate, db: Database):
    try:
        # 解析POST请求中的JSON数据
        post_id = post_data.post_id
        post_name = post_data.name
        post_date = post_data.time
        post_content = post_data.content
        post_cover = post_data.cover
        post_comic = ""
        category_id = post_data.category.id  # 使用单个分类ID
        recommended = post_data.recommended
    except KeyError as e:
        raise CustomHTTPException(status_code=400, detail=f"缺少必要字段：{str(e)}")

    try:
        # 在事务中执行数据库操作
        if post_id > 0:
            # 检查文章是否存在
            existing_post = await db.execute(
                "SELECT id FROM articles WHERE id = %s",
                post_id
            )
            if not existing_post:
                raise HTTPException(status_code=404, detail=f"找不到ID为 {post_id} 的文章")

            # 修改文章操作
            await db.execute(
                "UPDATE articles SET title = %s, date = %s, content = %s, cover = %s, comic = %s,recommended = %s WHERE id = %s",
                post_name, post_date, post_content, post_cover, post_comic, recommended, post_id
            )
            await db.execute(
                "UPDATE article_category_map SET category_id = %s WHERE article_id = %s",
                category_id, post_id
            )
        else:
            # 创建文章操作
            post_id = await db.execute(
                "INSERT INTO articles (title, date, content, cover, comic,recommended) VALUES (%s, %s, %s, %s, %s,%s)",
                post_name, post_date, post_content, post_cover, post_comic, recommended
            )
            post_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
            print("New post ID is: %s" % post_id)
            category = await db.execute(
                "SELECT id FROM categories WHERE id = %s AND category = '文章'",
                category_id
            )
            if not category:
                raise HTTPException(status_code=400, detail=f"无效的分类ID: {category_id}")
            await db.execute(
                "INSERT INTO article_category_map (article_id, category_id) VALUES (%s, %s)",
                post_id, category_id
            )
    except aiomysql.Error as e:
        raise CustomHTTPException(status_code=500, detail=f"数据库错误：{str(e)}")

    return {"status": "success", "message": "文章已成功创建/更新！"}
