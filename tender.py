from wp_file.MysqlHelper import MysqlHelper
import time
from datetime import datetime
#工程招标

def selectTender():
    mh = MysqlHelper('120.55.52.30', 'bigdata', 'bigdata', 'lezhu_new', 'utf8')
    start_time = int(time.mktime(datetime.now().date().timetuple()))  # 今天0点
    end_time = start_time - 86400  # 昨天0点
    sql = 'select title,content,addtime,edittime,`from`,address,cattitle from tp_tender where %d <= addtime and addtime < %d ' % (
        end_time, start_time)  #查询了昨天的数据
    tenders = mh.find(sql)
    lmh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    if (len(tenders) > 0):
        for tender in tenders:
            title = tender['title']
            content = tender['content']
            insert_title = "insert into pre_portal_article_title (catid,bid,uid,username,title,highlight,author,`from`,`fromurl`," \
                           "url,summary,pic,thumb," \
                           "remote,id,idtype,contents,allowcomment,owncomment,click1,click2,click3,click4," \
                           "click5,click6,click7,click8,tag,dateline,status,showinnernav,preaid,nextaid,htmlmade,htmlname,htmldir) VALUES " \
                           "('%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d'" \
                           ", '%d', '%d', '%d', '%d', '%d',unix_timestamp(now()), '%d', '%d', '%d', '%d', '%d', '%s', '%s')" % \
                           (5, 0, 1, 'admin', title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, '', '')
            lmh.cud(insert_title)
            max_id = lmh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_content = "insert into pre_portal_article_content (aid, id, idtype, title, content, pageorder, dateline" \
                             ") VALUES ('%d','%d','%s','%s','%s','%d',unix_timestamp(now()))" % (
                             id, 0, '', '', content, 5)
            lmh.cud(insert_content)


if __name__ == '__main__':
    selectTender()
