import os
from hashlib import md5
import pymongo
import time
import requests
from requests import RequestException


def download_image(url, path_url):
    print('正在下载', url)
    try:
        time.sleep(4)
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            save_image(response.content, path_url)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content, path_url):
    file_path = '{0}/{1}.{2}'.format(path_url, md5(content).hexdigest(), 'png')
    if not os.path.exists(path_url):
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path_url)
        print(path_url + ' 创建成功')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path_url + ' 目录已存在')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()
        return False


def find_data():
    try:
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        collection = db.equipment
        pic_list = collection.find()
        pic_path = 'https://su.bcebos.com/v1/lezhu/equipment/dsj/xieduohui/'
        for pic in pic_list:
            img_url_list = pic['img_url_list']
            dsj_id = pic['dsj_id']
            img_id = 'xieduohui_' + str(pic['id'])
            url = ''
            for img in img_url_list:
                path_url = 'E:/xieduohui/' + img_id
                if url == '':
                    url = pic_path + img_id + '/' + img.split('/')[-1]
                else:
                    url = url + ',' + pic_path + img_id + '/' + img.split('/')[-1]
                download_image(img, path_url)
            print(url)
            collection.update_one({'dsj_id': dsj_id}, {'$set': {'img_url_list': url, 'dsj_id': img_id}})
    except Exception as e:
        print(e)


if __name__ == '__main__':
    find_data()
