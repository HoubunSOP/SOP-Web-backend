import asyncio
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

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
        detail_url = item.find('DetailPageURL').text
        title = f"{title} 第{volume_no}卷"
        if img_url is None:
            img_url = 'https://houbunsha.co.jp/img/mv_img/con_item_nPrn_1.png'
        else:
            img_url = f"https://houbunsha.co.jp/{img_url}"

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
            existing_cover = result[0]['cover']
            if existing_cover != 'https://houbunsha.co.jp/img/mv_img/con_item_nPrn_1.png':
                if existing_cover != img_url:
                    update_sql = "UPDATE comics SET cover = %s WHERE name = %s"
                    await database.execute(update_sql, img_url, title)
            existing_intro = result[0]['intro']
            if not existing_intro:
                print(f"{title}查询到并没有简介，正在准备从芳文社官网获取")
                intro = get_intro(detail_url, volume_no)
                if intro is not None:
                    update_sql = "UPDATE comics SET intro = %s WHERE name = %s"
                    await database.execute(update_sql, intro, title)

        else:
            print(f"正在准备从芳文社官网获取{title}的简介")
            intro = get_intro(detail_url, volume_no)

            insert_sql = ("INSERT INTO comics "
                          "(name, author, date, cover, magazine, intro, auto) "
                          "VALUES (%s, %s, %s, %s, %s, %s, 1)")
            await database.execute(insert_sql, title, author, publication_date, img_url, magazine, intro)
        print(f"已成功/添加{title}")


# 获取XML内容
def get_xml_content():
    # 从网络获取XML内容
    url = "https://houbunsha.co.jp/xml/"
    response = requests.get(url)
    xml_data = response.content
    return xml_data


# Todo euc-jp编码导致的符号乱码+支持指定获取N卷的简介
def get_intro(detail_url, n):
    # 假设item是包含DetailPageURL的对象
    detail_url = f"https://houbunsha.co.jp/comics/{detail_url}"

    # 发送请求获取HTML页面内容
    response = requests.get(detail_url)
    html_content = response.text

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser', from_encoding='euc-jp')
    # 查找目标元素并提取文本
    intro = None
    maincolumn = soup.find('div', id='maincolumn')
    if maincolumn:
        entrycontainers = maincolumn.find_all('div', class_='entrycontainer')
        n = min(int(n), len(entrycontainers))
        entrycontainer = entrycontainers[-n]
        entryarea = entrycontainer.find(class_='entryarea') if entrycontainer else None
        txtarea = entryarea.find('dl', class_='txtarea') if entryarea else None
        story = txtarea.find('dd', class_='story') if txtarea else None
        intro = story.get_text(strip=True) if story else None
    return intro


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
