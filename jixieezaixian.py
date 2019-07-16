import json
import os
import hashlib
import pymongo
import requests
from requests import RequestException
import time

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '83',
    'Host': 'www.tgj168.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/2.5.0'

}


def get_page_index(url, data):
    try:
        # time.sleep(4)
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 503:
            get_page_index(url, data)
        if response.status_code == 200:
            if response.text == None:
                get_page_index(url, data)
            return str(response.text)

    except RequestException:
        print('请求目录页失败')


def get_page_detail(url, detail_data):
    try:
        # time.sleep(4)
        response = requests.post(url=url, data=detail_data, headers=headers)
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
        url = "http://www.tgj168.com/index.php?d=api&c=saas_square_info_all&m=info_page"
        detail_url = "http://www.tgj168.com/index.php?d=api&c=saas_square_info_all&m=info_byid"
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        collection = db.jiexieezaixian
        for page in range(1, 3000):
            data = {
                'page': page,
                'type': '11',
                'dataType': 'json',
                'dataFrom': 'eonline'
            }
            htmls = get_page_index(url, data)
            if htmls == None or htmls == '':
                continue
            datas = json.loads(htmls)['data']
            rows = datas['rows']
            for data in rows:
                id = data['infoid']
                detail_data = {
                    'infoid': id,
                    'dataType': 'json',
                    'dataFrom': 'eonline'
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
