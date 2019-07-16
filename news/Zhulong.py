import requests
from requests import RequestException
from selenium import webdriver
from pyquery import PyQuery as pq
import pymongo
from news.MysqlHelper import MysqlHelper

headers = {
    'Host': 'news.zhulong.com',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie': 'pcid=484873302; ZHULONGID=338C19248465AC8647365D1CAA3085CE:FG=1; __root_domain_v=.zhulong.com; _qddaz=QD.7jec5z.2rmsf2.jn491lv9; UM_distinctid=16763f7573b2d3-0c17582e0818b1-3a3a5c0e-1fa400-16763f7573c63c; PHPSESSID=jse41ubul4taonv4eg0p6nh117; fd=https%3A//www.baidu.com/link%3Furl%3DJbAm_R0kgFHIKHZdbPeOmKN06gTUnLHsgne2SmFEzCUetAmhzGq9GfxBUGQh5tTp%26wd%3D%26eqid%3Dc0fa4c2600017fab000000065c2d863b; Hm_lvt_49541358a94eea717001819b500f76c8=1546487517; Hm_lpvt_49541358a94eea717001819b500f76c8=1546487546'
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


def get_page_detail(url, date, collection):
    try:
        # time.sleep(4)
        print(url)
        response = requests.get(url=url, headers=headers, proxies=proxies)
        doc = pq(response.text)
        title = doc.find('.zhul_xx_newtzTitle').text()
        content = doc.find('.zhul_xx_content')
        content.find('.zhul_tz_addbq').remove()
        content_html = content.html()
        type = '新闻资讯'
        data = {'content': content.text(), 'contentHtml': content_html, 'img': '', 'pudate': date, 'title': title,
                'type': type,
                'url': url}
        if title != '' and title != None:
            collection.insert_one(data)
    except RequestException:
        print('请求详情页失败')


def main():
    try:
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        collection = db.zhulong
        url = 'http://news.zhulong.com/'
        browser = webdriver.Chrome('C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe')
        browser.get(url)
        for page in range(1, 20):
            print(page)
            if page == 1:
                urls = browser.find_elements_by_class_name('list-item')
                for i in urls:
                    href = i.find_element_by_class_name('a-t').get_attribute('href')
                    date = i.find_element_by_class_name('author').text
                    date = str(date).split('发表于')[1].split('回复')[0]
                    get_page_detail(href, date.strip(), collection)
            else:
                print('------------------------------------------------')
                button = browser.find_element_by_id('pull-more')
                button.click()
                urls = browser.find_elements_by_class_name('list-item')
                for i in urls[len(urls) - 10:len(urls)]:
                    href = i.find_element_by_class_name('a-t').get_attribute('href')
                    date = i.find_element_by_class_name('author').text
                    date = str(date).split('发表于')[1].split('回复')[0]
                    get_page_detail(href, date.strip(), collection)
    except RequestException:
        print('请求目录页失败')
    finally:
        browser.close()


if __name__ == '__main__':
    main()
