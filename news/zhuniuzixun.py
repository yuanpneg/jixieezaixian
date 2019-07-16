import requests
from pyquery import PyQuery as pq
import time
from news.MysqlHelper import MysqlHelper
import json
import datetime

# 筑牛资讯 修改完成
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'news.zhuniu.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie': 'JSESSIONID=5AA2299D346C13463C7FD86E69D5DA8C; Hm_lvt_e054c37a477ae164181ad14c7464b716=1549076893; Hm_lpvt_e054c37a477ae164181ad14c7464b716=1549076893'
}


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


# 获取详情页
def get_detail(url, title, mh):
    try:
        response = requests.get(url, headers=headers)
        doc = pq(response.text)
        type = '新闻资讯'
        content = doc.find('.zn-f16').text()
        content_html = doc.find('.zn-f16').find('p')
        content_htmls = str(content_html).replace('"', '')

        release_time = doc.find('.zn-f14').text().split(" ")[0]
        yesterday = getYesterday()
        if release_time == str(yesterday):
            if title != '' and title != None:
                sql = 'insert into tp_news (content, contentHtml, img, pudate, title, `type` ,url) values  \
                          ("%s", "%s", "%s", "%s", "%s","%s", "%s")' % (
                    content, content_htmls, '', release_time, title, type, url)
                mh.cud(sql)
    except Exception as e:
        print(e)
        print('请求目录页失败')


def get_page_index(url, data):
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        print('请求目录页失败')


def main():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')

    for page in range(1, 8):
        if page == 1:
            url = 'http://news.zhuniu.com/redian'
            response = requests.get(url)
            doc = pq(response.text)
            urls = doc.find('.item h3 a')
            for hrefs in urls.items():
                href = 'http://news.zhuniu.com/' + hrefs.attr('href')
                title = hrefs.text()
                print(href + "  " + title)
                get_detail(href, title, mh)
        else:
            url = 'http://news.zhuniu.com/ajaxList/redian'
            data = {
                'pageIndex': page,
                'pageSize': 6
            }
            html = get_page_index(url, data)
            datas = json.loads(html)
            for data in datas['data']:
                href = 'http://news.zhuniu.com/redian/' + str(data['id']) + '.html'
                title = data['articleTitle']
                get_detail(href, title, mh)


if __name__ == '__main__':
    main()
