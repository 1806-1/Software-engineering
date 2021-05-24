import csv
import requests
from bs4 import BeautifulSoup
import xlwt

with open(r'C:\Users\chensihan\Desktop\百科.csv', 'r') as f:
    reader = csv.reader(f)
    iii=0
    f = open(r"C:\Users\chensihan\Desktop\百科链接ggbwy.csv", 'w', encoding='utf-8',newline="")
    for row in reader:
        iii = iii + 1
        if (iii > 1):
            print(row[1])
            url=row[1]
            hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}
            r = requests.get(url, headers=hdrs)
            soup = BeautifulSoup(r.content.decode('utf8', 'ignore'), 'lxml')
            rowDatas = []
            name = "00"
            # 博物馆基本信息

            for tag in soup.find_all('h1'):
                # print("sdgaha",tag.get_text(),"dfhzdhzrjt")
                name = tag.get_text()
                rowDatas.append(name)
                break;
            i = 0
            museum_address="  "
            for tag in soup.find_all('dl', class_='basicInfo-block basicInfo-left'):
                for tag in soup.find_all('dd', class_='basicInfo-item value'):
                    i = i + 1
                    if (i == 3):
                        museum = tag.get_text()
                        museum_address = museum

                        print(museum_address, "i=", i)
            rowDatas.append(museum_address)
            # 博物馆简介
            div_list = soup.find_all('div', class_='lemma-summary')
            intro = " "
            for each in div_list:
                introduce = each.text.strip()
                museum_introduce = introduce
                museum_introduce.replace('\n', '').replace('\r', '').replace(' ', '')
                for i in museum_introduce:
                    intro = intro + str(i)
                    intro.join(str(i))
                    # print(i)
                    if (i == "。"):
                        break;
            img = "00"
            div_list = soup.find_all('a', class_='image-link')
            for each in div_list:
                each.get_text()
                img = "https://baike.baidu.com" + each['href']
                print(img)
                print(type((each)))
                break;
            rowDatas.append(img)
            # if(each['class']=="lazy-img"):
            #     print(each['data-src'])
            #     break;

            # print("srthsh",intro,"tjstjs")
            rowDatas.append(intro)
            print(rowDatas)
            rowTitle = ['博物馆名称', '博物馆地址', '博物馆图片', '博物馆简介']
            import pandas as pd
            #dataframe = pd.DataFrame({'属性': rowTitle, '内容': rowDatas})

            csv_writer = csv.writer(f)

            csv_writer.writerow([rowDatas[0], rowDatas[1], rowDatas[2],rowDatas[3]])
    f.close()

