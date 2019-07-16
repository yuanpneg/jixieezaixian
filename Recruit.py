from wp_file.MysqlHelper import MysqlHelper
import time
#招聘

def insertData():
    mh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    sql = 'select * from tp_job_recruit limit 100'
    recruits = mh.find(sql)
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    if len(recruits) > 0:
        for recruit in recruits:
            title = recruit['title']
            address = recruit['workplace']
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
            pre_content = '<p>岗位：' + title + ' ( ' + position + ' ) ' '</p> ' + '<p>发布时间：' + otherStyleTime + '</p>' + \
                          '<p>电话：' + tel + '</p>' + '<p>公司：' + company + '</p>' + \
                          '<p>工作经验：' + experience + \
                          '<p>薪资：' + price + '</p>' + '<p>详情：' + content + '</p>' + \
                          '<p>地址：' + address
            insert_title = "insert into pre_portal_article_title (catid,bid,uid,username,title,highlight,author,`from`,`fromurl`," \
                           "url,summary,pic,thumb," \
                           "remote,id,idtype,contents,allowcomment,owncomment,click1,click2,click3,click4," \
                           "click5,click6,click7,click8,tag,dateline,status,showinnernav,preaid,nextaid,htmlmade,htmlname,htmldir) VALUES " \
                           "('%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d'" \
                           ", '%d', '%d', '%d', '%d', '%d','%d', '%d', '%d', '%d', '%d', '%d', '%s', '%s')" % \
                           (8, 0, 1, 'admin', title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, release_time, 0, 0, 0, 0, 0, '', '')
            mh.cud(insert_title)
            max_id = mh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_content = "insert into pre_portal_article_content (aid, id, idtype, title, content, pageorder, dateline" \
                             ") VALUES ('%d','%d','%s','%s','%s','%d','%d')" % (
                                 id, 0, '', '', pre_content, 1, release_time)
            mh.cud(insert_content)


if __name__ == '__main__':
    insertData()
