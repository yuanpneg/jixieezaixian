import requests
import json
import pymysql

conn = pymysql.connect(host='120.55.52.30', user='bigdata', password='bigdata', db='lezhu_new')
cursor = conn.cursor()


# 获取百度地图api经纬度
def get_lng_lat(address):
    url = "http://api.map.baidu.com/geocoder/v2/?address=" + address + \
          "&output=json&ak=6xssQ7pGB8fsvW90w9jqZHH3&mcode=E9:B1:66:E2:" \
          "A3:1D:4B:39:95:39:C5:F4:62:7D:BE:9A:EE:29:B9:03;com.cz.nongyetong"
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text


if __name__ == '__main__':
    try:
        find_sql = 'select title from tp_region where id >= 36 and id <= 397 or id = 3401 or id = 3410 '
        cursor.execute(find_sql)
        for address in cursor.fetchall():
            html = get_lng_lat(address[0] + '市')
            response = json.loads(html)
            lng = response['result']['location']['lng']
            lat = response['result']['location']['lat']
            update_sql = 'update tp_region set   longitude = lng,latitude = lat where title like address[0]'
            cursor.execute(update_sql)
            conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
