from Model import CustomHTTPException
from components.MarkdownRenderer import markdown_renderer
from database import Database


async def get_post_info(post_id: int, md: int, db: Database):
    query = """
        SELECT c.title AS post_name,
               c.date AS post_date,
               c.content AS post_content,
               c.cover AS post_cover,
               c.comic AS post_comic,
               GROUP_CONCAT(DISTINCT ca.name) AS category_names,
               GROUP_CONCAT(DISTINCT ca.id) AS category_id,
               GROUP_CONCAT(DISTINCT t.name) AS tag_names
        FROM articles c
        LEFT JOIN article_category_map cc ON c.id = cc.article_id
        LEFT JOIN categories ca ON cc.category_id = ca.id
        LEFT JOIN article_tag_map ct ON c.id = ct.article_id
        LEFT JOIN tags t ON ct.tag_id = t.id
        WHERE c.id = %s
        GROUP BY c.id;
    """
    result = await db.execute(query, post_id)
    if result:
        post_name = result[0]['post_name']
        post_date = result[0]['post_date']
        post_content = result[0]['post_content']
        post_cover = result[0]['post_cover']
        post_comic = result[0]['post_comic']
        category_id = result[0]['category_id']
        categories = []
        tags = []
        for r in result:
            if r['category_names']:
                categories += r['category_names'].split(',')
            if r['tag_names']:
                tags += r['tag_names'].split(',')
        categories = list(set(categories))
        tags = list(set(tags))
        if md != 1:
            post_content = markdown_renderer(post_content)
        return {"status": "success",
                "message": {"post_id": post_id, "post_name": post_name, "post_date": post_date,
                            "post_content": post_content, "post_cover": post_cover, "post_comic": post_comic,
                            "categories": categories, "category_id": category_id, "tags": tags}}
    else:
        raise CustomHTTPException(detail='文章不存在')
