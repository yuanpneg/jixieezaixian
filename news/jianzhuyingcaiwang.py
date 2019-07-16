import requests
from pyquery import PyQuery as pq
import datetime
from news.MysqlHelper import MysqlHelper

# 建筑英才挖抓取
headers = {
    'Accept-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'news.buildhr.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def get_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'gb2312'
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        print('请求目录页失败')


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def get_page_index(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'gb2312'
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        print('请求目录页失败')


def main():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    for page in range(1, 20):
        url = 'http://news.buildhr.com/more.php?type=144&page=' + str(page)
        html = get_page_index(url)
        doc = pq(html)
        list = doc('.morenews li')
        i = 0;
        for url in list.items():
            if i % 2 == 0:
                href = url.find('a').attr('href')
                release_time = url.find('h1 span b').text()
                release_time = release_time.replace('年', '-').replace('月', '-').replace('日', '')
                yesterday = getYesterday()
                if release_time == str(yesterday):
                    print(href)
                    detail_html = get_detail(href)
                    detail_doc = pq(detail_html)
                    content = detail_doc.find('.newsContent').text()
                    content_html = detail_doc.find('.newsContent').find('p')
                    content_html.find('a').remove()
                    title = detail_doc.find('#newsMain').find('h1').text()
                    type = '新闻资讯'

                    if title != '' and title != None:
                        sql = 'insert into tp_news (content, contentHtml, img, pudate, title, `type` ,url) values  \
                              ("%s", "%s", "%s", "%s", "%s","%s", "%s")' % (
                            content, content_html, '', release_time, title, type, href)
                        mh.cud(sql)
            i = i + 1


if __name__ == '__main__':
    main()
