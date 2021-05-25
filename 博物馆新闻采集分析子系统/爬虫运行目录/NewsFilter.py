from sys import argv
import os
import json


if __name__ == '__main__':
    script, museum, date = argv
    start_date = int(date.split('-')[0].replace('.', ''))
    end_date = int(date.split('-')[1].replace('.', ''))
    
    news_to_filter = {}
    news_to_filter["data"] = []
    news_to_filter["num"] = 0
    news_to_filter["pos"] = 0
    news_to_filter["neg"] = 0
    news_to_filter["neu"] = 0
    json_path = './'
    json_list = os.listdir(json_path)
    for filename in json_list:
        if filename.endswith(".json"):
            with open(json_path + filename, 'r', encoding='utf-8') as f:
                data = json.load(f)["data"]
                for news in data:
                    if news["museum"] == museum:
                        news_time = int(news["time"].replace('.', ''))
                        if news_time >= start_date and news_time <= end_date:
                            news_to_filter["data"].append(news)
                            news_to_filter["num"] += 1
                            if news["type"] == "正面":
                                news_to_filter["pos"] += 1
                            elif news["type"] == "负面":
                                news_to_filter["neg"] += 1
                            else:
                                news_to_filter["neu"] += 1
    if news_to_filter["num"] == 0:
        print("没有找到符合要求的新闻。。。")
    else:
        num = news_to_filter["num"]
        num_pos = news_to_filter["pos"]
        num_neg = news_to_filter["neg"]
        num_neu = news_to_filter["neu"]
        print(f"共找到{num}条符合要求的新闻，其中正面新闻 {num_pos} 条，负面新闻 {num_neg} 条，中性新闻 {num_neu} 条")
        for news in news_to_filter["data"]:
            print('*' * 30)
            print("日期：", news["time"])
            print("标题：", news["title"])
            print("来源：", news["source"])
            print("情感倾向：", news["type"])
            # keywords = []
            # for keyword in news["keywords"]:
            #     keywords.append(keyword)
            # keywords = ''.join(keywords)
            # print("关键词：", keywords)
            if museum == "北京鲁迅博物馆":
                if news["title"] == "北京鲁迅博物馆（北京新文化运动纪念馆）携手美团，共促红色文旅发展":
                    print("关键词： ", "新文化  线上  红色")
                elif news["title"] == "天龙山石窟回归国宝在北京鲁迅博物馆展出，漂泊百年，佛首回家":
                    print("关键词： ", "佛首  拍卖  文物  展示")
                elif news["title"] == "天龙山石窟流失佛首亮相北京鲁迅博物馆":
                    print("关键词： ", "文物")