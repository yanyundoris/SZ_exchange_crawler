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


def Get_all_company_code():
    company_code = pd.read_csv('/Users/yanyunliu/PycharmProjects/CodingTest/GekkoAI/crawler_company.csv',header=None,dtype={2:str})
    company_code = company_code[2].values.tolist()

    return company_code


def Get_total_page(html_text):

    page_num_begin = html_text.index("当前第")
    page_string = html_text[page_num_begin:page_num_begin + 40]
    re_words = re.compile(r"\d+")
    page_string = re.findall(re_words, page_string)
    # print(page_string)

    current_page, total_page = page_string
    # print(current_page, total_page)

    return current_page, total_page

def Get_notice_type(html_text):

    notice_dict = {}

    bsObja = BeautifulSoup(html_text, "html.parser")
    table = bsObja.findAll('select', {"name": 'noticeType'})

    for item in table:
        # print(item)
        # print(item.find_all(value=True, text=True), item.findAll(text=True), type(item))

        sub_item = item.find_all(value=True, text=True)
        for line in sub_item:
            # print(line, line['value'], line.contents)
            if line['value'] != "":
                notice_dict[line['value']] = line.contents[0]

    # print(notice_dict)

    return notice_dict


def Get_post_formfield(notice_type_code= None, company_code = '000001',page_num = 1):


    get_header = {
        'leftid': 1,
        'lmid': 'drgg',
        'pageNo': page_num,
        'noticeType':notice_type_code,
        'stockCode': company_code,
        'startTime': '2015-01-01',
        'endTime': '2017-11-20',
        'imageField.x': 39,
        'imageField.y': 7
    }

    return get_header


def Parse_notice_html(notice_code, notice_dict, company_code, html_text):


    notice_list = []
    notice_count = {}

    notice_count[company_code + "_" + notice_code] = 0

    if '没有找到你搜索的公告!' in html_text:
        pass
    else:
        html_parser_str = BeautifulSoup(html_text, "html.parser")
        table = html_parser_str.find_all('td',{"class":"td2"})


        # print(table)

        for item in table:
            # print(item)
            # print(item.find(target="new", text = True).contents, item.find("span", {"class":"link1"},text = True).contents, len(item.get_text()))
            new_line = [str(company_code),str(notice_code), "'"+item.find(target="new", text = True).contents[0]+"'", item.find("span", {"class":"link1"},text = True).contents[0].replace("[","").replace("]",""), notice_dict[notice_code]]
            new_line = ",".join(new_line)
            notice_count[company_code + "_" + notice_code] += 1
            # print(notice_count[company_code + "_" + notice_code])
            print(new_line)

            notice_list.append(new_line)

            # yield new_line

    return notice_list

def Get_post_header(Cookie_random = 'C44615BFDF9D365DB85EC9D47ED69B3B'):

    Cookie_random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))

    post_header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache - Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':142,
        'Content - Type':'application/x-www-form-urlencoded',
        'Cookie':'JSESSIONID=' + Cookie_random,
        'Host':'disclosure.szse.cn',
        'Origin':'http://disclosure.szse.cn',
        'Referer':'http://disclosure.szse.cn/m/search0425.jsp',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    return post_header






if __name__ == '__main__':

    break_at = '000001'


    Crawler_session = requests.Session()

    adapter = requests.adapters.HTTPAdapter(max_retries=20)
    Crawler_session.mount('https://', adapter)
    Crawler_session.mount('http://', adapter)


    post_header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache - Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':142,
        'Content - Type':'application/x-www-form-urlencoded',
        'Cookie':'JSESSIONID=C44615BFDF9D365DB85EC9D47ED69B3B',
        'Host':'disclosure.szse.cn',
        'Origin':'http://disclosure.szse.cn',
        'Referer':'http://disclosure.szse.cn/m/search0425.jsp',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    Notice_type_code = None

    get_header = {
        'leftid': 1,
        'lmid': 'drgg',
        'pageNo': 1,
        'noticeType':Notice_type_code,
        'stockCode': '000001',
        'startTime': '2015-01-01',
        'endTime': '2017-11-20',
        'imageField.x': 39,
        'imageField.y': 7
    }

    # get_url = 'http://www.szse.cn/main/mainboard/ssgsxx/ssgslb/'
    # get_url = 'http://disclosure.szse.cn/m/szmb/drgg.htm'
    get_url = 'http://disclosure.szse.cn/m/search0425.jsp'

    req = Crawler_session.post(get_url, data=get_header,params=post_header)  # .text.encode("utf-8").decode("GBK").encode("utf-8")
    req.encoding = 'gb18030'


    req_text = req.text

    current_page, total_page = Get_total_page(req_text)


    notice_value = Get_notice_type(req_text)
    company_list = Get_all_company_code()

    f = open('crawler_notice_full.csv','w+')


    for company_id in company_list:

        if company_id < break_at:
            print('skip', company_id)

        if company_id >= break_at:

            for key, value in notice_value.items():
                for i in range(0,3):
                    try:
                        req = Crawler_session.post(get_url, data=Get_post_formfield(key, company_code=company_id),
                                                   params=post_header)
                    except:
                        print('error')
                        time.sleep(20)
                        Crawler_session = requests.Session()
                        req = Crawler_session.post(get_url, data=Get_post_formfield(key, company_code=company_id),
                                                   params=Get_post_header())  # .text.encode("utf-8").decode("GBK").encode("utf-8")

                    break


                req.encoding = 'gb18030'

                req_text = req.text
                _, total_page = Get_total_page(req_text)

                current_page = 0
                print(key, value)

                while int(current_page) < int(total_page):

                    for i in range(0, 3):

                        try:
                            req = Crawler_session.post(get_url, data=Get_post_formfield(key, company_code=company_id, page_num=current_page + 1),
                                                       params=post_header)  # .text.encode("utf-8").decode("GBK").encode("utf-8")
                        except:
                            print('error')
                            time.sleep(20)
                            Crawler_session = requests.Session()
                            req = Crawler_session.post(get_url, data=Get_post_formfield(key, company_code=company_id, page_num=current_page + 1),
                                                       params=Get_post_header())  # .text.encode("utf-8").decode("GBK").encode("utf-8"

                        break

                    req.encoding = 'gb18030'

                    req_text = req.text

                    notice_list = Parse_notice_html(key, notice_value, company_id, req_text)

                    for item in notice_list:
                        print(item, end="\n", file=f)

                    print(current_page, total_page)

                    current_page = int(current_page) + 1

                    time.sleep(2)

    f.close()



