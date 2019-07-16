# 建设网  新闻资讯  更新的太慢
# www.buildnet.cn
import requests
from pyquery import PyQuery as pq
import datetime
from news.MysqlHelper import MysqlHelper
from selenium import webdriver

headers = {
    'Host': 'www.buildnet.cn',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def get_page_detail(url, mh):
    try:
        # time.sleep(4)
        response = requests.get(url=url, headers=headers)
        response.encoding = 'gbk'
        doc = pq(response.text)
        doc.find('.bshare-custom').remove()
        title = doc.find('.style16000000').text()
        date = doc.find(".style666666").text().replace("来源：建设网", "").replace("/", "-")
        yesterday = getYesterday()
        if str(date).split(" ")[0] == str(yesterday):
            content = doc.find('#detailcontent').text()
            content_html = str(doc.find('#detailcontent')).replace('"', "")
            type = '新闻资讯'
            sql = 'insert into tp_news (content, contentHtml, img, pudate, title, `type` ,url) values  \
                      ("%s", "%s", "%s", "%s", "%s","%s", "%s")' % (content, content_html, '', date, title, type, url)
            mh.cud(sql)
    except Exception as e:
        print(e)
        print('请求详情页失败')


def main():
    try:
        mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
        url = 'http://www.buildnet.cn/NewsAndEvents/NewList.aspx?ID=31&GetType=Type'
        browser = webdriver.Chrome('C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe')
        browser.get(url)
        for page in range(1, 937):
            print(page)
            html = browser.page_source
            doc = pq(html)
            table = doc.find('#NewsLI')
            urls = table.find(".newstitle")
            for url in urls.items():
                href = 'http://www.buildnet.cn' + str(url).split("href=\"")[1].split('"')[0]
                print(href)
                get_page_detail(href, mh)
    except Exception as e:
        print(e)
        print('请求目录页失败')
    finally:
        browser.close()


if __name__ == '__main__':
    main()
