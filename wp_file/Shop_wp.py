from wp_file.MysqlHelper import MysqlHelper
from urllib.parse import quote


def insertData():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    sql = "select * from tp_goods_copy limit 35000,5000"
    goods = mh.find(sql)
    select_max_sql = "select MAX(id) as id from wp_posts"
    for good in goods:
        title = str(good['title'])
        post_content = '<p>' + title + '</p>' + '<p>单位：' + good['unit'] + '</p>' + '<p>价钱：' + str(
            good['price']) + '</p>' \
                       + '<p>公司名称：' + good['shoptitle'] + '</p>' + '<p>联系方式：' \
                       + str(good['usermobile']) + '</p>'
        title_split = str(title)[0:16]
        post_name = quote(title_split, 'utf-8')
        print(title_split)
        # pics = good['pics']
        # pic_list = pics.split(',')
        # if len(pic_list) > 0:
        #     for pic in pic_list:
        #         post_content = post_content+'<figure class="wp-block-image"><img src="'+pic+'"alt=""/></figure>'
        # print(post_content)
        insert = "insert into wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status, " \
                 "ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt,post_content_filtered, post_parent, " \
                 "guid, menu_order, post_type, post_mime_type, comment_count) VALUES " \
                 "('%d',now(),now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),'%s','%s','%s','%s','%s','%s','%d')" % \
                 (
                     1, post_content, title, '', 'publish', 'open', 'open', '', post_name, '', '', '', 0, '', 0, 'post',
                     '',
                     0)
        mh.cud(insert)
        max_id = mh.find(select_max_sql)
        id = int(max_id[0]['id'])
        insert_term = "insert into wp_term_relationships (object_id, term_taxonomy_id) VALUES ('%d','%d')" % (id, 6)
        mh.cud(insert_term)


if __name__ == '__main__':
    insertData()
