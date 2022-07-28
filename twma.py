import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent

columns = ["name", "comp_id", "owner", "comp_phone", 'comp_fax', "comp_address", "fact_phone",
           "fact_fax", "fact_address", "web_link", "property", "contect_mail", "employee", "keywords"]

tw_keywords = ['負責人', '電話', '傳真', '地址', 'Email', '網址']
en_keywords = ['President', 'Tel', 'Fax', 'Address', 'Email', 'Web']


def process_info(info_list, lang='tw'):
    dict = {}
    keywords = tw_keywords
    if lang != 'tw':
        keywords = en_keywords
    if len(info_list) == 1:
        print('len', len(info_list))
        raise 'len is not enough'
    for item in info_list:
        item_text = item.text.strip()
        if keywords[1] in item_text:
            last_key = keywords[1]
            dict[last_key] = item_text.split('：')[1].strip()
        elif keywords[2] in item_text:
            last_key = keywords[2]
            dict[last_key] = item_text.split('：')[1].strip()
        elif keywords[3] in item_text:
            last_key = keywords[3]
            dict[last_key] = item_text.split('：')[1].strip()
        elif keywords[4] in item_text:
            last_key = keywords[4]
            dict[last_key] = item_text.split('：')[1].strip()
        elif keywords[5] in item_text:
            last_key = keywords[5]
            dict[last_key] = item_text.split('：')[1].strip()
        else:
            temp = item_text.strip()
            dict[last_key] = dict[last_key]+temp
            continue
        # diff_keys = set(tw_keywords[1:]) ^ set(dict.keys())
        # if diff_keys is not None:
        #     for diff_key in diff_keys:
        #         dict[diff_key] = None
        # # print(dict.values())
        # # print(dict.keys())
    for keyword in keywords[1:]:
        if keyword not in dict.keys():
            dict[keyword] = None
            print('not in keyword', keyword)

    return dict[keywords[1]], dict[keywords[2]], dict[keywords[3]], dict[keywords[4]], dict[keywords[5]]


def driver_init():
    options = ChromeOptions()
    options.add_argument("headless")
    s = Service("/home/yuan/桌面/tempcode/crawler_ettody/chromedriver")
    browser = Chrome(
        service=s, options=options)
    return browser


def crawler_info(info_links, lang='tw'):

    lang_key = True if lang == 'tw' else False
    rows = []
    element_index = [4, 6, 12]
    if lang != 'tw':
        element_index = [8, 10, 14]
    for link in info_links:
        row = {c: None for c in columns}

        res = sess.get(link)
        soup = Soup(res.text, 'lxml')
        # print(link)
        name_list = soup.find_all('div', class_='_1KV2M')
        try:
            name_list = name_list[5].find_all(
                'span')  # chinses name english name
            name_list = set([name.text for name in name_list])
            name = [name for name in name_list if name.isalpha() ==
                    lang_key][-1]
            find_element = soup.find_all(
                class_='_1Q9if _3bcaz')
            basic_info = find_element[element_index[0]].find_all('h3')
            president = basic_info[1].text.split(
                '：', 1)[-1].strip()  # president
            Information = find_element[element_index[1]].find_all('h3')
            phone, fax, address, email, web = process_info(
                Information, lang=lang)
            product_info = find_element[element_index[2]].find_all(
                'h2', class_='font_2')
            text_list = [temp.text for temp in product_info]
            product = '、'.join(text_list)
            d = {'name': name, 'owner': president, "comp_phone": phone, "comp_address": address, "comp_fax": fax,
                 'web_link': web, 'contect_mail': email, 'keywords': product}
            row.update(d)
            rows.append(row)
        except Exception as e:
            print(link, e)
    # print(rows)
    return rows


def crawler(url):
    tw_df = pd.DataFrame()
    en_df = pd.DataFrame()
    page_list = ['members-a-to-e-tw', 'members-f-to-j-tw',
                 'members-k-to-o-tw', 'members-p-to-t-tw', 'members-u-to-z-tw']
    href_list = []
    for page in page_list:
        print(f'{url}/{page}')
        response = sess.get(f'{url}/{page}')
        soup = Soup(response.text, 'lxml')
        todo_list = soup.find_all(class_='_1BGyP _3D_sI')
        for item in todo_list:
            try:
                href = item.find('a').get('href')
                href_list.append(href)
            except Exception as e:
                print(e)
    print(len(href_list))
    rows = crawler_info(href_list)
    tw_df = tw_df.append(rows)
    tw_df.to_excel('twma_tw.xlsx', index=False)
    rows = crawler_info(href_list, 'en')
    en_df = en_df.append(rows)
    en_df.to_excel('twma_en.xlsx', index=False)


if __name__ == "__main__":
    url = 'https://www.twma.org.tw/'
    sess = requests.Session()
    ua = UserAgent()
    sess.headers['user-agent'] = ua.google
    crawler(url)
    # url = 'https://www.twma.org.tw/unitek-machinery'
    # res = sess.get(url)
