from wp_file.MysqlHelper import MysqlHelper
import time
from urllib.parse import quote
from apscheduler.schedulers.blocking import BlockingScheduler


# 招聘

def insertData():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    sql = 'select * from tp_job_recruit'
    recruits = mh.find(sql)
    select_max_sql = "select MAX(id) as id from wp_posts"
    if len(recruits) > 0:
        for recruit in recruits:
            address = recruit['workplace']
            title = recruit['title'] + "  " + address
            title_split = str(title)[0:17]
            print(title_split)
            post_name = quote(title_split, 'utf-8')
            experience = recruit['experience']
            content = recruit['description']
            company = recruit['company']  # 公司
            if company == '':
                company = '无'
            tel = recruit['telephone']
            position = recruit['positiontitle']  # 分类
            price = recruit['salary']  # 薪金
            release_time = recruit['addtime']
            timeArray = time.localtime(release_time)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            post_content = '<p>岗位：' + title + ' ( ' + position + ' ) ' '</p> ' + '<p>发布时间：' + otherStyleTime + '</p>' + \
                           '<p>电话：' + tel + '</p>' + '<p>公司：' + company + '</p>' + \
                           '<p>工作经验：' + experience + \
                           '<p>薪资：' + price + '</p>' + '<p>详情：' + content + '</p>' + \
                           '<p>地址：' + address
            insert = "insert into wp_posts (post_author,post_date,post_date_gmt,post_content," \
                     "post_title,post_excerpt,post_status,comment_status, " \
                     "ping_status, post_password, post_name, to_ping, pinged, post_modified," \
                     " post_modified_gmt,post_content_filtered, post_parent, " \
                     "guid, menu_order, post_type, post_mime_type, comment_count) VALUES " \
                     "('%d',now(),now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                     "now(),now(),'%s','%s','%s','%s','%s','%s','%d')" % \
                     (
                         1, post_content, title, '', 'publish', 'open', 'open', '', post_name, '', '', '', 0, '', 0,
                         'post', '',
                         0)
            mh.cud(insert)
            max_id = mh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_term = "insert into wp_term_relationships (object_id, term_taxonomy_id) VALUES ('%d','%d')" % (id, 4)
            mh.cud(insert_term)


if __name__ == '__main__':
    insertData()
    # scheduler = BlockingScheduler()  # 调度器
    # scheduler.add_job(insertData, 'cron', day_of_week='0-6', hour=21, minute=30)
    # scheduler.start()
