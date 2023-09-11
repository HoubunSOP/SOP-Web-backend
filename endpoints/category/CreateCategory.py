import aiomysql

from Model import CategoryCreate
from Model import CustomHTTPException
from database import Database


async def create_category(category_data: CategoryCreate, db: Database):
    try:
        # 解析POST请求中的JSON数据
        category_type = category_data.type
        category_name = category_data.name
    except KeyError as e:
        raise CustomHTTPException(status_code=400, detail=f"缺少必要字段：{str(e)}")

    try:
        # 检查分类是否已存在
        existing_category = await db.execute(
            "SELECT id FROM categories WHERE category = %s AND name = %s",
            category_type, category_name
        )
        if existing_category:
            raise CustomHTTPException(status_code=400, detail=f"分类已存在：{category_type} - {category_name}")

        # 创建新分类
        category_id = await db.execute(
            "INSERT INTO categories (category, name) VALUES (%s, %s)",
            category_type, category_name
        )
        category_id = (await db.execute("SELECT LAST_INSERT_ID()"))[0]["LAST_INSERT_ID()"]
        print("New category ID is: %s" % category_id)

    except aiomysql.Error as e:
        raise CustomHTTPException(status_code=500, detail=f"数据库错误：{str(e)}")

    return {"status": "success", "message": "分类已成功创建！"}
