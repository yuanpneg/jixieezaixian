from wp_file.MysqlHelper import MysqlHelper
#工程机械

def insertData():
    mh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    sql = 'select * from tp_equipment limit 100'
    equiments = mh.find(sql)
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    if len(equiments) > 0:
        for equiment in equiments:
            title = equiment['title']
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
            pre_content = '<p>品牌：' + brand + '</p> ' + '<p>型号：' + type + '</p>' + \
                          '<p>电话：' + tel + '</p>' + '<p>联系人：' + contact + '</p>' + \
                          '<p>价格：' + price + '</p>' + '<p>详情：' + content + '</p>' + \
                          '<p>地址：' + address + '</p>' + '<img class="" src=" ' + pic + '"alt="" data-original="' + pic + '"/> '
            insert_title = "insert into pre_portal_article_title (catid,bid,uid,username,title,highlight,author,`from`,`fromurl`," \
                           "url,summary,pic,thumb," \
                           "remote,id,idtype,contents,allowcomment,owncomment,click1,click2,click3,click4," \
                           "click5,click6,click7,click8,tag,dateline,status,showinnernav,preaid,nextaid,htmlmade,htmlname,htmldir) VALUES " \
                           "('%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d'" \
                           ", '%d', '%d', '%d', '%d', '%d',unix_timestamp(now()), '%d', '%d', '%d', '%d', '%d', '%s', '%s')" % \
                           (4, 0, 1, 'admin', title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, '', '')
            mh.cud(insert_title)
            max_id = mh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_content = "insert into pre_portal_article_content (aid, id, idtype, title, content, pageorder, dateline" \
                             ") VALUES ('%d','%d','%s','%s','%s','%d',unix_timestamp(now()))" % (
                                 id, 0, '', '', pre_content, 1)
            mh.cud(insert_content)


if __name__ == '__main__':
    insertData()
