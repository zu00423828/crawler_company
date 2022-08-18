import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
from fake_useragent import UserAgent
import time
# year select option key value
years = {2021: 20, 2020: 14, 2019: 13, 2018: 12, 2017: 11, 2016: 10, 2015: 9, 2014: 8, 2013: 7, 2012: 6,
         2011: 5, 2010: 4, 2009: 3, 2008: 2, 2007: 1, 2006: 15, 2005: 16, 2004: 17, 2003: 18, 2002: 19}

url_list = []


def crawler_info(sess: requests.Session, url: str):
    response = sess.get(url)
    soup = Soup(response.text, 'lxml')
    year = soup.find(class_='detailPanl--year green').text.strip()
    industry = soup.find(class_='detailPanl--type muted-7').text.strip()
    company_name = soup.find(
        class_='detailPanl--info flex fd-c').find('h3').text.strip()
    print(year, industry, company_name)
    return company_name, industry, year


def crawler(sess: requests.Session, base_url: str):
    df = pd.DataFrame()
    for key, item in years.items():
        rows = []
        for page in range(1, 3):
            url = base_url+f'year={item}&type=all&page={page}'
            print(url)
            response = sess.get(url)
            soup = Soup(response.text, 'lxml')
            todo_list = soup.find_all(class_='m-card bg-white m-card-company')
            for todo_item in todo_list:
                item_url = todo_item.find('a').get('href')
                name, industry, year = crawler_info(sess, item_url)
                rows.append({'name': name, 'industry': industry, 'year': year})
                time.sleep(0.1)
        df = df.append(rows)
    df.to_excel('idipc.xlsx', index=False)


if __name__ == "__main__":
    base_url = 'https://www.idipc.org.tw/golden/award?'
    sess = requests.Session()
    ua = UserAgent()
    sess.headers['user-agent'] = ua.google
    crawler(sess, base_url)
