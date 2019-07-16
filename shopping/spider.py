import os

import requests
from requests import RequestException
import pymysql
from xpinyin import Pinyin

conn = pymysql.connect(host='localhost', user='root', password='ok', db='goods_process')
cursor = conn.cursor()


def get_image(key1, key2):
    print(key2)
    selectImageUrlsSql = 'SELECT cattitle, pics,id,detail_pics FROM ' + key1 + ' where id in (select detailid from ' + key2 + ' where pics is null)'
    cursor.execute(selectImageUrlsSql)
    imageUrlsArray = cursor.fetchall()
    pin = Pinyin()
    for imageUrls in imageUrlsArray:
        name = imageUrls[0]
        title = pin.get_pinyin(name).replace("-", "")
        print(imageUrls)
        if imageUrls[1] != None:
            imagesUrlArray = imageUrls[1].split(',')
            # 详情内图片
            detail_images = imageUrls[3].split(',')
            urlid = imageUrls[2]
            count = 0
            a = set()
            for imageUrl in imagesUrlArray[0:5:1]:
                # splitjpg = imageUrl.split('..')
                # url = splitjpg[1]
                end_url = imageUrl.split("/")[-1].split(".jpg")[0]
                print(imageUrl)
                count += 1
                picss = 'https://su.bcebos.com/v1/lezhu/goods/dsj_new/alibaba/' + "alibaba_" + title + '/' + end_url + '.jpg'
                a.add(picss)
                print(",".join(str(i) for i in a))
                sql = 'UPDATE ' + key2 + ' SET pics= "%s"WHERE detailid= "%s"' % (
                    ",".join(str(i) for i in a), str(urlid))
                try:
                    cursor.execute(sql)
                    conn.commit()
                except:
                    conn.rollback()
                download_image(imageUrl, title, end_url)
            # 详情内图片
            detail_images = imageUrls[3].split(',')
            for detail_image in detail_images:
                detail_image_url = detail_image.split("/")[-1].split(".jpg")[0]
                #
                detail_picss = 'https://su.bcebos.com/v1/lezhu/goods/dsj_new/alibaba/' + "alibaba_" + title + '/' + detail_image_url + '.jpg'
                sql = 'update ' + key2 + ' set details = REPLACE(details,' + '"' + detail_image + '"' + ',' + '"' + detail_picss + '"' + ') where detailid = "%s"' % (
                    str(urlid))
                try:
                    cursor.execute(sql)
                    conn.commit()
                except:
                    conn.rollback()
                download_image(detail_image, title, detail_image_url)


def download_image(url, title, end_url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            save_image(response.content, title, end_url)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content, title, end_url):
    titleId = "alibaba_" + title
    path = 'F:\\alibaba1\\' + titleId
    file_path = '{0}/{1}.{2}'.format(path, end_url, 'jpg')
    isExists = os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()
        return False


if __name__ == '__main__':
    # 'pe波纹管', '安全帽', '安全鞋', '保温钉', '壁纸', '波纹补偿器', '不锈钢波纹管', '不锈钢管',
    # titles 为什么是一个数据库？这个数据库读出来的是什么?
    titles = ['tp_details']
    for title in titles:
        key1 = title
        key2 = "tp_goods_" + title
        get_image(key1, key2)
