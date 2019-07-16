import requests
import json
import pymysql
from recruit.config import *

from requests.exceptions import RequestException

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
cursor = conn.cursor()


# 获取百度地图api经纬度
def get_lng_lat(address):
    try:
        url = "http://api.map.baidu.com/geocoder/v2/?address=" + address + \
              "&output=json&ak=6xssQ7pGB8fsvW90w9jqZHH3&mcode=E9:B1:66:E2:" \
              "A3:1D:4B:39:95:39:C5:F4:62:7D:BE:9A:EE:29:B9:03;com.cz.nongyetong"
        response = requests.get(url)
        response.encoding = 'utf-8'
        return response.text
    except RequestException:
        print('请求索引页失败')
        return None


if __name__ == '__main__':
    try:
        find_sql = 'select title from tp_region2 '
        cursor.execute(find_sql)
        for address in cursor.fetchall():
            html = get_lng_lat(address[0])
            response = json.loads(html)
            lng = response['result']['location']['lng']
            lat = response['result']['location']['lat']
            print(address[0], "   ", str(lng) + "," + str(lat))
            update_sql = 'update tp_region2 set  longitude = "%s",latitude = "%s" where title like "%s"' % (
            str(lng), str(lat), address[0])
            cursor.execute(update_sql)
            conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
