from database import Database


async def get_category_list(type: str, db: Database):
    # 构建查询分类列表和文章数量的SQL语句
    sql = """
        SELECT categories.id, categories.name, (
            SELECT COUNT(*)
            FROM article_category_map
            LEFT JOIN articles ON article_category_map.article_id = articles.id
            WHERE article_category_map.category_id = categories.id
        ) AS article_count
        FROM categories
        """

    if type:
        sql += "WHERE categories.category = %s"
        params = (type,)
    else:
        params = ()

    sql += "GROUP BY categories.id"

    # 执行查询
    result = await db.execute(sql, *params)
    categories = []
    for row in result:
        category = {
            "id": row["id"],
            "name": row["name"],
            "article_count": row["article_count"]
        }
        categories.append(category)

    return {"status": "success", "message": categories}
