from wp_file.MysqlHelper import MysqlHelper
import time
from datetime import datetime
from urllib.parse import quote
from apscheduler.schedulers.blocking import BlockingScheduler


# 工程招标

def selectTender():
    mh = MysqlHelper('120.55.52.30', 'bigdata', 'bigdata', 'lezhu_new', 'utf8')
    start_time = int(time.mktime(datetime.now().date().timetuple()))  # 今天0点
    end_time = start_time - 86400  # 昨天0点
    sql = 'select title,content,addtime,edittime,`from`,address,cattitle from tp_tender where %d <= addtime and addtime < %d ' % (
        end_time, start_time)  # 查询了昨天的数据
    tenders = mh.find(sql)
    lmh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    select_max_sql = "select MAX(id) as id from wp_posts"
    if (len(tenders) > 0):
        for tender in tenders:
            title = tender['title']
            title_split = str(title)[0:17]
            print(title_split)
            post_name = quote(title_split, 'utf-8')
            content = tender['content']
            content = str(content).replace("\'", "\"")
            insert = "insert into wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status, " \
                     "ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt,post_content_filtered, post_parent, " \
                     "guid, menu_order, post_type, post_mime_type, comment_count) VALUES " \
                     "('%d',now(),now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),'%s','%s','%s','%s','%s','%s','%d')" % \
                     (
                         1, content, title, '', 'publish', 'open', 'open', '', post_name, '', '', '', 0, '', 0,
                         'post', '',
                         0)
            lmh.cud(insert)
            max_id = lmh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_term = "insert into wp_term_relationships (object_id, term_taxonomy_id) VALUES ('%d','%d')" % (id, 5)
            lmh.cud(insert_term)


if __name__ == '__main__':
    scheduler = BlockingScheduler()  # 调度器
    scheduler.add_job(selectTender, 'cron', day_of_week='0-6', hour=2, minute=30)
    scheduler.start()
