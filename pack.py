import requests
from urllib.parse import quote
from bs4 import BeautifulSoup as Soup
import pandas as pd
from fake_useragent import UserAgent
import pandas as pd
columns = ["name", "comp_id", "owner", "comp_phone", 'comp_fax', "comp_address", "fact_phone",
           "fact_fax", "fact_address", "web_link", "property", "contect_mail", "employee", "keywords"]

tw_keywords = ['公司電話', '公司傳真', '公司地址', '公司網址', '電子信箱', '主要產品']
en_keywords = ['Phone', 'Fax', 'Address', 'Website', 'Email', 'Product']


def crawler_info(url, lang='tw'):
    keywords = tw_keywords
    if lang != 'tw':
        keywords = en_keywords
    res = sess.get(url)
    soup = Soup(res.text, 'lxml')
    name = soup.find(class_='titStyle1').text.strip()
    info_list = soup.find('div', class_='pITR_remark').find_all('span')
    d = {}
    for info in info_list:
        for keyword in keywords:
            if keyword in info.get('data-name'):
                d[keyword] = info.text.strip()
    for keyword in keywords:
        if keyword not in d.keys():
            d[keyword] = None
    return name, d[keywords[0]], d[keywords[1]], d[keywords[2]], d[keywords[3]], d[keywords[4]], d[keywords[5]]


def crawler(url, lang='tw'):
    link_root = 'https://www.pack.org.tw/web/directory/directory_in.jsp'
    df = pd.DataFrame()
    # group member
    for page in range(1, 22):
        payload = {"npage": page,
                   "dm_no": "DM1576547679368",
                   "sp_type": "group",
                   "sp_lang": lang}
        res = sess.post(url, data=payload)
        soup = Soup(res.text, 'lxml')
        directory_list = soup.find_all('div', class_='directory_list')
        rows = []
        for directory in directory_list:
            row = {c: None for c in columns}
            href = directory.find('a').get(
                'href').split('directory_in.jsp')[-1]
            full_href = quote(link_root+href, safe=';/?.:@&=+$,')
            name, phone, fax, address, website, email, product = crawler_info(
                full_href, lang=lang)
            row.update({'name': name, 'comp_phone': phone, 'comp_fax': fax, 'comp_address': address,
                       'web_link': website, 'contect_mail': email, 'keyword': product})
            rows.append(row)
        df = df.append(rows)
    # # spnsor member
    # url = f'https://www.pack.org.tw/web/directory/directory.jsp?lang={lang}&sp_type=sponsor'
    # res = sess.get(url)
    # soup = Soup(res.text, 'lxml')
    # rows = []
    # for directory in directory_list:
    #     row = {c: None for c in columns}
    #     href = directory.find('a').get(
    #         'href').split('directory_in.jsp')[-1]
    #     full_href = quote(link_root+href, safe=';/?.:@&=+$,')
    #     name, phone, fax, address, website, email, product = crawler_info(
    #         full_href)
    #     row.update({'name': name, 'comp_phone': phone, 'comp_fax': fax, 'comp_address': address,
    #                 'web_link': website, 'contect_mail': email, 'keyword': product})
    #     rows.append(row)
    # df = df.append(rows)
    df.to_excel(f'pack-{lang}.xlsx', index=False)


if __name__ == '__main__':
    tw_url = 'https://www.pack.org.tw/web/directory/directory.jsp?sp_type=group&lang=tw'
    en_url = 'https://www.pack.org.tw/web/directory/directory.jsp?sp_type=group&lang=en'
    # url = 'https://www.pack.org.tw/web/directory/directory.jsp'
    sess = requests.Session()
    ua = UserAgent()
    sess.headers["user-agent"] = ua.google
    crawler(tw_url, 'tw')
    crawler(en_url, 'en')
