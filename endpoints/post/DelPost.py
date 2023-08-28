import aiomysql
from fastapi import HTTPException

from database import Database


async def delete_post(post_id: int, db: Database):
    try:
        # 检查文章是否存在
        existing_post = await db.execute(
            "SELECT id FROM articles WHERE id = %s",
            post_id
        )
        if not existing_post:
            raise HTTPException(status_code=404, detail=f"找不到ID为 {post_id} 的文章")

        # 删除文章与分类的映射关系
        await db.execute(
            "DELETE FROM article_category_map WHERE article_id = %s",
            post_id
        )
        # 删除文章
        await db.execute(
            "DELETE FROM articles WHERE id = %s",
            post_id
        )

        return {"status": "success", "message": f"ID为 {post_id} 的文章已成功删除！"}
    except aiomysql.Error as e:
        raise HTTPException(status_code=500, detail=f"数据库错误：{str(e)}")
