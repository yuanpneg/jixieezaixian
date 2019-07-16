import json
import pymongo
import requests
from requests import RequestException
import time

headers = {
    'Host': 'web.zhaozhonggong.com:443',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HUAWEI MLA-AL10 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

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


if __name__ == '__main__':
    data = {
        'projectName': '',
        'date': '1',
        'month': '',
        'begin_time': '',
        'end_time': '',
        'dealType': 'Deal_Type1',
        'noticType': '1+',
        'area': '',
        'huanJie': 'NOTICE',
        'pageIndex': '1'
    }

    url = 'http://www.sqggzy.com/spweb/HNSQ/TradeCenter/ColTableInfo.do'
    html = get_page_index(url, data)
    print(html)
