from Model import CustomHTTPException, SettingsChange
from database import Database


async def change_settings(settings_change: SettingsChange, db: Database):
    await change_top_swiper(settings_change.topswiper, db)
    return {"status": "success", "message": "设置已经成功更新！"}


async def change_top_swiper(topswiper_change, db: Database):
    post_ids_str = topswiper_change
    post_ids = post_ids_str.split(",")

    # 如果topswiper_change为空，则删除settings表中的topswiper字段内容
    if post_ids[0].isdigit():
        # 检查每个post_id是否存在
        for post_id in post_ids:
            select_query = "SELECT * FROM articles WHERE id = %s"
            result = await db.execute(select_query, post_id)
            # 如果文章不存在，则抛出CustomHTTPException
            if not result:
                raise CustomHTTPException(status_code=200, detail=f"文章 {post_id} 不存在")

        # 更新settings表中的topswiper字段
        update_query = "UPDATE settings SET topswiper = %s WHERE id = 0"
        await db.execute(update_query, post_ids_str)
    else:
        update_query = "UPDATE settings SET topswiper = '' WHERE id = 0"
        await db.execute(update_query)


async def get_settings(db: Database):
    settings = await db.execute("SELECT topswiper FROM settings WHERE id = 0")
    return {"status": "success", "message": {"topswiper": settings[0]['topswiper']}}
