# -*- coding: utf-8 -*-
"""
Created on Sun May 16 09:21:11 2021

@author: lenovo
"""


import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup


hdrs = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}

# 博物馆活动列表页网址
url = "https://baike.baidu.com/item/%E5%9B%BD%E5%AE%B6%E4%B8%80%E7%BA%A7%E5%8D%9A%E7%89%A9%E9%A6%86/1372604?fr=aladdin"

r = requests.get(url, headers = hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')
name=[]
i=0
# class_ ='maintxt' 活动列表正文部分   根据网页tag修改 
div_list = soup.find_all('div', class_ ='anchor-list')
# for tag in soup.find_all('a', target='_blank'):
#     title=tag.get_text()
#     i=i+1
#     if(i>51 and i<=247):
#         name.append(title)

#查找下一级网址 即各个活动详情页的网址
anchors = soup.findAll('a')
i=0
links = [] #存取各个活动详情页网址
for tag in soup.find_all('table'):

    anchors = tag.findAll('a')

    if(len(anchors)>1):
        print("anchors",anchors)

        for a in anchors:
            i = i + 1
            #print("i=i=ii=i", i)
            if(i<191):
                title = tag.get_text()
                name.append(","+title)
                links.append("https://baike.baidu.com"+a['href'])

newnamelist = []
helplist = []
for elem in name:
    print("elem\n",elem)
    # helplist.append(elem.split("--"))
    # for helpelem in helplist:
    #     newnamelist.append(helpelem)

print("namwfgind",newnamelist)
print(len(newnamelist))
# print("links\n:",links,name)
# print(len(links))
# print(len(name))
dataframe = pd.DataFrame({
                          '博物馆网址':links,

                              })
dataframe.to_csv(r"C:\Users\chensihan\Desktop\百科.csv",sep=',')
