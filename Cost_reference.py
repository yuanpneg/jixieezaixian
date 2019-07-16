#工程造价（参考价）
from wp_file.MysqlHelper import MysqlHelper
import time

def insertData():
    mh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    sql = 'select * from top_good_zaojiatongcankaojia'
    cost_msg = mh.find(sql)
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    if len(cost_msg) > 0:
        for cost in cost_msg:
            title = cost['materialRef_name']  # 标题名称
            first_title = cost['title']
            city = cost['region']  # 城市/省
            unit = cost['unit']  # 单位
            date = cost['updatetime']  # 发布日期
            timeArray = int(time.mktime(time.strptime(str(date).split(" ")[0], '%Y-%m-%d')))
            avg = cost['avg']  # 均价
            price_min = cost['min']  # 最小值
            price_max = cost['max']  # 最大值
            upanddown = cost['upanddown']  # 涨跌价
            source = cost['source']  # 来源
            spec = cost['specificationType']  # 商品类型
            main_title = title + "&nbsp;&nbsp;&nbsp;" + spec + "&nbsp;&nbsp;&nbsp;" + source
            pre_content = '<p><table border="1" cellspacing="0" style="width:100%;text-align:center;height:20%"><tr>' + first_title + \
                          '</tr> <tr><td>产品名称</td><td>规格型号</td><td>单位</td><td>更新时间</td><td>城市</td><td>来源</td></tr><tr><td>' + title + '</td><td>' + spec + '</td><td>' + unit + '</td><td>' + date + '</td><td>' + city + '</td><td>'+source+'</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;height:20%"><tr style="width:100%;text-align:center;height:15%">参考价（单位：元）</tr><tr><td>最小价格</td><td>最大价格</td><td>平均价格</td><td>涨跌价格</td></tr><tr><td>' + str(
                price_min) + '</td><td>' + str(price_max) + '</td><td>' + str(avg) + '</td><td>' + str(
                upanddown) + '</td>'
            '''
            pre_content = '<p>' + source + '</p><p>名称：' + title + '</p>' + \
                          '<p>行业：' + industry + '</p><p>规格型号：' + spec + '<p>单位：' + unit + '</p>' + '<p>更新时间：' + \
                          date + '</p>' + \
                          '<p>含税信息价</p>' + '<p>当前价格：' + tax_information + '</p>' + '<p>上期价格：' + tax_upprice + '</p>' + \
                          '<p>平均价格：' + tax_avg + '</p><p>最高价格：' + tax_max + '</p><p>最低价格：' + tax_min + '</p>' + \
                          '<p>除税信息价</p>' + '<p>当前价格：' + notax_price + '</p>' + '<p>上期价格：' + notax_upprice + '</p>' + \
                          '<p>平均价格：' + notax_avg + '</p><p>最高价格：' + notax_max + '</p><p>最低价格：' + notax_min + '</p>'
            '''
            insert_title = "insert into pre_portal_article_title (catid,bid,uid,username,title,highlight,author,`from`,`fromurl`," \
                           "url,summary,pic,thumb," \
                           "remote,id,idtype,contents,allowcomment,owncomment,click1,click2,click3,click4," \
                           "click5,click6,click7,click8,tag,dateline,status,showinnernav,preaid,nextaid,htmlmade,htmlname,htmldir) VALUES " \
                           "('%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d'" \
                           ", '%d', '%d', '%d', '%d', '%d','%d', '%d', '%d', '%d', '%d', '%d', '%s', '%s')" % \
                           (10, 0, 1, 'admin', main_title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, timeArray, 0, 0, 0, 0, 0, '', '')
            mh.cud(insert_title)
            max_id = mh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_content = "insert into pre_portal_article_content (aid, id, idtype, title, content, pageorder, dateline" \
                             ") VALUES ('%d','%d','%s','%s','%s','%d','%d')" % (
                                 id, 0, '', '', pre_content.strip(), 1, timeArray)
            mh.cud(insert_content)


if __name__ == '__main__':
    insertData()