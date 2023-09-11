from Model import CustomHTTPException
from database import Database


async def get_comics_by_tag(db: Database, tag_id: int, num: int):
    types = await db.execute('SELECT tag,name FROM tags WHERE id = %s;', tag_id)
    if types[0]['tag'] != '漫画':
        return {"status": "error", "message": "此标签ID为文章类型"}
    # 执行查询
    query = """
        SELECT c.id, c.name, c.date, c.cover, c.magazine
        FROM comics c
        JOIN comic_tag_map m ON c.id = m.comic_id
        WHERE m.tag_id = %s
        ORDER BY c.date DESC
        LIMIT %s
    """
    rows = await db.execute(query, tag_id, num)
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
    return {"status": "success", "message": {"tag_name": types[0]['name'], "comic_list": comics}}


async def get_posts_by_tag(db: Database, tag_id: int, num: int):
    types = await db.execute('SELECT tag FROM tags WHERE id = %s;', tag_id)
    print(types)
    if types[0]['tag'] != '文章':
        raise CustomHTTPException(detail='此标签ID为漫画类型')
    # 执行查询
    query = """
        SELECT c.id, c.title, c.date, c.cover
        FROM articles c
        JOIN article_tag_map m ON c.id = m.article_id
        WHERE m.tag_id = %s
        ORDER BY c.date DESC
        LIMIT %s
    """
    rows = await db.execute(query, tag_id, num)
    posts = []
    for row in rows:
        post = {
            "id": row['id'],
            "title": row['title'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "cover": row['cover'],
        }
        posts.append(post)

    return {"status": "success", "message": {"tag_name": types[0]['name'], "post_list": posts}}
