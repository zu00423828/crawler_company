import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import time

columns = ["name", "comp_id", "owner", "comp_phone", "comp_fax", "comp_address", "fact_phone",
           "fact_fax", "fact_address", "web_link", "property", "contect_mail", "employee", "keywords", ]
tw_keywords = ['地址', '電話', '傳真', '網址', '電子信箱', '負責人']
en_keywords = ['ADDRESS', 'TEL', 'FAX', 'WEB SITE', 'E-MAIL', 'PRESIDENT']


def info_process(info_urls, lang='tw'):
    # sess = requests.Session()
    # sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    rows = []
    seq = '：'
    keywords = tw_keywords

    if lang != 'tw':
        keywords = en_keywords
        seq = ':'
    for name, info_url in info_urls:
        row = {c: None for c in columns}
        time.sleep(2)
        res = session.get(f'{url_root}{info_url}')
        soup = Soup(res.text, 'lxml')
        try:
            desc_list = soup.find('div', class_='desc_html').find_all('li')
            d = {}
            for desc in desc_list:
                desc_text = desc.text
                for keyword in keywords:
                    if keyword in desc_text:
                        d[keyword] = desc_text.split(seq, 1)[-1].strip()
            for keyword in keywords:
                if keyword not in d.keys():
                    d[keyword] = None
                # address = desc[0].text.split(seq, 1)[-1].strip()
                # phone = desc[1].text.split(seq, 1)[-1].strip()
                # fax = desc[2].text.split(seq, 1)[-1].strip()
                # web = desc[3].text.split(seq, 1)[-1].strip()
                # email = desc[4].text.split(seq, 1)[-1].strip()
                # president = desc[5].text.split(seq, 1)[-1].strip()
            address, phone, fax, web, email, president = d[keywords[0]], d[keywords[1]
                                                                           ], d[keywords[2]], d[keywords[3]], d[keywords[4]], d[keywords[5]]
            product = soup.find_all('p', class_='txt-2')[1]
            products = product.text.strip()
            # print(name, address, phone, fax, web, email, president, keywords)
            row.update({'name': name, 'owner': president,
                        'comp_phone': phone, 'comp_fax': fax, 'comp_address': address, 'web_link': web, 'contect_mail': email, 'keywords': products})

            rows.append(row)
        except Exception as e:
            print(name, info_url, e)
    return rows


def crawler(url, lang='tw'):
    df = pd.DataFrame()
    info_links = []
    sum = 0
    for i in range(1, 15):
        res = session.get(f'{url}{i}')
        soup = Soup(res.text, "lxml")
        todo_list = soup.find_all('div',
                                  class_='toggle faq category01 category03 clearfix')
        sum += len(todo_list)
        for item in todo_list:
            info_link = item.find('a')
            info_links.append([info_link.text, info_link.get('href')])
            # print(info_link)
    print(sum)
    rows = info_process(info_links, lang)
    df = df.append(rows)
    print(columns, list(df.columns))
    df.to_excel(f'tfpma-{lang}.xlsx', index=False)


if __name__ == "__main__":
    url_root = 'http://www.tfpma.org.tw'
    tw_url = 'http://www.tfpma.org.tw/zh-TW/member/index.html?page='
    en_url = 'http://www.tfpma.org.tw/en/member/index.html?page='
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    crawler(tw_url, 'tw')
    crawler(en_url, 'en')
