# -*- coding:utf8 -*-
import MySQLdb
import os
import re
import sys
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup
import time
import json

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
# 1 - 网页分析
reload(sys)
sys.setdefaultencoding('utf-8')

# 2 - 网页信息获取函数
def get_per_page_info(url):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    request_index = urllib2.Request(url)
    request_index.add_header("User-Agent", agent)
    while 1 == 1:
        try:
            response2 = urllib2.urlopen(request_index, timeout=60)
            html = response2.read()
            break
        except Exception, e:
            print '请求超时,正在重新请求资源,若超时超过3分钟,请检查你的网络链接！'

    # 3 - 打开url的信息过滤
    html = html.replace('<br>', '')
    html = html.replace(' ', '')
    html = BeautifulSoup(html).__unicode__().decode('utf-8')

    # 4 - html源码信息(用于保存到数据库)
    html_info = html

    # 5 - html每行切分
    html = html.strip('\n')

    # 6 - 多行数据合并成一行,方便正则取值(用于保存到数据库)
    html = ' '.join(html.split())

    # 7 - 取出标签里的内容
    p_format = u">(.*?)<"
    p_format_complie = re.compile(p_format)
    result = p_format_complie.findall(html)

    result_delete_solve = []

    # 8 - 将取出的标签中的信息合成
    string = ''
    for i in range(len(result)):
        if (json.dumps(result[i], encoding='UTF-8', ensure_ascii=False) != '\"宋体\"'):
            result_delete_solve.append((json.dumps(result[i], encoding='UTF-8', ensure_ascii=False)))

    for i in range(len(result_delete_solve)):
        string = string + ' ' + result_delete_solve[i][1:len(result_delete_solve[i]) - 1]
        string = string.replace('&nbsp;', '')
        string = string.replace('  ', '')

    # 9 - 返回网页html源码和有效文字信息组成的列表
    info_list = [html_info, string]
    return info_list

