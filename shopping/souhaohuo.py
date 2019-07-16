# 搜好货网
# http://www.912688.com
from urllib import parse
from pyquery import PyQuery as pq
import requests
from requests import RequestException
import pymysql
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Host': 's.912688.com',
    'Referer': 'http://www.912688.com/?spm=p201905.vshopindex.logo.e4bec9e6-ba43-4c69-81fe-1c4e7a407baa'
}

conn = pymysql.connect(host='localhost', user='root', password='ok', db='goods_process')
cursor = conn.cursor()


# 请求列表页页面
def request_list(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


# 获取详情信息
def get_detail(html, href, cattitle, catid):
    # 获取商品详情
    doc = pq(html)
    title = doc('body > div.main > div > div.main-data > div.main-data-box.clearfix > div.main-data-param.R > h1') \
        .text()
    prices = doc('.price .arial').text()
    price = prices.split(' ')[0]
    units = doc('.count .arial').text()
    unit = units.split(' ')[0]
    count = doc('.count > div').text()
    unit = unit + count
    have = ""
    if doc.html().find('have'):
        have = doc('.have .arial').text()
    company = doc('#three-data > div.concat-container > div > div.L > ul > li:nth-child(1) > span').text()
    contact = doc('#three-data > div.concat-container > div > div.L > ul > li:nth-child(2) > span:nth-child(2)').text()
    telephone = doc(
        '#bot-nav > div.member.act.csb > div.member-info > ul > li:nth-child(4) > span.val.prod-phone').text()
    phone = doc('#bot-nav > div.member.act.csb > div.member-info > ul > li:nth-child(5) > span.val.prod-phone').text()
    address = doc('#bot-nav > div.member.act.csb > div.member-info > ul > li:nth-child(6) > span.val').text()
    model = doc('#bot-nav > div.member.act.csb > div.member-info > ul > li:nth-child(7) > span.val').text()
    adr = doc('#three-data > div.concat-container > div > div.L > ul > li.adr').text()
    print(title)
    print(price)
    print(unit + ' ' + count)
    print(company)
    print(contact)
    print(telephone)
    print(phone)
    print(address)
    print(type)
    print(adr)
    print(href)

    # 获取图片地址
    pics_arr = doc('.move-container').find('img').items()
    pics = ''
    for pic in pics_arr:
        print(pic.attr('src'))
        pics = pics + pic.attr('src') + ','

    property = {}
    # 获取属性值
    params = doc('.three-con').find('td').items()
    name = ''
    value = ''
    for index, param in enumerate(params):
        if index % 2 == 0:
            name = param.text()
            print(name)
        else:
            value = param.text()
            print(value)
        property[name] = value

    # 存入tp_detail数据库
    insert_detail = 'insert into tp_details(catid, cattitle, title,company,model,telephone,phone,unit,address,' \
                    'contact,pics,' \
                    'href, property, have) ' \
                    'values ("%d","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        catid, cattitle, title, company, model, telephone, phone, unit, adr, contact, pics, href,
                        property, have)
    cursor.execute(insert_detail)
    good_id = int(conn.insert_id())
    conn.commit()

    # 规格价格
    if doc.html().find('obj') > 0:
        # 获取多个规格的
        standard_name_one = doc('.obj-val').text()  # 第一个参数
        insert_key = 'insert into tp_unit_key(unit_key, goodid, cattitle, parentid)values ("%s","%d","%s","%d")' % (
            standard_name_one, good_id, breed, 0
        )
        cursor.execute(insert_key)
        standard_one_id = int(conn.insert_id())  # 第一个参数id
        conn.commit()

        standard_name_two = doc('.title-val').text()  # 第二个规格参数
        insert_key = 'insert into tp_unit_key(unit_key, goodid, cattitle, parentid)values ("%s","%d","%s","%d")' % (
            standard_name_two, good_id, breed, 0
        )
        cursor.execute(insert_key)
        standard_two_id = int(conn.insert_id())  # 第二个参数id
        conn.commit()

        standard_list = list(doc('.turn-param').find('a').items())
        standards = list(doc('.detail-table .specTr').items())
        num = len(standard_list)
        size = len(standards)
        per = int(size / num)
        start = 0
        for standard_title in standard_list:
            unit_key = standard_title.text()
            print(len(standards))
            insert_key = 'insert into tp_unit_key(unit_key, goodid, cattitle, parentid)values ("%s","%d","%s","%d")' % (
                unit_key, good_id, breed, standard_one_id
            )
            cursor.execute(insert_key)
            key_one_id = int(conn.insert_id())
            conn.commit()
            index = 0
            for i in range(start, len(standards)):
                doc_standard = doc(standards[i])
                standard_title = doc_standard('.size').text()  # 参数
                standard_vals = list(doc_standard('.val').items())
                standard_value = standard_vals[0].text()  # 价格
                standard_unit = standard_vals[1].text()  # 可出售数量
                insert_key = 'insert into tp_unit_key(unit_key, goodid, cattitle, parentid)values ("%s","%d","%s","%d")' \
                             % (
                                 standard_title, good_id, breed, standard_two_id
                             )
                cursor.execute(insert_key)
                standardid = int(conn.insert_id())
                conn.commit()

                standard_specs = {standard_one_id: key_one_id, standard_two_id: standardid}  # {'属性id':3,'光源功率':4}

                # 插入 sku 表中
                insert_sku = 'insert into sku(goodid, title, price, specs, stock)values ("%d","%s","%s","%s", "%s")' % (
                    good_id, title, standard_value, standard_specs, standard_unit
                )
                cursor.execute(insert_sku)
                conn.commit()

                print(standard_value)
                print(standard_unit)
                index = index + 1
                if index / per == 1:
                    start = start + per
                    break

    # 判断是否有规格
    elif doc.html().find('detail-table-box ') > 0:
        standards = doc('.detail-table .s')
        standard_title = doc('.title-val').text()
        insert_key = 'insert into tp_unit_key(unit_key, goodid, cattitle, parentid)values ("%s","%d","%s","%d")' % (
            standard_title, good_id, breed, 0
        )
        cursor.execute(insert_key)
        standard_two_id = int(conn.insert_id())  # 第二个参数id
        conn.commit()
        for standard in standards:
            doc_standard = doc(standard)
            standard_title = doc_standard('.size').text()
            standard_vals = list(doc_standard('.val').items())
            standard_value = standard_vals[0].text()
            standard_unit = standard_vals[1].text()
            # 存入数据库
            insert_key = 'insert into tp_unit_key(unit_key, goodid, cattitle, parentid)values ("%s","%d","%s","%d")' \
                         % (
                             standard_title, good_id, breed, standard_two_id
                         )
            cursor.execute(insert_key)
            standardid = int(conn.insert_id())
            conn.commit()

            standard_specs = {standard_two_id: standardid}
            # 插入 sku 表中
            insert_sku = 'insert into sku(goodid, title, price, specs, stock)values ("%d","%s","%s","%s", "%s")' % (
                good_id, title, standard_value, standard_specs, standard_unit
            )
            cursor.execute(insert_sku)
            conn.commit()


if __name__ == '__main__':

    breed = '砂岩'
    catid = 11
    # 要查询的品种
    key_encode = parse.quote(breed)
    url = 'http://s.912688.com/prod/dy/search?kw=' + key_encode  # %25E6%25B0%25B4%25E6%25B3%25A5 水泥
    html = request_list(url)
    doc = pq(html)
    # 获取最大页数
    page_max = doc('body > div.clearfix > div:nth-child(1) > div.s-mod-page.mb30 > span.total').text()
    pages = page_max.replace('共', '').replace('页', '')
    for page in range(1, int(pages)):
        url = 'http://s.912688.com/prod/dy/search?kw=' + breed + '&pageSize=20&spm=p201905.psearchlist.page.858b3697' \
                                                                 '-dfa3-4f1b-8b32-2d7dadeb63e8&page=' + str(page)
        # 获取详情页
        html_list = request_list(url)
        doc = pq(html)
        hrefs = doc('.product-dt-list-new > li > a')
        for href in hrefs:
            href = pq(href)('a').attr('href')
            html_detail = request_list(href)
            get_detail(html_detail, href, breed, catid)
    pass
