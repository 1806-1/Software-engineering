import requests
import pandas as pd
from bs4 import BeautifulSoup

hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}
url = "http://www.aihuihistorymuseum.com/"
r = requests.get(url, headers=hdrs)
soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')

div_list = soup.find_all('div', class_='maintxt')

anchors = soup.findAll('a')
links = []
for tag in soup.find_all('ul', class_='piclist'):
    anchors = tag.findAll('a')
    # print("anchors",anchors)
for a in anchors:
    links.append(a['href'])
# print(links)

TitleList = []
k = 0
for tag in soup.find_all('ul', class_='piclist'):
    k = k + 1
    title = tag.get_text()
    TitleList.append(title)
    # if k == 1:
    # print(title)
# print(TitleList)


TimeList = []
for tt in links:
    Detailurl = tt
    Detailr = requests.get(Detailurl, headers=hdrs)
    Detailsoup = BeautifulSoup(Detailr.content.decode('utf8', 'ignore'), 'lxml')
    time = Detailsoup.find('div', class_='p').text
    # time = tag.get_text()
    TimeList.append(time)
    # if k == 1:
    #     print(time)
# print(TimeList)

IntroList = []
ImgList = []
for kk in links:
    Detailurl = kk
    Detailr = requests.get(Detailurl, headers=hdrs)
    Detailsoup = BeautifulSoup(Detailr.content.decode('utf8', 'ignore'), 'lxml')
    for tag in Detailsoup.findAll('div', class_='maintxt'):
        img_link = tag.findAll('img')
        for a in img_link:
            ImgList.append("http://www.sxhm.com/" + a['src'])
            # print("http://www.sxhm.com/" + a['src'])
            break
        i = 0  # 计数
        for tag in Detailsoup.select('p', calss_='MsoNormal'):  # <p class="MsoNormal">字段是文字介绍
            i = i+1
            if (i <= 2):  # 保存前三句
                continue
            Introduce = tag.get_text()
            # IntroList.append(Introduce)
            # print(Introduce)
            if len(Introduce) > 2:  # 大于5个字的保存并且结束（即只保存第一句）
                IntroList.append(Introduce)
                break
            else:
                continue  # 可能是空格，太短的不保存
# print(IntroList)
# =============================================================================
# 爬取完成
# 开始数据格式处理
# =============================================================================
# 最终写入csv的list
Name_Exhibition_List = []  # 展览名
Time_Exhibition_List = []  # 活动时间
Intro_Exhibition_List = []  # 活动简介
Photo_Exhibition_List = []  # 活动图片链接

newTitleList = TitleList[0].split('\n')  # 之前得到的titlelist是一整句，list中只有一个元素，各活动用‘\n'分割 通过这个语句从每个\n分开成新的元素

# print(newTitleList)

for name in newTitleList:
    lenth = len(name)
    if lenth < 2:  # split可能截取出空格作为一个元素 太短的跳过
        continue
    # Title = "".join(name.split())  # 去掉’\x0xa‘等格式控制符只提取文本
    Name_Exhibition_List.append(name[:lenth-3])
print(Name_Exhibition_List)

for time in TimeList:
    lenth = len(time)
    if lenth < 2:  # split可能截取出空格作为一个元素 太短的跳过
        continue
    Time = time[1:10]  # 取十个字符，刚好是时间
    # if(len(Time) == 10):
    #     Time_Act_List.append(Time)
    Time_Exhibition_List.append(Time)
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
    Museum_list.append("爱辉历史陈列馆")

# # =============================================================================
# # 开始向CSV中写数据
# # =============================================================================
d = {
    '博物馆名称': Museum_list,
    '展览名字': Name_Exhibition_List,
    '展览时间': Time_Exhibition_List,
    '展览介绍': Intro_Exhibition_List,
    '展览图片地址': Photo_Exhibition_List
}
dataframe = pd.DataFrame(d)
dataframe.to_csv(r"爱辉历史陈列馆展览.csv", sep=',')
