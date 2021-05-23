# 针对更新的需求进行调整
# 1、每次运行这个脚本之前都要对当前目录下已有的json文件进行处理，以实现导入数据库的只有增量部分，同时保留历史版本

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
            # print("请求的页面不存在！（可能是由于该博物馆没有那么多新闻）")
            return
        for result in results:
            url_list.append(result["url"])
        print(f"正在获取{keyword}的第{curPage}页新闻。。。")
        print("新闻链接地址列表：")
        for idx, url in enumerate(url_list):
            print(f"地址{idx}: {url}")
        print("*"*20 + "\n")
        return url_list
    except Exception as e:
        print(e)    


def crawl_news(url_list, keyword, symbol):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36"
    }
    
    all_news = {}
    all_news["data"] = []
    titles = []
    
    for url in url_list:

        try:
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, "lxml")

            head_line = soup.find("div", class_="head-line")
            if head_line is None:
                continue
            h1 = head_line.find_next("h1")
            if h1 is None:
                continue

            title = h1.find_next("span").text.replace("\n", "").replace('\r', "")
            if title in titles:
                continue
            print(title)
            titles.append(title)

            header_time = soup.find("div", class_="header-time")
            year = header_time.find("span", class_="year").find("em").text.replace("\n", "").replace(" ", "")
            day = header_time.find("span", class_="day").text.replace(" ", "").split('/')
            date = year + "." + day[0] + "." + day[1]
            print(date)

            content = []
            img = []
            ps = soup.find("div", id="detail").find_all("p")
            for p in ps:
                p_text = p.text.replace("\u3000", "").replace('\n', "").replace('\r', "").replace('\t', "").replace('\xa0', "")
                if "摄" in p_text:
                    if len(p_text) < 50 and p_text.find("记者", -15):  
                        print("本段包含‘XXX摄影’等信息，已删去！")
                        continue
                content.append(p_text)

                url_page = '/'.join(url.split('/')[:-1])
                p_imgs = p.find_all("img")
                for p_img in p_imgs:
                    img.append(url_page + '/' + p_img.get("src"))
                    print(p_img.get("src"))
            content = ''.join(content)
            
            if len(content) < 20:
                syb = content
                if syb in symbol:
                    continue
            else:
                syb = content[:10] + content[-10:]
                if syb in symbol:
                    continue
            news = {}
            news["museum"] = keyword
            news["time"] = date
            news["type"] = "positive"
            news["content"] = content
            news["photo"] = img[0] if (len(img) > 0) else ''
            news["source"] = "新华网"
            all_news["data"].append(news)
          

        except Exception as e:
            print(e)

    if len(all_news["data"]) > 0:
        with open(f"新华网_{keyword}.json", 'w', encoding="utf-8") as f:
            json.dump(all_news, f, ensure_ascii=False)


def update_check(json_path):
    # 将当前json文件都合到一起形成news_inserted.json，其结构与其它任何一个json一样
    news_inserted = {}
    news_inserted["data"] =  []
    # 取新闻内容(content)中前10与后10个字为一条新闻的标志，不足20个字以整个content为标志
    symbol = []

    json_list = os.listdir(json_path)
    for filename in json_list:
        if not filename.endswith(".json"):
            continue
        museum = filename[4:-5]
        with open(json_path + filename, 'r', encoding='utf-8') as f:
            data = json.load(f)["data"]
        news_inserted["data"].extend(data)
        for news in data:
            content = news["content"]
            if len(content) < 20:
                symbol.append(content)
            else:
                symbol.append(content[:10] + content[-10:])
        shutil.move(json_path + filename, json_path + "backup/" + filename)
    
    if len(news_inserted["data"]) > 0:
        with open("news_inserted.json", 'w', encoding="utf-8") as f:
            json.dump(news_inserted, f, ensure_ascii=False)

    print(f"已有{len(symbol)}条新闻")
    return symbol

if __name__ == "__main__":
    keywords = {"故宫博物院": [], "首都博物馆": [], "中国科学技术馆": [], "中国地质博物馆": [], "中国人民革命军事博物馆": [],
                "中国航空博物馆": [], "中国国家博物馆": [], "北京自然博物馆": [], "上海博物馆": [], "南京博物院": []}
    symbol = update_check("./")
    for keyword in keywords.keys():
        for curPage in range(1, 6): 
            origin_url = f"http://so.news.cn/getNews?keyword={keyword}&curPage={curPage}&sortField=0&searchFields=1&lang=cn"
            url_list = get_url_list(origin_url)
            if url_list is not None:
                keywords[keyword].extend(url_list)
        if len(keywords[keyword]) == 0:
            print(f"没有找到{keyword}的新闻  :(")
        else:
            print(f"共找到{len(keywords[keyword])}条关于{keyword}的新闻  :)")
            crawl_news(keywords[keyword], keyword, symbol)
