# 针对更新的需求进行调整（v4）
# 1、实现地方频道的爬取
# 2、在结果json中加入title，省去v3中提取symbol的步骤，改为判断title，相应地，要改导入数据库的文件
# 3、测试说明
#   （1）先用少一点的博物馆和少一点的curPage
#   （2）再加curPage
#   （3）再加别的博物馆

import requests
import json
import os
from bs4 import BeautifulSoup
import shutil

def get_url_list(origin_url):
    url = origin_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36",
        'Content-Type': 'application/json;charset=UTF-8'
    }
    url_list = []
    try:
        json_urls = requests.get(url=url, headers=headers).json()
        results = json_urls["content"]["results"]
        if results is None:
            return
        for result in results:
            url_list.append(result["url"])
        print(f"正在获取{keyword}的第{curPage}页新闻。。。")
        return url_list
    except Exception as e:
        print(e)    


# 地方频道
# eg. http://www.js.xinhuanet.com/2021-02/07/c_1127073849.htm
#     http://www.zj.xinhuanet.com/2020-06/13/c_1126110863.htm
def crawl_news_A(url, article, soup, titles):
    h1 = article.find_next("h1", id="title")
    if h1 is None:
        return
    title = h1.text.replace("\n", "").replace('\r', "").replace('\u3000', "，").strip().replace(' ', "，")
    if title in titles:
        print("重复的新闻！")
        # print("titles: ", titles)
        # print("title: ", title)
        return
    titles.append(title)

    time = soup.find("span", class_="time").text.replace("\n", "").replace(" ", "").replace('\r', "")
    year = time.split('年')[0]
    month = time.split('年')[1].split('月')[0]
    day = time.split('年')[1].split('月')[1].split('日')[0]
    date = year + "." + month + "." + day

    source = soup.find("em", id="source").text.replace("\n", "").replace(" ", "").replace('\r', "")

    content = []
    img = []
    ps = article.find("div", class_="article").find_all("p")
    for p in ps:
        p_text = p.text.replace("\u3000", "").replace('\n', "").replace('\r', "").replace('\t', "").replace('\xa0', "")
        if "摄" in p_text or "图片来源" in p_text:
            if len(p_text) < 50 and p_text.find("记者", -15):  
                continue
        content.append(p_text)

        url_page = '/'.join(url.split('/')[:-1])
        p_imgs = p.find_all("img")
        for p_img in p_imgs:
            img.append(url_page + '/' + p_img.get("src"))
    content = ''.join(content) 
   
    news = {}
    news["museum"] = keyword
    news["time"] = date
    news["type"] = "positive"
    news["content"] = content
    news["photo"] = img[0] if (len(img) > 0) else ''
    news["source"] = source if (source is not None) else "新华网"
    news["title"] = title

    return news


# 正文频道
# eg. http://www.xinhuanet.com/2020-09/02/c_1126445038.htm
#     http://www.xinhuanet.com/expo/2019-11/18/c_1210358665.htm
def crawl_news_B(url, p_detail, soup, titles):
    h_title = soup.find("div", class_="h-title")
    if h_title is None:
        return
    title = h_title.text.replace("\n", "").replace('\r', "").replace('\u3000', "，").strip().replace(' ', "，")
    if title in titles:
        print("重复的新闻！")
        # print("titles: ", titles)
        # print("title: ", title)
        return
    titles.append(title)

    time = soup.find("span", class_="h-time").text.replace("\n", "").replace(" ", "").replace('\r', "")[:10]
    date = time.split('-')[0] + "." + time.split('-')[1] + "." + time.split('-')[2]

    content = []
    img = []
    ps = p_detail.find_all("p")
    for p in ps:
        if p.find("a"):
            continue
        p_text = p.text.replace("\u3000", "").replace('\n', "").replace('\r', "").replace('\t', "").replace('\xa0', "")
        if "摄" in p_text or "图片来源" in p_text:
            if len(p_text) < 50 and p_text.find("记者", -15):  
                continue
        content.append(p_text)

        url_page = '/'.join(url.split('/')[:-1])
        p_imgs = p.find_all("img")
        for p_img in p_imgs:
            img.append(url_page + '/' + p_img.get("src"))
    content = ''.join(content) 
    
    news = {}
    news["museum"] = keyword
    news["time"] = date
    news["type"] = "positive"
    news["content"] = content
    news["photo"] = img[0] if (len(img) > 0) else ''
    news["source"] = "新华网"
    news["title"] = title

    return news


