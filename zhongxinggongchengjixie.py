import pymongo
import requests
from requests import RequestException
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium import webdriver
import time

headers = {
    'Host': 'www.zx5880.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.zx5880.com/chuzu/',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HUAWEI MLA-AL10 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
}


# 首次请求
def get_page_index(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return str(response.text)
        if response.status_code == 500:
            return ''
    except RequestException:
        print('请求目录页失败')


# 其他请求
def get_page_second(url, data):
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return str(response.text)
        if response.status_code == 500:
            return ''
    except RequestException:
        print('请求目录页失败')


def get_page_detail(url):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = 'gb2312'
        print(response.status_code)
        if response.status_code == 200:
            if response.text != None:
                return response.text
        if response.status_code == 500:
            return ''
        return ''
    except Exception as e:
        print(e)
        print('请求详情页失败')


def main():
    try:
        browser = webdriver.Firefox()  # 火狐的selenium
        browser.maximize_window()
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        collection = db.zhongxing
        browser.get('http://www.zx5880.com/chuzu/')
        time.sleep(1)
        for page in range(1, 11):
            print('page %d' % page)
            html = browser.find_element_by_class_name('info')
            href = ''
            title = ''
            detailed_description = ''
            address = ''
            category = ''
            brand = ''
            model = ''
            dsj_id = ''
            tel = ''
            contacts = ''
            equipment = {}
            if (html != '' and html != None):
                info_list = html.find_elements_by_tag_name('a')
                for info in info_list:
                    info_href = info.get_attribute('href')
                    detail_html = get_page_detail(info_href)
                    doc_detail = pq(detail_html)
                    title = doc_detail('h1').text()
                    detailed_description = doc_detail('#texts').text().split('联系我时请说')[0]
                    canshuBg = doc_detail('#canshuBg li').items()
                    for canshu in canshuBg:
                        if canshu.text().find('所在区域') != -1:
                            address = canshu.text().replace('所在区域：', '')
                        elif canshu.text().find('设备类型') != -1:
                            string = canshu.text().replace('设备类型：', '')
                            category = string.split('-', 1)[0]
                            brand = string.split('-', 1)[1].split('-', 1)[0].strip()
                            model = string.split('-', 1)[1].split('-', 1)[1].strip()
                    id = str(info_href).replace('http://www.zx5880.com/chuzu/info_', '').split('.')[0]
                    dsj_id = 'zhongxing_' + id
                    contacts_url = 'http://www.zx5880.com/publicFile/getInfo.aspx?id=' + id + '&action=chuzu&_=1542789754350'
                    contacts_html = get_page_detail(contacts_url)
                    doc_contacts = pq(contacts_html)
                    tel = doc_contacts('#lxTel').text()
                    contacts = doc_contacts('#lxren').text()
                    equipment = {'contacts': contacts, 'title': title, 'price': '面议',
                                 'address': address,
                                 'brand': brand, 'model': model, 'tel': tel, 'description': detailed_description,
                                 'dsj_id': dsj_id, 'category': category,
                                 'url': info_href}
                    print(equipment)
                    collection.insert(equipment)
                button = browser.find_element_by_id('lnkbtnNext')
                button.click()
    except Exception as e:
        print(str(e))
    finally:
        browser.close()


if __name__ == '__main__':
    main()
