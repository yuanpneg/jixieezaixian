import pymysql
from recruit.config import *
from pyquery import PyQuery as pq
import os

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db='lz_crawler')
cursor = conn.cursor()


def get_html_detail():
    work_dir = 'C:\\Users\\Administrator\\Desktop\\key_value'
    # 获取文件夹下的所有文件路径
    for parent, dirnames, filenames in os.walk(work_dir, followlinks=True):
        # 文件名称
        for filename in filenames:
            print(filename)
            print('=================================================')
            # 文件路径
            file_path = os.path.join(parent, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
                doc = pq(html)
                lis = doc('body > div.export-wrapper > ul > li')
                cattitle = doc('body > div.export-wrapper > div > div:nth-child(1)').text()
                select_sql = 'select id from tp_category where title = "%s" and level = 2' % (cattitle)
                cursor.execute(select_sql)
                if(cursor.rowcount == 0):
                   catid = 0
                else:
                   catid = cursor.fetchone()[0]
                   if catid == None or catid == '':
                       catid = 0
                for li in lis:
                    li_detail = pq(li)
                    type_names = li_detail('li > span')
                    type_name = type_names[0]
                    name = type_name.text.replace("分类", "")

                    sql = 'INSERT  INTO tp_unit_key_gc(unitKey, catid, cattitle) values ("%s", %d, "%s")' % (
                        name, catid, cattitle)
                    cursor.execute(sql)
                    key_id = int(conn.insert_id())
                    conn.commit()

                    for value in type_names[1:]:
                        print(value.text)
                        sql_value = 'INSERT  INTO tp_unit_value_gc(unitValue, keyid, catid) values ("%s", %d, %d)' % (
                            value.text, key_id, catid)
                        cursor.execute(sql_value)
                        conn.commit()


if __name__ == '__main__':
    get_html_detail()