# 主站
# eg. http://m.xinhuanet.com/2021-04/30/c_1127399187.htm
#     http://m.xinhuanet.com/2021-04/30/c_1127398081.htm
def crawl_news_main(url, head_line, soup, titles):
    h1 = head_line.find_next("h1")
    if h1 is None:
        print("h1 is None")
        return  
    title = h1.find_next("span").text.replace("\n", "").replace('\r', "").replace('\u3000', "，").strip().replace(' ', "，")
    if title in titles:
        print("重复的新闻！")
        # print("titles: ", titles)
        # print("title: ", title)
        return
    titles.append(title)
    
    header_time = soup.find("div", class_="header-time")
    year = header_time.find("span", class_="year").find("em").text.replace("\n", "").replace(" ", "").replace('\u3000', "")
    day = header_time.find("span", class_="day").text.replace(" ", "").split('/')
    date = year + "." + day[0] + "." + day[1]

    content = []
    img = []
    ps = soup.find("div", id="detail").find_all("p")
    for p in ps:
        p_text = p.text.replace("\u3000", "").replace('\n', "").replace('\r', "").replace('\t', "").replace('\xa0', "")
        if "摄" in p_text or "图片来源" in p_text:
            if len(p_text) < 50 and p_text.find("记者", -15):  
                continue
        content.append(p_text)

        url_page = '/'.join(url.split('/')[:-1])
        p_imgs = p.find_all("img")
        for p_img in p_imgs:
            img.append(url_page + '/' + p_img.get("src"))
    content = ''.join(content) 
    
    news = {}
    news["museum"] = keyword
    news["time"] = date
    news["type"] = "positive"
    news["content"] = content
    news["photo"] = img[0] if (len(img) > 0) else ''
    news["source"] = "新华网"
    news["title"] = title

    return news


def crawl_news(url_list, keyword, titles):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36"
    }
    
    all_news = {}
    all_news["data"] = []
    
    for url in url_list:

        try:
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, "lxml")

            head_line = soup.find("div", class_="head-line")
            if head_line is None:
                article = soup.find("div", id="article")
                p_detail = soup.find("div", id="p-detail")
                if article is not None:  # 地方频道
                    news = crawl_news_A(url, article, soup, titles)
                    if news is None:
                        error = "地方频道爬取失败"
                elif p_detail is not None:  # 正文频道
                    news = crawl_news_B(url, p_detail, soup, titles)
                    if news is None:
                        error = "正文频道爬取失败"
                else:
                    news = None
                    error = "不符合主站、正文、地方频道三种页面布局"
            else:  # 主站
                news = crawl_news_main(url, head_line, soup, titles)   
                if news is None:
                    error = "主站爬取失败"
            if news is not None:
                all_news["data"].append(news)
            else:
                print(f"爬取 {url} 对应的新闻出现错误：{error}")

        except Exception as e:
            print(e)

    if len(all_news["data"]) > 0:
        with open(f"新华网_{keyword}.json", 'w', encoding="utf-8") as f:
            json.dump(all_news, f, ensure_ascii=False)


def update_check(json_path):
    # 将当前json文件都合到一起形成news_inserted.json
    # "data"键对应的值（列表）是一条条新闻，是通过其他json文件中的"data"键获取的，包括上一次运行产生的news_inserted.json
    news_inserted = {}
    news_inserted["data"] =  []
    titles = []

    json_list = os.listdir(json_path)
    for filename in json_list:
        if not filename.endswith(".json"):
            continue
        with open(json_path + filename, 'r', encoding='utf-8') as f:
            data = json.load(f)["data"]
        news_inserted["data"].extend(data)
        for news in data:
            titles.append(news["title"])
        shutil.move(json_path + filename, json_path + "backup/" + filename)
    
    news_inserted["num"] = len(titles)
    if news_inserted["num"] > 0:
        with open("news_inserted.json", 'w', encoding="utf-8") as f:
            json.dump(news_inserted, f, ensure_ascii=False)

    print(f"已有{len(titles)}条新闻")
    return titles

if __name__ == "__main__":
    keywords = {"故宫博物院": [], "首都博物馆": [], "中国科学技术馆": [], "中国地质博物馆": [], "中国人民革命军事博物馆": [],      
                "中国航空博物馆": [], "中国国家博物馆": [], "北京自然博物馆": [], "上海博物馆": [], "南京博物院": [],
                "北京鲁迅博物馆": [], "浙江省博物馆": [], "中国茶叶博物馆": []}
    JSON_PATH = "./"  # 默认所有操作均在当前目录
    titles = update_check(JSON_PATH)
    for keyword in keywords.keys():
        for curPage in range(1, 2): 
            origin_url = f"http://so.news.cn/getNews?keyword={keyword}&curPage={curPage}&sortField=0&searchFields=1&lang=cn"
            url_list = get_url_list(origin_url)
            if url_list is not None:
                keywords[keyword].extend(url_list)
        if len(keywords[keyword]) == 0:
            print(f"没有找到{keyword}的新闻  :(")
        else:
            print(f"共找到{len(keywords[keyword])}条关于{keyword}的新闻  :)")
            crawl_news(keywords[keyword], keyword, titles)