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
url = "http://www.zhejiangmuseum.com/Collection"

r = requests.get(url, headers=hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')

# class_ ='maintxt' 活动列表正文部分   根据网页tag修改
div_list = soup.find_all('div', class_='maintxt')

# 查找下一级网址 即各个活动详情页的网址
anchors = soup.findAll('a')
links = []  # 存取各个活动详情页网址
for tag in soup.find_all('ul', class_='piclist'):
    anchors = tag.findAll('a')
for a in anchors:
    links.append(a['href'])
print("links:", links)

# 从藏品列表页爬取藏品名称
TitleList = []  # 存取藏品名称 这个网址爬出来后十个字符刚好是活动时间
# k = 0
for tag in soup.find_all('ul', class_='piclist'):
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
    for tag in Detailsoup.findAll('div', class_='maintxt'):  # 详情页活动介绍正文
        img_link = tag.findAll('img')  # 查找所有img字段
        for a in img_link:  # 遍历img字段
            ImgList.append("http://www.sxhm.com/" + a['src'])  # 网页给的img链接没有"http://www.sxhm.com/"自己加上
            print("http://www.sxhm.com/" + a['src'])
            break  # 只取第一张图片
        i = 0  # 计数
        for tag in Detailsoup.select('p', calss_='MsoNormal'):  # <p class="MsoNormal">字段是文字介绍
            if (i==1):  # 保存前三句
                break;
            # if (i <= 3):  # 前两个是时间和杂项不需要用， 第三个才是介绍第一句，存入Introlist
            #     continue
            Introduce = tag.get_text()

            # IntroList.append(Introduce)
            # print(Introduce)
            if (len(Introduce) >5):  # 大于5个字的保存并且结束（即只保存第一句）
                i = i + 1
                IntroList.append(Introduce)
                print("Introduce", Introduce)
            else:
                continue  # 可能是空格，太短的不保存
print("IntroList", IntroList)

# =============================================================================
# 爬取完成
# 开始数据格式处理
# =============================================================================

# 最终写入csv的list
Name_Act_List = []  # 藏品名
# Time_Act_List = []  # 活动时间
Intro_Act_List = []  # 藏品简介
Photo_Act_List = []  # 活动图片链接

newTitleList = TitleList[0].split('\n')  # 之前得到的titlelist是一整句，list中只有一个元素，各活动用‘\n'分割 通过这个语句从每个\n分开成新的元素

print("newTitleList", newTitleList)

for name in newTitleList:
    lenth = len(name)
    if (lenth < 2):  # split可能截取出空格作为一个元素 太短的跳过
        continue
    # Time = name[lenth - 10:]  # 取后十个字符，刚好是时间
    # if(len(Time) == 10):
    #     Time_Act_List.append(Time)
    # Time_Act_List.append(Time)
    # Title = name[:lenth - 10]  # 后十个之外的是活动名
    Name_Act_List.append(name)

# print(Time_Act_List)
print("Name_Act_List", Name_Act_List)

for intro in IntroList:
    lenth = len(intro)
    # a = intro.find('。')  # 找第一个句号的位置
    # intro = intro[:a + 1]  # 取第一个句号之前的作为简介
    out = "".join(intro.split())  # 去掉’\x0xa‘等格式控制符只提取文本
    Intro_Act_List.append(out)
    #print(out)
print(Intro_Act_List)

Photo_Act_List = ImgList

help_x_list = []
Museum_list = []
for i in range(0, len(Name_Act_List)):
    help_x_list.append(str(i))
    Museum_list.append("浙江省博物馆")

# =============================================================================
# 开始向CSV中写数据
# =============================================================================
dataframe = pd.DataFrame({
    '博物馆名称': Museum_list,
    '藏品名字': Name_Act_List,
    '藏品介绍': Intro_Act_List,
    '藏品图片地址': Photo_Act_List
})
dataframe.to_csv(r"浙江省博物馆藏品.csv", sep=',')




















