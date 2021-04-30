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

for tag in soup.find_all('dl', class_='basicInfo-block basicInfo-left'):
    for tag in soup.find_all('dd', class_='basicInfo-item value'):
        museum=tag.get_text()
        museum_mes = museum
        print(museum_mes)
        list.append(museum_mes)

for tag in soup.find_all('dl', class_='basicInfo-block basicInfo-left'):
    for tag in soup.find_all('dt', class_='basicInfo-item name'):
        museum=tag.get_text()
        museum_mes_name = museum
        print(museum_mes_name)
        name_list.append(museum_mes_name)

# =============================================================================
# 对于左边的信息进行爬取
# =============================================================================
# for each in div_list:
#     uls = each.find('dl',class_ ='basicInfo-block basicInfo-left')
#     m_span = uls.findAll('dd')#内容 如 南京博物馆
#     n_span = uls.findAll('dt')#属性 如 博物馆名称




# =============================================================================
# 暂存英文属性名
#     "Museum_English_Name"
#     "Museum_Category"
#     "Museum_OpeningTime"
#     "Museum_Address"
# =============================================================================

# =============================================================================
# 将爬取信息加入字典中 但现在只能实现将李斯特输出在csv中 dict暂时无用
# # dict_left = {n_span[0].contents[0] : m_span[0].contents[0], 
# #         n_span[1].contents[0] : m_span[1].contents[0],
# #         n_span[2].contents[0] : m_span[2].contents[0],
# #         n_span[3].contents[0] : m_span[3].contents[0],
# #         n_span[5].contents[0] : m_span[5].contents[0]
# #         }
# # print(dict_left)
# =============================================================================



# length = len(m_span)#数据项数目
# # 将爬取数据逐项存入list中
# for i in range (0,length):
#     list.append(m_span[i].contents[0])
#     name_list.append(n_span[i].contents[0])
#     print(m_span[i].contents[0], n_span[i].contents[0])


# =============================================================================
#  对于右边的信息进行爬取    
# =============================================================================

# for each in div_list:
#     uls = each.find('dl',class_ ='basicInfo-block basicInfo-right')
#     # uls = each.find('div', class_ ='basic-info cmn-clearfix')
#     m_span = uls.findAll('dd')#内容 如 南京博物馆
#     n_span = uls.findAll('dt')#属性 如 博物馆名称
    
# =============================================================================
    # 同上面的dict_left 暂时无用
# # dict_right = {n_span[0].contents[0] : m_span[0].contents[0], 
# #         n_span[1].contents[0] : m_span[1].contents[0],
# #         n_span[2].contents[0] : m_span[2].contents[0],
# #         n_span[4].contents[0] : m_span[4].contents[0],
# #         n_span[3].contents[0] : m_span[3].contents[0],
# #         n_span[5].contents[0] : m_span[5].contents[0]
# #         }
# # print(dict_right)
# =============================================================================

# 同上边的for循环
# length = len(m_span)
# for i in range (0,length):
#     list.append(m_span[i].contents[0])
#     name_list.append(n_span[i].contents[0])
#     print(m_span[i].contents[0], n_span[i].contents[0])

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
# 后面代码都不用  以上代码都是根据最后面的从#!/usr/bin/env python开始的代码改写而来
# =============================================================================
# # 如果不添加newline=""的话，就会每条数据中间都会有空格行
# with open("test.csv","w", newline="",encoding='utf-8') as csvfile: 
#     # 初始化写入对象
#     writer = csv.writer(csvfile)

#     #先写入columns_name
#     #writer.writerow(["index","a_name","b_name"])
#     #写入多行用writerows
#     writer.writerows([name_left_list,list_left,name_right_list,list_right])



# =============================================================================
#!/usr/bin/env python
# coding=utf-8
# =============================================================================
# import requests
# from bs4 import BeautifulSoup
# hdrs = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}
# url = "http://jbk.39.net/yyz/jbzs/"
# r = requests.get(url, headers = hdrs)
# soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')
# #疾病名称
# for tag in soup.find_all('div', class_='disease'):
#     disease = tag.find('h1').get_text()
#     disease_name = disease
# print(disease)
# #疾病简介
# div_list = soup.find_all('p', class_='introduction')
# for each in div_list:
#     introduce = each.text.strip()
#     disease_introduce = introduce
# print(disease_introduce)
# for tag in soup.find_all('div', class_='list_left'):
#     uls = tag.find('ul',class_="disease_basic")
#     m_span = uls.findAll('span')
#     # print(m_span)
#     is_yibao = m_span[1].contents[0]#是否医保
#     other_name = m_span[3].contents[0]#别名
#     fbbw = m_span[5].contents[0]#发病部位
#     is_infect = m_span[7].contents[0]#是否传染
#     dfrq = m_span[9].contents[0]#多发人群
#     m_a = uls.findAll('a')
#     fbbw = m_a[0].contents[0]#发病部位
# print(is_yibao)
# print(other_name)
# print(is_infect)
# print(fbbw)
# =============================================================================
# =============================================================================
