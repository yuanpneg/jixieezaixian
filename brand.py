import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from recruit.config import *
import pymysql

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}


def get_urls_detail(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        print(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


if __name__ == '__main__':
    try:
        urls = ['https://www.china-10.com/?action=getbelow&catid=57&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=58&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=59&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=55&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=2990&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=51&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=5075&pac=brand10&pnum=12',
                'https://www.china-10.com/?action=getbelow&catid=51&pac=brand10&pnum=11',
                'https://www.china-10.com/?action=getbelow&catid=5075&pac=brand10&pnum=11',
                'https://www.china-10.com/?action=getbelow&catid=55&pac=brand10&pnum=11',
                'https://www.china-10.com/?action=getbelow&catid=59&pac=brand10&pnum=11',
                'https://www.china-10.com/?action=getbelow&catid=54&pac=brand10&pnum=11',
                'https://www.china-10.com/?action=getbelow&catid=5075&pac=brand10&pnum=11',
                'https://www.china-10.com/?action=getbelow&catid=51&pac=brand10&pnum=11']
        for url in urls:
            list_urls = pq(get_urls_detail(url))
            hrefs = list_urls('a')
            for href in hrefs.items():
                print('https:' + href.attr('href'))
                cattitle = href.text()
                detail_html = pq(get_urls_detail('https:' + href.attr('href')))
                shops = detail_html('.brandbox')
                for shop in shops.items():
                    shop_detail = pq(shop)
                    shop_name = shop_detail('div.brandinfo > dl > dt > a').text()[0:30]
                    shop_info = shop_detail('div.brandinfo').text().replace('"', "").replace('\n', "")
                    insert_sql = 'insert into goods_brand(shop_name,shop_info,cattitle) values ( "%s","%s","%s")' % (
                        shop_name, shop_info, cattitle)
                    cursor.execute(insert_sql)
                    conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        print('存储到数据库失败')
