from wp_file.MysqlHelper import MysqlHelper
from urllib.parse import quote
# 建筑商城  4
# 工程招标  5
# 造价信息  9
# 建筑知识  6
# 人才招聘  8
# 建筑资讯  2
# 设备租赁  1

def insertData():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    sql = "select * from tp_news limit 1000"
    knows = mh.find(sql)
    select_max_sql = "select MAX(id) as id from wp_posts"
    for know in knows:
        title = str(know['title'])  # 标题
        post_content = know['contentHtml']
        name = title[0:10]
        post_name = quote(name, 'utf-8')
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
        insert_term = "insert into wp_term_relationships (object_id, term_taxonomy_id) VALUES ('%d','%d')" % (id, 8)
        mh.cud(insert_term)


if __name__ == '__main__':
    insertData()