import aiomysql

from Model import CustomHTTPException
from database import Database


async def delete_comic(comic_id: int, db: Database):
    try:
        # 检查文章是否存在
        existing_post = await db.execute(
            "SELECT id FROM comics WHERE id = %s",
            comic_id
        )
        if not existing_post:
            raise CustomHTTPException(status_code=404, detail=f"找不到ID为 {comic_id} 的文章")

        # 删除文章与分类的映射关系
        await db.execute(
            "DELETE FROM comic_category_map WHERE comic_id = %s",
            comic_id
        )
        # 删除文章
        await db.execute(
            "DELETE FROM comics WHERE id = %s",
            comic_id
        )

        return {"status": "success", "message": f"ID为 {comic_id} 的漫画已成功删除！"}
    except aiomysql.Error as e:
        raise CustomHTTPException(status_code=500, detail=f"数据库错误：{str(e)}")
