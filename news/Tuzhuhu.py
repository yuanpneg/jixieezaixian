import requests
from pyquery import PyQuery as pq
import datetime
from news.MysqlHelper import MysqlHelper

# 土筑虎网站
headers = {
    'Accept-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'www.tuzhuhu.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# 获取页面总页数
def get_page_total(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            doc = pq(response.text)
            page_total = doc(".STYLE1").text()
            page = page_total.split('，共')[1].replace('页', "")
            return page
    except Exception as e:
        print(e)


def get_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        print('请求目录页失败')


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

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def main():
    ids = [3, 4, 7, 18]
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    for id in ids:
        print(id)
        url = 'https://www.tuzhuhu.com/consult/list.html?id=' + str(id)
        #page_total = get_page_total(url)
        for page in range(1, 10):
            print(page)
            url = 'https://www.tuzhuhu.com/consult/list.html?id=' + str(id) + '&pageNum=' + str(page)
            html = get_page_index(url)
            doc = pq(html)
            list = doc('.item')
            for url in list.items():
                href = url('.item-r').find('a').attr('href')
                date = url('.item-r').find('span').text()
                yesterday = getYesterday()
                if str(date) == str(yesterday):
                    title = url('.item-r').find('a').attr('title')
                    print(href)
                    detail_html = get_detail(href)
                    detail_doc = pq(detail_html)
                    content = detail_doc.find('.cont-main').text()
                    content_html = detail_doc.find('.cont-main').find('p')
                    content_html = str(content_html).replace('"','')
                    #content_html.find('a').remove()
                    type = '新闻资讯'
                    if title != '' and title != None:
                        sql = 'insert into tp_news (content, contentHtml, img, pudate, title, `type` ,url) values  \
                              ("%s", "%s", "%s", "%s", "%s","%s", "%s")' % (
                            content, content_html, '', date, title, type, href)
                        mh.cud(sql)

if __name__ == '__main__':
    main()
