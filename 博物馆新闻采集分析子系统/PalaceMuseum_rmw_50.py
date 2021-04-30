import requests
import json
from bs4 import BeautifulSoup

def crawl_news(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36",
    }
    url = url
    info = {}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "lxml")

        title_h1s = soup.find_all("h1")
        for title_h1 in title_h1s:
            print(title_h1.text)
            if title_h1.find_next('a') or title_h1.find_next('img'):
                continue
            else:
                print("标题：" + title_h1.text)
        # print(len(title_h1s))
        if len(title_h1s) > 1:
            box_01_1 = ".channel"
            date_source_1 = "col-1-1"
            box_con_1 = ".rm_txt_con"
        else:
            box_01_1 = ".box01"
            date_source_1 = "fl"
            box_con_1 = ".box_con"

        box_01 = soup.select_one(box_01_1)
        date_source = box_01.find_next("div", class_=date_source_1).text
        # print(date_source)
        date_source = date_source.strip().replace("\n", "").replace('\r', "").replace(' ', "").replace("|", "")
        date = date_source.split("来源：")[0]
        source = date_source.split("来源：")[1]
        print("日期：" + date)
        print("来源：" + source)

        content = []
        box_con = soup.select_one(box_con_1)
        p_all = box_con.find_all("p")
        for p in p_all:
            content.append(p.text.replace("\u3000", "").replace('\n', "")
                                 .replace('\r', "").replace('\t', "").replace('\xa0', ""))
        # print(content)
    except Exception as e:
        print(e)


def get_url_list(origin_url):
    url = origin_url
    data = {
        "key":"故宫博物院",
        "page":1,
        "limit":10,
        "hasTitle":"true",
        "hasContent":"true",
        "isFuzzy":"true",
        "type":0,
        "sortType":2,
        "startTime":0,
        "endTime":0
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36",
        'Content-Type': 'application/json;charset=UTF-8'
    }

    url_list = []
    try:
        json_urls = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
        records = json_urls["data"]["records"]
        for record in records:
            url_list.append(record["url"])
        # print(url_list)
        return url_list
    except Exception as e:
        print(e)



if __name__ == "__main__":
    origin_url = "http://search.people.cn/api-search/elasticSearch/search"
    url_list = get_url_list(origin_url)
    # print(len(url_list))
    for url in url_list:
    # url = url_list[1]
        crawl_news(url)
