from wp_file.MysqlHelper import MysqlHelper
#商品
def insertData():
    mh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    sql = "select * from tp_goods limit 100"  #设置了条数
    goods = mh.find(sql)
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    for good in goods:
        title = str(good['title'])
        post_content =  '<p>单位：' + good['unit'] + '</p>' + '<p>价钱：' + str(
            good['price']) + '</p>' \
                       + '<p>公司名称：' + good['shoptitle'] + '</p>' + '<p>联系方式：' \
                       + str(good['usermobile']) + '</p>' + \
                       '<p>商品详情：' + str(good['content']) + '</p>'
        pics = good['pics']
        pic_list = pics.split(',')
        if len(pic_list) > 0:
            for pic in pic_list:
                post_content = post_content + '<img class="" src="' + pic + '"alt="" data-original="' + pic + '"/> '
        print(post_content)
        insert_title = "insert into pre_portal_article_title (catid,bid,uid,username,title,highlight,author,`from`,`fromurl`," \
                       "url,summary,pic,thumb," \
                       "remote,id,idtype,contents,allowcomment,owncomment,click1,click2,click3,click4," \
                       "click5,click6,click7,click8,tag,dateline,status,showinnernav,preaid,nextaid,htmlmade,htmlname,htmldir) VALUES " \
                       "('%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d'" \
                       ", '%d', '%d', '%d', '%d', '%d',unix_timestamp(now()), '%d', '%d', '%d', '%d', '%d', '%s', '%s')" % \
                       (3, 0, 1, 'admin', title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, '', '')
        mh.cud(insert_title)
        max_id = mh.find(select_max_sql)
        id = int(max_id[0]['id'])
        insert_content = "insert into pre_portal_article_content (aid, id, idtype, title, content, pageorder, dateline" \
                         ") VALUES ('%d','%d','%s','%s','%s','%d',unix_timestamp(now()))" % (id, 0, '', title, post_content, 1)
        mh.cud(insert_content)


if __name__ == '__main__':
    insertData()
