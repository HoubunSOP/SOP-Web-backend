from database import Database


async def delete_empty_category(db: Database, category_id):
    # 检查分类是否存在
    check_query = "SELECT COUNT(*) FROM categories WHERE id = %s"
    result = await db.execute(check_query, category_id)
    count = result[0]["COUNT(*)"]

    if count == 0:
        # 分类不存在，返回错误或抛出异常，根据你的需求
        return {"status": "error", "message": "并没有此分类"}
    # 查询分类下的文章数量
    query = "SELECT COUNT(*) FROM article_category_map WHERE category_id = %s"
    result = await db.execute(query, category_id)
    articles_count = result[0]["COUNT(*)"]

    # 查询分类类型
    category_type_query = "SELECT category FROM categories WHERE id = %s"
    category_type_result = await db.execute(category_type_query, category_id)
    category_type = category_type_result[0]["category"]

    # 如果分类类型是漫画，不删除分类
    if category_type == "漫画":
        return {"status": "error", "message": "此分类并不是文章分类，暂不支持删除"}

    # 如果文章数量为 0，删除分类
    if articles_count == 0:
        delete_query = "DELETE FROM categories WHERE id = %s"
        await db.execute(delete_query, category_id)
        return {"status": "success", "message": "删除完成"}
    else:
        return {"status": "error", "message": "此分类下还有文章，请将所有文章都转移到其他分类后再删除"}


async def update_category_name(db: Database, category_id, new_name):
    # 检查分类是否存在
    check_query = "SELECT COUNT(*) FROM categories WHERE id = %s"
    result = await db.execute(check_query, category_id)
    count = result[0]["COUNT(*)"]

    if count == 0:
        # 分类不存在，返回错误或抛出异常，根据你的需求
        return {"status": "error", "message": "并没有此分类"}

    # 更新分类名称
    update_query = "UPDATE categories SET name = %s WHERE id = %s"
    await db.execute(update_query, new_name, category_id)

    return {"status": "success", "message": "分类重命名完成"}
