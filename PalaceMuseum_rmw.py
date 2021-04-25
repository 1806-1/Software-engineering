import json
import re
import requests
import datetime
import os
from bs4 import BeautifulSoup


def crawl_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36",
    }
    url = "http://bj.people.com.cn/n2/2021/0320/c82846-34631893.html"
    info = {}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "lxml")

        title_h1 = soup.find("h1")
        print("标题：" + title_h1.text)

        box_01 = soup.select_one(".box01")
        date_source = box_01.find_next("div", class_="fl").text
        date = date_source.split("来源：")[0]
        source = date_source.split("来源：")[1]
        print("日期：" + date)
        print("来源：" + source)

        content = []
        box_con = soup.select_one(".box_con")
        p_all = box_con.find_all("p")
        for p in p_all:
            content.append(p.text.replace("\n\t\u3000\u3000", ""))
        print(content)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    crawl_news()

