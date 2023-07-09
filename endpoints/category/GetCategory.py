from database import Database


async def get_comics_by_category(db: Database, category_id: int, num: int):
    types = await db.execute('SELECT category FROM categories WHERE id = %s;',category_id)
    if types[0]['category'] != '漫画':
        return {"status": "error", "message": "此分类ID为文章类型"}
    # 执行查询
    query = """
        SELECT c.id, c.name, c.date, c.cover, c.magazine
        FROM comics c
        JOIN comic_category_map m ON c.id = m.comic_id
        WHERE m.category_id = %s
        ORDER BY c.date DESC
        LIMIT %s
    """
    rows = await db.execute(query, category_id, num)
    comics = []
    for row in rows:
        comic = {
            "id": row['id'],
            "name": row['name'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "cover": row['cover'],
            "magazine": row['magazine'],
        }
        comics.append(comic)
    return {"status": "success", "message": comics}


async def get_posts_by_category(db: Database, category_id: int, num: int):
    types = await db.execute('SELECT category FROM categories WHERE id = %s;', category_id)
    print(types)
    if types[0]['category'] != '文章':
        return {"status": "error", "message": "此分类ID为漫画类型"}
    # 执行查询
    query = """
        SELECT c.id, c.title, c.date, c.cover
        FROM articles c
        JOIN article_category_map m ON c.id = m.article_id
        WHERE m.category_id = %s
        ORDER BY c.date DESC
        LIMIT %s
    """
    rows = await db.execute(query, category_id, num)
    posts = []
    for row in rows:
        post = {
            "id": row['id'],
            "title": row['title'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "cover": row['cover'],
        }
        posts.append(post)
    return {"status": "success", "message": posts}
