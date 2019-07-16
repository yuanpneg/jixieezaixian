import pymongo
import requests
from requests import RequestException
from bs4 import BeautifulSoup

headers = {
    'Host': 'm.58zulin.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HUAWEI MLA-AL10 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

}


def get_page_index(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return str(response.text)
        if response.status_code == 500:
            return ''
    except RequestException:
        print('请求目录页失败')


def get_page_detail(url):
    try:
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
        collection = db.zujixie
        for page in range(56, 1007):
            print('页数: ', page)
            url = 'http://m.58zulin.com/5-0-0-' + str(page) + '.html'
            html = get_page_index(url)
            if (html != '' and html != None):
                soup = BeautifulSoup(html, "html.parser")
                divs = soup.find_all('li', class_='aui-list-item aui-padded-t-5 aui-padded-b-5')
                for div in divs:
                    try:
                        price = ''
                        brand = ''
                        model = ''
                        city = ''
                        staust = ''
                        company = ''
                        contacts = ''
                        phone = ''
                        tel = ''
                        area = ''
                        address = ''
                        detailed_description = ''
                        dsj_id = ''
                        equipment = {}
                        detail = div.find('div', class_='aui-list-item-title aui-ellipsis-2')
                        href = 'http://m.58zulin.com/' + detail.a['href']
                        html_detail = get_page_detail(href)
                        soup_detail = BeautifulSoup(html_detail, "html.parser")
                        title = soup_detail.find('span', class_='aui-margin-l-10 dt-text-black').text
                        contents = soup_detail.find_all('li', class_='aui-list-item-title')
                        if (len(contents) > 0):
                            for content in contents:
                                if (content.text.find('设备租金') != -1):
                                    price = content.text.rstrip().split(':')[1]
                                if (content.text.find('设备品牌') != -1):
                                    brand = content.text.rstrip().split(':')[1]
                                if (content.text.find('设备型号') != -1):
                                    model = content.text.rstrip().split(':')[1]
                                if (content.text.find('所在城市') != -1):
                                    city = content.text.rstrip().split(':')[1]
                                if (content.text.find('设备状态') != -1):
                                    staust = content.text.rstrip().split(':')[1]
                        contact_information = soup_detail.find('div', class_='dtchip-contact')
                        contact_text = contact_information.find_all('a')
                        if len(contact_text) == 1:
                            tel = contact_information.a.text
                            contacts = div.find('div', class_='aui-list-item-text dt-margin-t-5').text.strip(
                                "\n")  # 联系人
                            address = div.find('span', class_='dt-label aui-label-warning aui-label-outlined').text
                        else:
                            for key, link_text in enumerate(contact_text):
                                if (link_text.text.find('公司') != -1):
                                    company = link_text.text.rstrip()
                                if (key == 3):
                                    phone = link_text.text.rstrip()
                                if (key == 4):
                                    tel = link_text.text.rstrip()
                                if (key == 5):
                                    area = link_text.text.rstrip()
                                if (key == 6):
                                    address = link_text.text.rstrip()

                        detailed_description = soup_detail.find('div',
                                                                class_='aui-card-list-content-padded aui-padded-t-10 aui-padded-b-10 dt-chip-content').text
                        dsj_id = 'zjx' + detail.a['href'].split('.')[0]
                        equipment = {'contacts': contacts, 'address': address, 'title': title, 'price': price,
                                     'staust': staust,
                                     'brand': brand, 'model': model, 'tel': tel, 'description': detailed_description,
                                     'dsj_id': dsj_id, 'city': city, 'company': company, 'phone': phone, 'area': area,
                                     'url': href}
                        print(equipment)
                        collection.insert(equipment)

                    except Exception:
                        print('解析页面报错')
                        continue
    except Exception:
        print('解析页面报错')


if __name__ == '__main__':
    main()
