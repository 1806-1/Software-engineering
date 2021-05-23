import requests
import pandas as pd
from bs4 import BeautifulSoup

hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}
url = "http://www.jlmuseum.org/"
r = requests.get(url, headers=hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')

div_list = soup.find_all('div', class_='con')

anchors = soup.findAll('li')
links = []
for tag in soup.find_all('div', class_='con'):
    anchors = tag.findAll('a')
    # print("anchors",anchors)
for a in anchors:
    strr = a['href']
    # http: // museum.nenu.edu.cn / info / 1037 / 2124.
    # htm
    links.append("http://museum.nenu.edu.cn/" + strr[3:])

# print(links[1:])

TitleList = []
k = 0
for tag in soup.find_all('div', class_='con'):
    k = k + 1
    title = tag.get_text()
    TitleList.append(title)
    # if k != 1:
    #     pass
    # else:
    #     print(title)
    newTitleList = TitleList[0].split('\n')
# print(newTitleList[3:8])

IntroList = []
ImgList = []
for kk in links[1:]:
    Detailurl = kk
    Detailr = requests.get(Detailurl, headers=hdrs)
    Detailsoup = BeautifulSoup(Detailr.content.decode('utf8', 'ignore'), 'lxml')
    for tag in Detailsoup.findAll('div', class_='v_news_content'):
        # img_link = tag.findAll('img')
        # # print(img_link)

        ImgList.append("http://museum.nenu.edu.cn/.jpg")
# print(ImgList)

        i = 0  # 计数
        # for tag in Detailsoup.select('tr', calss_='firstRow'):
        anchors = Detailsoup.findAll('p')
        for a in anchors:
            i = i + 1
            if i <= 3:  # 保存前三句
                continue
            tt = a.get_text()

            if len(tt) > 2:  # 大于5个字的保存并且结束（即只保存第一句）
                IntroList.append(tt)
                #             # IntroList.append(Introduce)
                #             # print(Introduce)
                break
            else:
                continue  # 可能是空格，太短的不保存
# print(IntroList)
# # =============================================================================
# # 爬取完成
# # 开始数据格式处理
# # =============================================================================
# # 最终写入csv的list
Name_Exhibition_List = []  # 展览名
Time_Exhibition_List = []  # 活动时间
Intro_Exhibition_List = []  # 活动简介
Photo_Exhibition_List = []  # 活动图片链接

newTitleList = TitleList[0].split('\n')  # 之前得到的titlelist是一整句，list中只有一个元素，各活动用‘\n'分割 通过这个语句从每个\n分开成新的元素

# print(newTitleList)

for name in newTitleList[3:8]:
    lenth = len(name)
    # Title = "".join(name.split())  # 去掉’\x0xa‘等格式控制符只提取文本
    Name_Exhibition_List.append(name[10:])
    Time_Exhibition_List.append(name[:10])
# print(Name_Exhibition_List)
# print(Time_Exhibition_List)

for intro in IntroList:
    lenth = len(intro)
    # print(lenth)
    a = intro.find('。')  # 找第一个句号的位置
    intro = intro[:a + 1]  # 取第一个句号之前的作为简介
    out = "".join(intro.split())  # 去掉’\x0xa‘等格式控制符只提取文本
    Intro_Exhibition_List.append(out)
    # print(out)
# print(Intro_Exhibition_List)

Photo_Exhibition_List = ImgList
# print(Photo_Exhibition_List)

help_x_list = []
Museum_list = []

for i in range(0, len(Name_Exhibition_List)):
    help_x_list.append(str(i))
    Museum_list.append("常州博物馆")

# # =============================================================================
# 开始向CSV中写数据
## =============================================================================
d = {
    '博物馆名称': Museum_list,
    '展览名字': Name_Exhibition_List,
    '展览时间': Time_Exhibition_List,
    '展览介绍': Intro_Exhibition_List,
    '展览图片地址': Photo_Exhibition_List
}
dataframe = pd.DataFrame(d)
dataframe.to_csv(r"常州博物馆展览.csv", sep=',')
