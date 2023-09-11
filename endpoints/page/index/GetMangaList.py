from datetime import datetime

from database import Database


async def get_manga_list(db:Database):
    # 获取当前时间月份的第一天
    today = datetime.today()
    first_day_of_month = datetime(today.year, today.month, 1)

    # 构建查询在当前时间月份第一天之后发布的漫画列表的SQL语句
    sql = """
        SELECT id, name, date,cover
        FROM comics
        WHERE date >= %s
    """

    # 执行查询
    result = await db.execute(sql, first_day_of_month)
    if len(result) <= 1:
        return {"status": "warn", "message": "当前并没有漫画预计发布"}
    # 构造返回结果
    manga_list = []
    for row in result:
        manga = {
            "id": row['id'],
            "name": row['name'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "cover": row['cover']
        }
        manga_list.append(manga)

    return {"status": "success", "message": manga_list}