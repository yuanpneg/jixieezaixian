import pymysql
from recruit.config import *

# 保存天眼查公司信息
conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
cursor = conn.cursor()


def save_company():
    try:
        #  查询库中所有公司名称
        select_sql = 'select DISTINCT company,telephone,longitude,latitude,workplace ' \
                     'from tp_job_recruit_6 where telephone !="None" ' #where telephone != "0516-61230688"
        cursor.execute(select_sql)
        for company in cursor.fetchall():
            company_name = company[0]
            is_jude_company = 'select id from tp_company where company ="%s"' % (company_name)
            cursor.execute(is_jude_company)
            is_null = cursor.fetchone()
            if is_null == None:
                telephone = company[1]
                longitude = company[2]
                latitude = company[3]
                workplace = company[4]
                insert_sql = 'insert into tp_company (company,telephone,longitude,latitude,workplace) ' \
                             'VALUES ("%s","%s","%s","%s","%s")' % (company_name, telephone, longitude, latitude,
                                                                    workplace)
                cursor.execute(insert_sql)
                conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


if __name__ == '__main__':
    save_company()
