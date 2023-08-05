from database import Database


async def get_post_list(db: Database, limit: int = 10, page: int = 1, category_id: int = None):
    # 判断分类ID是否存在
    if category_id:
        # 获取分类类型（漫画或文章）
        category_result = await db.execute("SELECT category FROM categories WHERE id = %s", category_id)
        if not category_result:
            return {"status": "error", 'message': "无效的分类ID"}

        category = category_result[0]['category']

        if category == '漫画':
            return {"status": "error", 'message': "无法筛选漫画"}

    # 构建计数查询的SQL语句
    count_sql = "SELECT COUNT(*) FROM articles"
    if category_id:
        count_sql += " INNER JOIN article_category_map ON articles.id = article_category_map.article_id"
        count_sql += " WHERE article_category_map.category_id = %s"

    # 计算总页数
    count_result = await db.execute(count_sql, category_id)  # 使用带有分类筛选的计数查询
    total_count = count_result[0]['COUNT(*)']
    total_pages = (total_count + limit - 1) // limit
    if page > total_pages:
        return {"status": "error", 'message': "并没有那么多的页面"}

    # 构建文章列表查询的SQL语句
    list_sql = "SELECT id, title, date, cover FROM articles"
    if category_id:
        list_sql += " INNER JOIN article_category_map ON articles.id = article_category_map.article_id"
        list_sql += " WHERE article_category_map.category_id = %s"
    list_sql += " ORDER BY date DESC LIMIT %s OFFSET %s"

    # 计算当前页的文章列表
    offset = limit * (page - 1)
    result = await db.execute(list_sql, category_id, limit, offset)  # 使用带有分类筛选的文章列表查询
    articles = []
    for row in result:
        article = {'id': row['id'], 'title': row['title'], 'date': row['date'], 'cover': row['cover']}
        articles.append(article)

    return {"status": "success", "message": {'articles': articles, 'total_pages': total_pages}}
