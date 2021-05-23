# -*- coding: utf-8 -*-
"""
Created on Sun May 16 09:21:11 2021

@author: lenovo
"""

import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup

hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}

# 博物馆藏品列表页网址
url = "http://www.rjjng.com.cn/"

r = requests.get(url, headers=hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')

# class_ ='maintxt' 活动列表正文部分   根据网页tag修改
div_list = soup.find_all('div', class_='tz_r_first')

# 查找下一级网址 即各个活动详情页的网址
anchors = soup.findAll('a')
links = []  # 存取各个活动详情页网址
for tag in soup.find_all('ul', class_='xwdt'):
    anchors = tag.findAll('a')
for a in anchors:
    links.append("http://www.jzmsm.org/"+a['href'])
print("links:", links)

# 从藏品列表页爬取藏品名称
TitleList = []  # 存取藏品名称 这个网址爬出来后十个字符刚好是活动时间
# k = 0
for tag in soup.find_all('ul', class_='xwdt'):
    # k = k + 1
    title = tag.get_text()
    TitleList.append(title)

print("TitleList:", TitleList)

#
IntroList = []  # 存取简介（爬取结束后存的是大段文字，后面根据句号只取第一句上传数据库）
ImgList = []  # 存取图片地址（爬取结束后与最终写入csv的Photolist一致，直接复制）
for kk in links:  # 遍历详情页链接
    Detailurl = kk
    Detailr = requests.get(Detailurl, headers=hdrs)
    Detailsoup = BeautifulSoup(Detailr.content.decode('utf8', 'ignore'), 'lxml')
    for tag in Detailsoup.findAll('div', class_='gbxs'):  # 详情页活动介绍正文
        img_link = tag.findAll('img')  # 查找所有img字段
        for a in img_link:  # 遍历img字段
            ImgList.append("http://www.jzmsm.org/" + a['src'])  # 网页给的img链接没有"http://www.sxhm.com/"自己加上
            print("photo:http://www.jzmsm.org/" + a['src'])
            break  # 只取第一张图片
        i = 0  # 计数
        intro_arr = tag.find_all('span')
        intro_str = ""
        for intro in intro_arr:
            Introduce = tag.get_text()
            intro_str = intro_str + Introduce
    IntroList.append(Introduce)
    print("Introduce2", IntroList)
    print("length_intro:",len(IntroList))
    print("length_photo:", len(ImgList))
# =============================================================================
# 爬取完成
# 开始数据格式处理
# =============================================================================

# 最终写入csv的list
Name_Act_List = []  # 藏品名
Intro_Act_List = []  # 藏品简介
Photo_Act_List = []  # 活动图片链接

newTitleList = TitleList[0].split('\n')  # 之前得到的titlelist是一整句，list中只有一个元素，各活动用‘\n'分割 通过这个语句从每个\n分开成新的元素

print("newTitleList", newTitleList)
for name in newTitleList:
    lenth = len(name)
    if (lenth <2):  # split可能截取出空格作为一个元素 太短的跳过
        continue
    else:
        Name_Act_List.append(name)
print("Name_Act_List", Name_Act_List)
print("length_title:", len(newTitleList))
for intro in IntroList:
    lenth = len(intro)
    a = intro.find('，')  # 找第一个句号的位置
    intro = intro[:a + 1]  # 取第一个句号之前的作为简介
    out = "".join(intro.split())  # 去掉’\x0xa‘等格式控制符只提取文本
    Intro_Act_List.append(out)
    #print(out)
print(Intro_Act_List)

Photo_Act_List = ImgList

help_x_list = []
Museum_list = []
for i in range(0, len(Name_Act_List)):
    help_x_list.append(str(i))
    Museum_list.append("瑞金中央革命根据地纪念馆")

# # =============================================================================
# # 开始向CSV中写数据
# # =============================================================================
# dataframe = pd.DataFrame({
#     '博物馆名称': Museum_list,
#     '藏品名字': Name_Act_List,
#     '藏品介绍': Intro_Act_List,
#     '藏品图片地址': Photo_Act_List
# })
# dataframe.to_csv(r"博物馆藏品.csv", sep=',')