from database import Database


async def get_comic_info(comic_id: int, db: Database):
    query = """
        SELECT c.name AS comic_name,
               c.date AS comic_date,
               c.intro AS comic_intro,
               c.cover AS comic_cover,
               c.magazine AS comic_magazine,
               GROUP_CONCAT(DISTINCT ca.name) AS category_names,
               GROUP_CONCAT(DISTINCT t.name) AS tag_names
        FROM comics c
        LEFT JOIN comic_category_map cc ON c.id = cc.comic_id
        LEFT JOIN categories ca ON cc.category_id = ca.id
        LEFT JOIN comic_tag_map ct ON c.id = ct.comic_id
        LEFT JOIN tags t ON ct.tag_id = t.id
        WHERE c.id = %s
        GROUP BY c.id;
    """
    result = await db.execute(query, comic_id)
    if result:
        comic_name = result[0]['comic_name']
        comic_date = result[0]['comic_date']
        comic_intro = result[0]['comic_intro']
        comic_cover = result[0]['comic_cover']
        comic_magazine = result[0]['comic_magazine']
        categories = []
        tags = []
        for r in result:
            if r['category_names']:
                categories += r['category_names'].split(',')
            if r['tag_names']:
                tags += r['tag_names'].split(',')
        categories = list(set(categories))
        tags = list(set(tags))
        return {"status": "success",
                "message": {"comic_id": comic_id, "comic_name": comic_name, "comic_date": comic_date,
                            "comic_intro": comic_intro, "comic_cover": comic_cover, "comic_magazine": comic_magazine,
                            "categories": categories, "tags": tags}}
    else:
        return {"status": "error", "message": "漫画不存在"}
