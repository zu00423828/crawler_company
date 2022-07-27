import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd


columns = ["name", "comp_id", "owner", "comp_phone", "comp_address", "fact_phone",
           "fact_fax", "fact_address", "web_link", "property", "contect_mail", "employee", "keywords", ]

tw_keywords = ['聯絡地址：', '聯絡電話：', '傳真：', '生產項目：']
en_keywords = ['Address：', 'Tel：', 'Fax：', 'Product：']


def crawler(url, lang='tw'):
    df = pd.DataFrame()
    keywords = tw_keywords
    if lang == 'en':
        keywords = en_keywords
    for i in range(1, 78):
        res = requests.get(f'{url}{i}')
        soup = Soup(res.text, "lxml")
        todo_list = soup.find_all(class_='search__item hover-1')
        for item in todo_list:
            d = {c: None for c in columns}
            name = item.find(class_='search-com-name').text.strip()
            d.update({'name': name})
            info = item.find_all(class_='search-info')
            for information in info:
                info_rows = information.find_all('div')
                for info_row in info_rows:
                    if keywords[0] in info_row.text:
                        address = info_row.text.split("：")[-1]
                        d.update({"comp_address": address,
                                 "fact_address": address})
                    if keywords[1] in info_row.text:
                        phone = info_row.text.split("：")[-1]
                        d.update({"comp_phone": phone, "fact_phone": phone})
                    if keywords[2] in info_row.text:
                        fax = info_row.text.split("：")[-1]
                        d.update({"fact_fax": fax})
                    if keywords[3] in info_row.text:
                        product = info_row.text.split("：")[-1]
                        d.update({"keywords": product})
            email = item.find_all('a')[0].get('href')
            web_link = item.find_all('a')[-1].get('href')
            if len(web_link) < 10:
                web_link = None
            d.update({'contect_mail': email})
            d.update({'web_link': web_link})
            df = df.append([d])

    df.to_excel(f'tmba-{lang}.xlsx', index=False, columns=columns)


if __name__ == "__main__":
    url = 'https://www.tmba.org.tw/zh-TW/member-search?page='
    url = 'https://www.tmba.org.tw/en/member-search?page='
    crawler(url, 'en')
    crawler(url, 'tw')
