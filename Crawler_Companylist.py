# -*- coding: utf-8 -*-
import json
import requests
import random
import string
import logging
import time
import chardet
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


def Get_next_page(session_crawl, current_page):

    post_header = {
        'ACTIONID':7,
        'AJAX':'AJAX-TRUE',
        'CATALOGID':'1743_zb',
        'TABKEY':'tab1',
        'tab1PAGENO':int(current_page) + 1,
        'tab1PAGECOUNT':48,
        'tab1RECORDCOUNT':476,
        'REPORT_ACTION':'navigate'
    }

    request_url = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.8722948465900369'

    req = Crawler_session.post(request_url, params=post_header)
    # print(req)
    req.encoding = 'gb18030'

    req_text = req.text

    return req_text

def Parse_table_row(line, date_info, page_info):

    new_line = [date_info, page_info]
    for item in line:
        if isinstance(item,list) and len(item) == 1:
            new_line.append(item[0])
        elif isinstance(item,list) and len(item) == 0:
            new_line.append("")
        elif isinstance(item,list) and len(item) >1:
            #print(item)
            new_line.append(list(filter(lambda x: x if x !=' ' else None, item))[0])
    return new_line
#
# def Get_page_num(html_text):
#
#     current_page_num = ""
#     page_num_begin = html_text.index("当前第") + 3
#     print(page_num_begin, html_text[page_num_begin])
#
#     while True:
#         if html_text[page_num_begin].isdigit():
#             current_page_num = current_page_num + html_text[page_num_begin]
#             page_num_begin = page_num_begin + 1
#         else:
#             break
#
#     print(current_page_num)
#     return current_page_num

def Get_total_page(html_text):

    page_num_begin = html_text.index("当前第")
    page_string = html_text[page_num_begin:page_num_begin + 20]
    re_words = re.compile(r"\d+")
    page_string = re.findall(re_words, page_string)
    # print(page_string)

    current_page, total_page = page_string
    # print(current_page, total_page)

    return current_page, total_page


def Get_update_date(html_text):

    html_parser_str = BeautifulSoup(html_text, "html.parser")

    date_data = html_parser_str.findAll('span', {"class": 'cls-subtitle'})

    return date_data[0].text.strip()

def Get_table_from_page(released_date, current_page, html_data):

    html_parser_str = BeautifulSoup(html_data, "html.parser")
    table = html_parser_str.findAll('table', {"class": 'cls-data-table-common cls-data-table'})

    table = table[0]

    rows = table.findAll('tr')
    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]

    for item in data:
        if len(item) == 6:
            new_line = Parse_table_row(item,released_date, current_page)
            new_line = ",".join(new_line)

            yield new_line


if __name__ == '__main__':


    Crawler_session = requests.Session()


    get_header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                  'Upgrade-Insecure-Requests' : 1,
                  'Host':'www.szse.cn',
                  'Connection':'keep-alive',
                  'Cache-Control':'max-age=0'}

    get_url = 'http://www.szse.cn/main/mainboard/ssgsxx/ssgslb/'

    req = Crawler_session.get(get_url, params = get_header)
    req.encoding='gb18030'

    req_text = req.text

    bsObja=BeautifulSoup(req_text,"html.parser")
    table = bsObja.findAll('table',{"class":'cls-data-table-common cls-data-table'})

    released_date = Get_update_date(req_text)
    _, total_page = Get_total_page(req.text)


    f = open('crawler_company_info.csv','w+')

    current_page = 0

    while int(current_page) < int(total_page):

        print(current_page, total_page)

        req_text = Get_next_page(Crawler_session, current_page)
        released_date = Get_update_date(req_text)
        current_page, total_page = Get_total_page(req_text)
        table_lines = Get_table_from_page(released_date, current_page, req_text)

        for new_line in table_lines:
            print(new_line, end="\n", file=f)

        time.sleep(2)

    f.close()
