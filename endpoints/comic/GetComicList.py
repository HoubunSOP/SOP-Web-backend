from database import Database


async def get_comic_list(db: Database, limit: int = 10, page: int = 1, category_id: int = None):
    # 判断分类ID是否存在
    if category_id:
        # 获取分类类型（漫画或文章）
        category_result = await db.execute("SELECT category FROM categories WHERE id = %s", category_id)
        if not category_result:
            return {"status": "error", 'message': "无效的分类ID"}

        category = category_result[0]['category']

        if category == '文章':
            return {"status": "error", 'message': "无法从漫画列表筛选文章分类"}

    # 构建计数查询的SQL语句
    count_sql = "SELECT COUNT(*) FROM comics"
    if category_id:
        count_sql += " INNER JOIN comic_category_map ON comics.id = comic_category_map.comic_id"
        count_sql += " WHERE comic_category_map.category_id = %s"

    # 计算总页数
    count_result = await db.execute(count_sql, category_id)  # 使用带有分类筛选的计数查询
    total_count = count_result[0]['COUNT(*)']
    total_pages = (total_count + limit - 1) // limit
    if page > total_pages:
        return {"status": "error", 'message': "并没有那么多的页面"}

    # 构建文章列表查询的SQL语句
    list_sql = '''
            SELECT a.id, a.name, a.date, a.cover,
               (SELECT GROUP_CONCAT(c.id, ':', c.name) 
                FROM comic_category_map AS acm 
                JOIN categories AS c ON acm.category_id = c.id 
                WHERE acm.comic_id = a.id) AS categories
        FROM comics AS a
    '''
    if category_id:
        list_sql += " INNER JOIN comic_category_map ON comics.id = comic_category_map.comic_id"
        list_sql += " WHERE comic_category_map.category_id = %s"
    list_sql += " ORDER BY a.date DESC LIMIT %s OFFSET %s"

    # 计算当前页的文章列表
    offset = limit * (page - 1)
    result = await db.execute(list_sql, category_id, limit, offset)  # 使用带有分类筛选的文章列表查询
    comics = []
    for row in result:
        categories = row['categories'].split(":")
        comic = {'id': row['id'], 'name': row['name'], 'date': row['date'], 'cover': row['cover'],
                 'category_id': categories[0], 'category_name': categories[1]}
        comics.append(comic)

    return {"status": "success", "message": {'comics': comics, 'total_pages': total_pages}}
