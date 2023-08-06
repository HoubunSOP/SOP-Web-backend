from datetime import timedelta, date
from database import Database


async def get_manga_calendar(db: Database):
    # 获取当前时间前后三个月的时间范围
    today = date.today()
    start_date = today - timedelta(days=90)
    end_date = today + timedelta(days=90)

    # 构建查询在当前时间前后三个月发售的漫画列表的SQL语句
    sql = """
        SELECT name, date
        FROM comics
        WHERE date >= %s AND date <= %s
    """

    # 执行查询
    result = await db.execute(sql, start_date, end_date)

    manga_list = []
    for row in result:
        manga_date = row["date"].strftime("%Y-%m-%d")
        is_complete = row["date"] < today
        color = "blue" if is_complete else "red"
        manga = {
            "description": row["name"],
            "isComplete": is_complete,
            "dates": [manga_date],
            "color": color
        }
        manga_list.append(manga)

    return {"status": "success", "message": manga_list}
