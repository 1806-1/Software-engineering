#!/usr/bin/env python
# coding=utf-8
import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup
hdrs = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}

# =============================================================================
# # 针对不同博物馆的网址 新加博物馆按如下格式加上博物馆百度百科网址即可
# =============================================================================

# 北京自然博物馆
# url = "https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E8%87%AA%E7%84%B6%E5%8D%9A%E7%89%A9%E9%A6%86/2002464?fr=aladdin"
# 南京博物馆
# url = "https://baike.baidu.com/item/%E5%8D%97%E4%BA%AC%E5%8D%9A%E7%89%A9%E9%99%A2?fromtitle=%E5%8D%97%E4%BA%AC%E5%8D%9A%E7%89%A9%E9%A6%86&fromid=3075497"
# 上海博物馆
# url = "https://baike.baidu.com/item/%E4%B8%8A%E6%B5%B7%E5%8D%9A%E7%89%A9%E9%A6%86/556555?fr=aladdin"
# 中国国家博物馆
# url = "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E5%8D%9A%E7%89%A9%E9%A6%86/567902?fr=aladdin"
# 中国航空博物馆
url = "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E8%88%AA%E7%A9%BA%E5%8D%9A%E7%89%A9%E9%A6%86/1632663?fr=aladdin"



r = requests.get(url, headers = hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')


div_list = soup.find_all('div', class_ ='basic-info cmn-clearfix')

# 用于输出的list
list = [] #内容
name_list = [] #属性

# 爬取博物馆信息 内容
for tag in soup.find_all('dl', class_='basicInfo-block basicInfo-left'):
    for tag in soup.find_all('dd', class_='basicInfo-item value'):
        museum=tag.get_text()
        museum_mes = museum
        print(museum_mes)
        list.append(museum_mes)

# 爬取博物馆信息表表头内容
for tag in soup.find_all('dl', class_='basicInfo-block basicInfo-left'):
    for tag in soup.find_all('dt', class_='basicInfo-item name'):
        museum=tag.get_text()
        museum_mes_name = museum
        print(museum_mes_name)
        name_list.append(museum_mes_name)



# 设置写入文件的格式
dataframe = pd.DataFrame({'属性':name_list,'内容':list})
# =============================================================================
# 针对不同博物馆写入不同文件
# =============================================================================
# 北京自然博物馆
# dataframe.to_csv(r"北京自然博物馆.csv",sep=',')

# 南京博物院
# dataframe.to_csv(r"南京博物院.csv",sep=',')

# 上海博物馆
# dataframe.to_csv(r"上海博物馆.csv",sep=',')

# # 中国国家博物馆
# dataframe.to_csv(r"中国国家博物馆.csv",sep=',')

# 中国航空博物馆
dataframe.to_csv(r"中国航空博物馆.csv",sep=',')




# =============================================================================
