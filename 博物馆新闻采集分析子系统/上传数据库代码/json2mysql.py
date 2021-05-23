import os
import json
import mysql.connector


# 读取json文件
def load_json(json_path):
    # 合并各个json文件的内容后，要存入数据库的列表
    news_to_insert = []

    json_list = os.listdir(json_path)
    for filename in json_list:
        if not filename.endswith(".json"):
            continue
        with open(json_path + filename, 'r', encoding='utf-8') as f:
            data = json.load(f)["data"]
        if data is None:
            continue
        for news in data:
            news_to_insert.append(tuple(news.values()))
    
    # for i in news_to_insert:
    #     print(i)
    return news_to_insert


def insert_mysql(news_to_insert):
    print(f"预计插入{len(news_to_insert)}条数据。。。")

    DATABASE = "MUSEUM"
    TABLE = "news"
    mydb = mysql.connector.connect(
        host = "182.92.221.222",
        user = "root",
        passwd = "CS1806se.",
        database = DATABASE
    )
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {TABLE} (museum, time, type, content, photo, source) VALUES (%s, %s, %s, %s, %s, %s)"
    val = news_to_insert
    mycursor.executemany(sql, val)
    mydb.commit()
    print(f"{mycursor.rowcount}条记录插入成功。。。")
    mycursor.close()

 
if __name__ == "__main__":
    json_path = "./"
    news_to_insert = load_json(json_path)
    insert_mysql(news_to_insert)