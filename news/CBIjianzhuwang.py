import requests
from pyquery import PyQuery as pq
from news.MysqlHelper import MysqlHelper
import time
# CBI 建筑网  建筑知识
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'www.cbi360.net',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def get_page_index(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        print('请求目录页失败')


def get_detail(url, title, date, mh):
    try:
        time.sleep(0.5)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            detail_html = response.text
            detail_doc = pq(detail_html)
            content = detail_doc.find('.new-cont').text()
            content_html = detail_doc.find('.new-cont')
            content_htmls = str(content_html).replace('"', '').replace("'","")
            if content.find('以上' + title + '内容由建筑网搜集整理') == -1:
                content = content.split('想知道更多关')[0]
                content_htmls = content_htmls.split('想知道更多关')[0]
            else:
                content = content.split('以上' + title + '内容由建筑网搜集整理')[0]
                content_htmls = content_htmls.split('以上' + title + '内容由建筑网搜集整理')[0]
            sql = 'insert into tp_knowledge (content, contentHtml, img, pudate, title, `type` ,url) values  \
                      ("%s", "%s", "%s", "%s", "%s","%s", "%s")' % (
                content, content_htmls, '', date, title, type, url)
            mh.cud(sql)
    except Exception as e:
        print(e)
        print('请求目录页失败')


def main():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    for i in range(1372, 3814):
        print(i)
        #time.sleep(3)
        url = 'https://www.cbi360.net/hyjd/jzzs/' + str(i) + '.html'
        html = get_page_index(url)
        doc = pq(html)
        # 置顶三条
        urls = doc.find('.hyjd-list li')
        for url in urls.items():
            href = 'https://www.cbi360.net' + url.find('a').attr('href')
            title = url.find('h2 a').text()
            date = url.find('.hyjd-class-area p').text()
            print(href)
            get_detail(href, title, date, mh)
        #  列表
        urls = doc.find('.hyjd-list-cont li')
        for url in urls.items():
            href = 'https://www.cbi360.net' + url.find('h2 a').attr('href')
            title = url.find('h2 a').text()
            date = url.find('div').text()
            print(href)
            get_detail(href, title, date, mh)


if __name__ == '__main__':
    main()
