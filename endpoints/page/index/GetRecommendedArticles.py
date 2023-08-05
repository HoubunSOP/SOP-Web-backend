from database import Database

async def get_recommended_articles(db: Database):
    result = await db.execute("SELECT id, title, date, cover FROM articles WHERE recommended = true")
    articles_list = []
    for row in result:
        article = {
            "id": row["id"],
            "title": row["title"],
            "date": row["date"],
            "cover": row["cover"]
        }
        articles_list.append(article)
    return {"status": "success", "messages": articles_list}