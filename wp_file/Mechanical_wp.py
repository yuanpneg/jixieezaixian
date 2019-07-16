from wp_file.MysqlHelper import MysqlHelper
from urllib.parse import quote
#工程机械

def insertData():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    sql = 'select * from tp_equipment limit 1000'
    equiments = mh.find(sql)
    select_max_sql = "select MAX(id) as id from wp_posts"
    if len(equiments) > 0:
        for equiment in equiments:
            title = equiment['title']
            title_split = str(title)[0:17]
            post_name = quote(title_split, 'utf-8')
            address = equiment['address']
            pic = equiment['pic']
            content = equiment['content']
            tel = equiment['telephone']
            contact = equiment['contact']
            brand = equiment['brandtitle']  # 品牌
            type = equiment['typetitle']  # 型号
            price = equiment['rentpricelist']  # 价格
            if price == '':
                price = '面议'
            post_content = '<p>品牌：' + brand + '</p> ' + '<p>型号：' + type + '</p>' + \
                      '<p>电话：' + tel + '</p>' + '<p>联系人：' + contact + '</p>' + \
                      '<p>价格：' + price + '</p>' + '<p>详情：' + str(content).split("\n")[0] + '</p>' + \
                      '<p>地址：' + address + '</p>'


            insert = "insert into wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status, " \
                     "ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt,post_content_filtered, post_parent, " \
                     "guid, menu_order, post_type, post_mime_type, comment_count) VALUES " \
                     "('%d',now(),now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),'%s','%s','%s','%s','%s','%s','%d')" % \
                     (
                         1, post_content, title, '', 'publish', 'open', 'open', '', post_name, '', '', '', 0, '', 0,
                         'post',
                         '',
                         0)
            mh.cud(insert)
            max_id = mh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_term = "insert into wp_term_relationships (object_id, term_taxonomy_id) VALUES ('%d','%d')" % (id, 9)
            mh.cud(insert_term)


if __name__ == '__main__':
    insertData()
