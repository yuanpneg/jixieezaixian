import pymysql


conn = pymysql.connect(host='localhost', user='root', password='ok', db='goods_process')
cursor = conn.cursor()


# 从本地公司修改电话
def updatePhone():
    find_all_company = 'select distinct company from tp_details_copy where flag = 0'
    cursor.execute(find_all_company)
    for company in cursor.fetchall():
        company_name = company[0]
        is_jude_company = 'select telephone from tp_company where flag = 1 and  company ="%s"' % company_name
        cursor.execute(is_jude_company)
        is_null = cursor.fetchone()
        if is_null is not None:
            telephone = is_null[0]
            update_telephone = 'update tp_details_copy set telephone = "%s" , flag = 1 where company = "%s" ' % (
                telephone, company_name)
            cursor.execute(update_telephone)
            conn.commit()


if __name__ == '__main__':
    updatePhone()
