from urllib.parse import urlencode
import requests
from requests import RequestException
from pyquery import PyQuery as pq
import time
import random


def Tianyan(company, cookie, page):
    proxies = {
        'http': 'http://46.101.145.206:3128'
    }
    data = {
        'key': company
    }
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    url = 'https://www.tianyancha.com/search/p' + str(page) + '?' + urlencode(data)
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


if __name__ == '__main__':
    cookie = 'TYCID=cf2e5060781711e88d7e391fdfc48f53; undefined=cf2e5060781711e88d7e391fdfc48f53; ssuid=4376321506; _ga=GA1.2.2007233096.1535090125; aliyungf_tc=AQAAADx6q2IxWQYAWmVotOze+8CLGCIa; csrfToken=wrG8TKQ0C9YhwbnpJ89UKrwD; __insp_wid=677961980; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20v; __insp_targlpt=5aSp55y85p_lLeS6uuS6uumDveWcqOeUqOWVhuS4muWuieWFqOW3peWFt1%2FkvIHkuJrkv6Hmga%2Fmn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol%2FkvIHkuJrkv6HnlKjkv6Hmga%2Fmn6Xor6Lns7vnu58%3D; _gid=GA1.2.1119874094.1546845841; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1546845841; __insp_norec_sess=true; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E8%25BF%2588%25E5%2585%258B%25E5%25B0%2594%25C2%25B7%25E6%259B%25BC%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%2522126%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk1MjE1MjE0NiIsImlhdCI6MTU0Njg0Njc1NCwiZXhwIjoxNTYyMzk4NzU0fQ.Dn7ByBXRJVd4d5-DKzsXPV8lElFPe1OBQKaa-iu1THGRhcmDyuquojkE2CMhlR17n7u8TDEB59248OpU66hyqQ%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213952152146%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk1MjE1MjE0NiIsImlhdCI6MTU0Njg0Njc1NCwiZXhwIjoxNTYyMzk4NzU0fQ.Dn7ByBXRJVd4d5-DKzsXPV8lElFPe1OBQKaa-iu1THGRhcmDyuquojkE2CMhlR17n7u8TDEB59248OpU66hyqQ; __insp_slim=1546846764724; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1546846767'
    for page in range(1, 10):
        sleep_time = random.randint(2, 6)
        time.sleep(sleep_time)
        html = Tianyan('工程机械租赁', cookie, page)
        doc = pq(html)
        list = doc('')

        print(html)
