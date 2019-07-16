import pymysql
from recruit.config import *

# 查询标记为1 的公司数据并存入数据库
conn = pymysql.connect(host='localhost', user='root', password='ok', db='goods_process')
cursor = conn.cursor()


def save_company():
    try:
        #  查询库中所有公司名称
        select_sql = 'select DISTINCT company,telephone,address,alibburl ' \
                     'from tp_details_copy '
        cursor.execute(select_sql)
        for company in cursor.fetchall():
            company_name = company[0]
            # 判断公司名是否存在
            is_jude_company = 'select id from tp_company where company ="%s"' % company_name
            cursor.execute(is_jude_company)
            is_null = cursor.fetchone()
            if is_null is None:
                telephone = company[1]
                workplace = company[2]
                alibabaurl = company[3]
                insert_sql = 'insert into tp_company (company,telephone,workplace,alibabaurl) ' \
                             'VALUES ("%s","%s","%s","%s")' % (company_name, telephone, workplace, alibabaurl)
                cursor.execute(insert_sql)
                conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


if __name__ == '__main__':
    save_company()
