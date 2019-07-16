from urllib import parse

from recruit.config import *
import pymysql
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import time
from pyquery import PyQuery as pq
import random

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
cursor = conn.cursor()

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H734T8RC07W33G7D"
proxyPass = "90D30C8BC19B2430"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

headers = {
    'Cookie': COOKIE,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}


# 天眼查列表
def Tianyan(company, i):
    data = {
        'key': company,
        'base': 'xuzhou'  # 省份、城市名称
    }

    url = 'https://www.tianyancha.com/search/p' + str(i) + '?' + 'key='+parse.quote(company)+'&base=xuzhou' #urlencode(data)  %E8%B7%AF%E6%B2%BF%E7%9F%B3
    print(url)
    try:
        response = requests.get(url, headers=headers)
        r = random.randint(1, 3)
        print(r)
        time.sleep(r)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


# 获取详情页
def getDetail(url):
    try:
        response = requests.get(url, headers=headers)
        time.sleep(1)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('')
        return None


def findPhone():
    try:
        company_name = '路沿石'
        for i in range(1, 6):
            tianYanHtml = Tianyan(company_name, i)
            if tianYanHtml != None:
                tiYandq = pq(tianYanHtml)
                urls = tiYandq('.name')
                for href in urls.items():
                    #  获取电话
                    print(href.attr('href'))
                    detailhtml = getDetail(href.attr('href'))
                    doc = pq(detailhtml)
                    tel = doc('#company_web_top > div.box.-company-box > div.content > div.detail > '
                              'div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text()
                    print(tel)
                    if tel != '暂无信息' and len(tel) > 8:
                        name = doc('#company_web_top > div.box.-company-box > div.content > div.header > h1').text()
                        print(name)
                        address = doc('#company_web_top > div.box.-company-box > div.content > '
                                      'div.detail > div:nth-child(2) > div:nth-child(2)').text().split('地址：')[1]
                        print(address)
                        business_scope = doc('#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > '
                                             'tr:nth-child(10) > td:nth-child(2) > span > span > span.js-full-container.hidden').text()
                        print(business_scope)
                        sql = 'insert into tianyan_company(`name`, tel, address,description) values ("%s","%s","%s","%s")' % (name, str(tel), address.replace('"', ""), business_scope)
                        print(sql)
                        cursor.execute(sql)
                        conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        conn.close()
        print('存储到数据库失败')


if __name__ == '__main__':
    findPhone()
