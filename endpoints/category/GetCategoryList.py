from database import Database


async def get_category_list(type: str, db: Database):
    # 构建查询分类列表和文章数量的SQL语句
    sql = """
        SELECT categories.id, categories.name, COUNT(*) AS article_count
        FROM categories
        LEFT JOIN article_category_map ON categories.id = article_category_map.category_id
        LEFT JOIN articles ON article_category_map.article_id = articles.id
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

    return {"status": "success", "messages": categories}
