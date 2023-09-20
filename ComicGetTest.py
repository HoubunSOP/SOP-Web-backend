import asyncio
import xml.etree.ElementTree as ET
import requests
from database import Database

db = Database()


# 解析XML文件
def parse_xml(xml_content):
    root = ET.fromstring(xml_content)
    items = root.findall('.//Item')
    return items


# 存储数据到MySQL数据库
# Todo 之后需要在数据库中添加是否为自动添加的，并且在后台前端中显示
async def store_data_to_mysql(database, data):
    for item in data:
        title = item.find('Title').text
        volume_no = item.find('VolumeNo').text
        author = item.find('Author').text
        publication_date = item.find('PublicationDate').text
        img_url = item.find('ImgURL').text
        title = f"{title} 第{volume_no}卷"
        if img_url is None:
            img_url = 'https://houbunsha.co.jp/img/mv_img/con_item_nPrn_1.png'

        label = item.find('Label').text
        if label == '6':
            magazine = 'krf'
        elif label == '4':
            magazine = 'kr'
        else:
            magazine = None

        # 检查数据是否已存在，如果存在就更新img_url字段
        sql = "SELECT * FROM comics WHERE name = %s"
        result = await database.execute(sql, title)
        if result:
            existing_cover = result['cover']
            if existing_cover != img_url and existing_cover != 'https://houbunsha.co.jp/img/mv_img/con_item_nPrn_1.png':
                update_sql = "UPDATE comics SET cover = %s WHERE name = %s"
                await database.execute(update_sql, img_url, title)
        else:
            insert_sql = "INSERT INTO comics (name, author, date, cover, magazine) VALUES (%s, %s, %s, %s, %s)"
            await database.execute(insert_sql, title, author, publication_date, img_url, magazine)


# 获取XML内容
def get_xml_content():
    # 从网络获取XML内容
    url = "https://houbunsha.co.jp/xml/"
    response = requests.get(url)
    xml_data = response.content
    return xml_data


# 主函数
async def main():
    # 获取XML内容
    await db.connect()
    xml_content = get_xml_content()

    # 解析XML文件
    items = parse_xml(xml_content)

    # 筛选Label为6或4的Item
    filtered_items = [item for item in items if item.find('Label').text in ['6', '4']]

    # 存储数据到MySQL数据库
    await store_data_to_mysql(db, filtered_items)

    await db.disconnect()


# 运行异步函数
if __name__ == '__main__':
    asyncio.run(main())
