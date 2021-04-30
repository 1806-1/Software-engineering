""""
服务器上overview表只有5列，id(AI)\address\introduction\name\photo
按模板内容写csv,修改line7、8地址，可实现将地址、简介名称输入数据库
"""
import cursor as cursor
import pandas as pd
io = r'C:\Users\chensihan\Desktop\大三\0-软件工程\课设\中国科学技术馆.csv'
idk=r'C:\Users\chensihan\Desktop\大三\0-软件工程\课设\中国科学技术馆.csv'
data=pd.read_csv(io,encoding='gbk')
print(data)
adress=data.loc[1]["内容"]
name=data.loc[0]["内容"]
intro=data.loc[2]["内容"]
#pht=data.loc[3]["内容"]  如果有图片，修改sql语句
print(name,intro,adress)
import MySQLdb
#db = MySQLdb.connect("182.92.221.222", "root", "CS1806se.", "MUSEUM", charset='utf8' )
db = MySQLdb.connect(host='182.92.221.222',port=3306, user='root', password='CS1806se.',db='MUSEUM',charset='utf8')
cursor = db.cursor()
# SQL 插入语句

sql = "INSERT INTO MUSEUM.overview(address,introduction,bwgname) VALUES ('%s','%s','%s')"%(adress,intro,name)

print(sql)
try:
   # 执行sql语句
   cursor.execute(sql)
   print("数据库连接成功，开始进行查询......")
   db.commit()
except:
   # Rollback in case there is any error
   print("Error: unable to fetch data")
   db.rollback()

# 关闭数据库连接
db.close()