from Model import CustomHTTPException
from database import Database


async def get_top_swiper(db: Database):
    result = await db.execute("SELECT topswiper FROM settings")
    if result is None:
        raise CustomHTTPException(detail='没有找到设置')
    print(result)
    top_swiper_ids = result[0]["topswiper"].split(',')
    articles = []
    for article_id in top_swiper_ids:
        article_result = await db.execute("SELECT id, title, cover FROM articles WHERE id = %s", article_id)
        article = article_result[0]
        articles.append({'id': article['id'], 'title': article['title'], 'cover': article['cover']})
    return {"status": "success",
            "message": articles}
