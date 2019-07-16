import json
import os
from _md5 import md5

import pymongo
import requests
from requests import RequestException
import time

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '35',
    'Host': 'www.baobaojixie.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10)'

}

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


def get_page_index(url, data):
    try:
        time.sleep(4)
        response = requests.post(url, data=data, headers=headers, proxies=proxies)
        if response.status_code == 503:
            get_page_index(url, data)
        if response.status_code == 200:
            if response.text == None:
                get_page_index(url, data)
            return str(response.text)

    except RequestException:
        print('请求目录页失败')


# def parse_page_index(html):
#     data = json.loads(html)
#     indexDataList = data['result']['dataList']
#     for item in indexDataList:
#         id = item['id']
#         yield id


def get_page_detail(url, detail_data):
    try:
        time.sleep(4)
        response = requests.post(url=url, data=detail_data, headers=headers, proxies=proxies)

        print(response.status_code)
        if response.status_code == 503:
            get_page_detail(url, detail_data)
        if response.status_code == 200:
            if response.text == None:
                get_page_detail(url, detail_data)
            return str(response.text)
        return ''
    except RequestException:
        print('请求详情页失败')


def main():
    try:
        url = "http://www.baobaojixie.com/api/rental/rentalList "
        detail_url = "http://www.baobaojixie.com/api/rental/rentalDetail"
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        collection = db.equipment
        for page in range(1, 3000):
            data = {
                'page': page,
                'member_id': '-1'
            }
            htmls = get_page_index(url, data)
            if htmls == None or htmls == '':
                continue
            datas = json.loads(htmls)['data']
            for data in datas:
                id = data['id']
                detail_data = {
                    'id': id,
                    'member_id': '-1'
                }
                # print(detail_url)
                html = get_page_detail(detail_url, detail_data)
                if html != None and html != '':
                    machine = json.loads(html)['data']
                    string = 'jixieezaixian_' + str(id)
                    mach = dict(machine)
                    mach['dsj_id'] = string
                    print(mach)
                    collection.insert(mach)
                else:
                    continue
    except RequestException:
        print('请求详情页失败')


if __name__ == '__main__':
    main()
