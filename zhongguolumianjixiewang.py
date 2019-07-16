# 中国路面机械网   https://www.lmjx.net/

import pymongo
import requests
from requests import RequestException
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

headers = {
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Cookie': 'UM_distinctid=16449a26796c11-04291b3ab516f2-5b163f13-1fa400-16449a26798dc1; CNZZDATA452385=cnzz_eid%3D1225653535-1542609432-%26ntime%3D1542609432'
}


def get_page_index(url):
    try:
        headers["host"] = 'list.lmjx.net'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return str(response.text)
        if response.status_code == 500:
            return ''
    except RequestException as e:
        print(e.strerror)
        print('请求目录页失败')


def get_page_detail(url):
    try:
        headers["host"] = 'detail.lmjx.net'
        response = requests.get(url=url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            if response.text != None:
                return response.text
        if response.status_code == 500:
            return ''
        return ''
    except Exception:
        return ''
        print('请求详情页失败')


def main():
    try:
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        collection = db.lumianjixiewang
        for page in range(1, 2314):
            print('页数: ', page)
            url = 'https://list.lmjx.net/zl/?p=' + str(page)
            html = get_page_index(url)
            if (html != '' and html != None):
                soup = BeautifulSoup(html, "lxml")
                divs = soup.select('.plist  .item')
                for div in divs:
                    try:
                        price = ''
                        brand = ''  # 产品品牌
                        model = ''  # 规格型号
                        city = ''
                        staust = ''
                        company = ''  # 公司信息
                        contacts = ''  # 联系人
                        phone = ''  # 电话
                        tel = ''  # 手机
                        area = ''  # 出租地区
                        address = ''  # 所在地址
                        category = ''  # 产品分类
                        detailed_description = ''
                        dsj_id = ''
                        pic = ''  # 图片
                        email = ''  # 邮箱
                        caddress = ''  # 公司地址
                        equipment = {}  # 机械对像

                        href = 'https:' + div.a['href']
                        html_detail = get_page_detail(href)
                        # soup_detail = BeautifulSoup(html_detail, "lxml")  #商品详情
                        doc = pq(html_detail)
                        title = doc('.titile').text()
                        productinf = doc('.productinf p')  # 机械详情
                        for p in productinf:
                            string = p.text.replace('：', ":")
                            if (string.find('产品品牌') != -1):
                                brand = string.rstrip().split(':')[1]
                            if (string.find('规格型号') != -1):
                                model = string.rstrip().split(':')[1]
                            if (string.find('出租价格') != -1):
                                price = string.rstrip().split(':')[1]
                            if (string.find('出租区域') != -1):
                                s = string.replace('\r\n', '')
                                area = s.rstrip().split(':')[1]
                            if (string.find('所在地区') != -1):
                                address = string.rstrip().split(':')[1]
                            if (string.find('产品分类') != -1):
                                category = string.rstrip().split(':')[1]

                        img = doc(
                            'body > div.allbody > div.allrightbody > div.morchoosepro.morcwid > div:nth-child(2) > div > img')
                        pic = "https:" + img.attr('src')
                        detailed_description = doc(
                            'body > div.allbody > div.allrightbody > div.morchoosepro.morcwid > div:nth-child(2) > div > div.inf').text()
                        company = doc('.tb_box .cnm').find('a').text()
                        contacts = doc('.tb_box').find('td')[2].text
                        phone = doc('.tb_box').find('td')[6].text
                        caddress = doc('.tb_box').find('td')[7].text
                        if address == '' or address == None:
                            address = area
                        tel = doc('.tb_box').find('td')[8].text
                        dsj_id = 'lmjx_' + href.split('market_')[1].split('.html')[0]
                        equipment = {'contacts': contacts, 'caddress': caddress, 'title': title, 'price': price,
                                     'staust': staust, 'address': address,
                                     'brand': brand, 'model': model, 'tel': tel, 'description': detailed_description,
                                     'dsj_id': dsj_id, 'city': city, 'company': company, 'phone': phone, 'area': area,
                                     'pic': pic, 'category': category,
                                     'url': href}
                        print(equipment)
                        collection.insert(equipment)
                    except Exception as e:
                        print(e)
                        print('解析页面报错')

    except Exception as e:
        print(str(e))
        print('解析页面报错')

if __name__ == '__main__':
    main()
