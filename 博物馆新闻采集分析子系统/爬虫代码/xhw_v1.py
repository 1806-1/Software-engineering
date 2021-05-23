import requests
import json
from bs4 import BeautifulSoup


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


def crawl_news(url_list, keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/67.0.3396.99 Safari/537.36"
    }
    
    all_news = {}
    all_news["name"] = keyword
    all_news["data"] = []
    all_news["valid_num"] = 0  # 有效新闻的数量
    titles = []  # 有些新闻是重复的，要去重
    
    for url in url_list:

        try:
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, "lxml")

            # 主站新闻都是这个格式，跳过地方频道、视频新闻
            head_line = soup.find("div", class_="head-line")
            if head_line is None:
                continue
            h1 = head_line.find_next("h1")
            if h1 is None:
                continue

            # 主站新闻可以进行到这一步
            # 取标题
            title = h1.find_next("span").text.replace("\n", "").replace('\r', "")
            # 去重
            if title in titles:
                continue
            print(title)
            titles.append(title)

            # 取日期
            header_time = soup.find("div", class_="header-time")
            year = header_time.find("span", class_="year").find("em").text.replace("\n", "").replace(" ", "")
            day = header_time.find("span", class_="day").text.replace(" ", "").split('/')
            date = year + "." + day[0] + "." + day[1]
            print(date)

            # 取新闻内容和图片
            content = []
            img = []
            ps = soup.find("div", id="detail").find_all("p")
            # 每段新闻在一对<p></p>标签之中，图片也位于<p></p>之中
            for p in ps:
                p_text = p.text.replace("\u3000", "").replace('\n', "").replace('\r', "").replace('\t', "").replace('\xa0', "")
                # 例子：暂时想不到更好的办法处理这个问题
                # （1）4月30日，工作人员在故宫博物院新陶瓷馆内观看展品。新华社记者 金良快 摄
                # （2）新华社记者金良快摄
                #   - 最后15个字符内含有“摄”以及“记者”，整段长度小于50（这段中“XX记者摄”所占比重过大）
                # （1）4月13日，观众在海南琼海的南海博物馆参观故宫博物院藏黄花梨沉香文物展。
                #   当日，“故宫·故乡·故事——故宫博物院藏黄花梨沉香文物展”在位于海南琼海的南海博物馆正式开展。
                #   本次展览精选70余件故宫博物院藏黄花梨家具与沉香器物，采用场景陈设与重点展示相结合的方式，
                #   凸显海南特色地域文化。 新华社记者 张丽芸 摄
                #   - 虽然最后15个字符内含有“摄”以及“记者”，但这么长一段还是比较重要的，不能删去
                if "摄" in p_text:
                    if len(p_text) < 50 and p_text.find("记者", -15):  
                        print("本段包含‘XXX摄影’等信息，已删去！")
                        continue
                content.append(p_text)

                # 直接通过.get("src")得到的不是完整地址，要和该页面url拼接，把最后一部分替换掉
                # 例子：
                # 新闻url：http://www.xinhuanet.com/expo/2021-04/14/c_1211110209.htm
                # p_img.get("src")：1211110209_16183683818691n.jpg
                # 图片地址：http://www.xinhuanet.com/expo/2021-04/14/1211110209_16183683818691n.jpg
                url_page = '/'.join(url.split('/')[:-1])
                p_imgs = p.find_all("img")
                for p_img in p_imgs:
                    img.append(url_page + '/' + p_img.get("src"))
                    print(p_img.get("src"))
            content = ''.join(content)

            news = {}
            news["url"] = url
            news["title"] = title
            news["date"] = date
            news["content"] = content
            news["img"] = img
            all_news["data"].append(news)
            all_news["valid_num"] += 1

        except Exception as e:
            print(e)
    valid_num = all_news["valid_num"]
    # 所谓“处理”就是过滤掉非主站新闻，因为非主站（地方频道、其他子频道）新闻的页面布局各不相同，一个个的话写时间成本高
    print(f"处理过后还剩{valid_num}条新闻  :(")
    print(all_news)
    with open(f"新华网_{keyword}.json", 'w', encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False)


if __name__ == "__main__":
    # keywords字典存放博物馆名字以及对应新闻的url列表
    keywords = {"故宫博物院": [], "首都博物馆": [], "中国科学技术馆": [], "中国地质博物馆": [], "中国人民革命军事博物馆": [],
                "中国航空博物馆": [], "中国国家博物馆": [], "北京自然博物馆": [], "上海博物馆": [], "南京博物院": []}
    for keyword in keywords.keys():
        for curPage in range(1, 6):  # 假定先爬1-5页
            # 新华网AJAX的请求地址
            origin_url = f"http://so.news.cn/getNews?keyword={keyword}&curPage={curPage}&sortField=0&searchFields=1&lang=cn"
            url_list = get_url_list(origin_url)
            if url_list is not None:
                keywords[keyword].extend(url_list)
        if len(keywords[keyword]) == 0:
            print(f"没有找到{keyword}的新闻  :(")
        else:
            print(f"共找到{len(keywords[keyword])}条关于{keyword}的新闻  :)")
            crawl_news(keywords[keyword], keyword)
