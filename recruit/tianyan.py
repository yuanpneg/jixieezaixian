from recruit.config import *
import pymysql
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import time
from pyquery import PyQuery as pq
import random
from ipdb import set_trace

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
COOKIE = COOKIE
headers = {
    'Cookie': COOKIE,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}


def Tianyan(company):
    data = {
        'key': company
    }

    url = 'https://www.tianyancha.com/search?' + urlencode(data)

    try:
        response = requests.get(url, headers=headers)
        r = random.randint(1, 2)
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

        find_all_company = 'select distinct company from tp_job_recruit_6 where telephone is null or  telephone = "" or telephone = "None"'
        cursor.execute(find_all_company)
        for company in cursor.fetchall():
            company_name = company[0]
            tianYanHtml = Tianyan(company_name)
            if tianYanHtml != None:
                tiYandq = pq(tianYanHtml)
                if tiYandq == None:
                    continue
                #  获取href
                href = tiYandq('.name').attr('href')
                if href != None:
                    detailhtml = getDetail(href)
                    if detailhtml == None:
                        continue
                    doc = pq(detailhtml)
                    telephone = doc('#company_web_top > div.box.-company-box > div.content > div.detail > '
                                    'div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text()
                    # 修改数据库中的电话
                    if telephone == '暂无数据' or telephone == None or len(telephone) <= 8 or len(telephone) > 13:
                        telephone = '0516-61230688'
                        print('默认电话')
                    print(telephone)
                    update_telephone = 'update tp_job_recruit_6 set telephone = SUBSTRING_INDEX( "%s" ,"-",2) where company = "%s" ' % (
                        telephone, company_name)
                    cursor.execute(update_telephone)
                    conn.commit()
                else:
                    set_trace()  # 设置断点
    except Exception as e:
        print(e.args)
        conn.rollback()
        conn.close()
        print('存储到数据库失败')


# 从本地建筑公司修改电话
def updatePhone():
    find_all_company = 'select distinct company from tp_job_recruit_6 where telephone = "" or telephone is  null '
    cursor.execute(find_all_company)
    for company in cursor.fetchall():
        company_name = company[0]
        is_jude_company = 'select telephone from tp_company where company ="%s"' % (company_name)
        cursor.execute(is_jude_company)
        is_null = cursor.fetchone()
        if is_null != None:
            telephone = is_null[0]
            update_telephone = 'update tp_job_recruit_6 set telephone =SUBSTRING_INDEX( "%s" ,"-",2) where company = "%s" ' % (
                telephone, company_name)
            cursor.execute(update_telephone)
            conn.commit()


if __name__ == '__main__':
    #updatePhone()
    findPhone()
