# 工程造价（信息价）
from wp_file.MysqlHelper import MysqlHelper
import time



def insertData():
    mh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    sql = 'select * from top_good_zaojiatongxinxijia limit 100'
    cost_msg = mh.find(sql)
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    if len(cost_msg) > 0:
        for cost in cost_msg:
            title = cost['title']  # 商品名
            source = cost['company']  # 城市/省
            industry = cost['industry']  # 行业
            unit = cost['unit']  # 单位
            date = cost['infomIssueDate']  # 发布日期
            timeArray = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
            notax_avg = cost['notaxAvg']  # 除税平均价
            notax_price = cost['notaxInformation']  # 除税价
            notax_min = cost['notaxMin']  # 除税最小值
            notax_max = cost['notaxMax']  # 除税最大值
            notax_upprice = cost['notaxUpprice']  # 除税上期价格
            spec = cost['specificationType']  # 商品类型
            tax_avg = cost['taxAvg']
            if tax_avg == '':
                tax_avg = '--'  # 含税平均价
            tax_information = cost['taxInformation']
            if tax_information == "无":
                tax_information = '--'  # 含税价
            tax_max = cost['taxMax']  # 含税最大值
            tax_min = cost['taxMin']  # 含税最小值
            tax_upprice = cost['taxUpprice']  # 含税上期价格
            main_title = title + "&nbsp;&nbsp;&nbsp;" + spec + "&nbsp;&nbsp;&nbsp;" + source
            pre_content = '<p><table border="1" cellspacing="0" style="width:100%;text-align:center;height:25%"><tr>' + source + '</tr> <tr><td>名称</td><td>行业</td><td>规格型号</td><td>单位</td><td>更新时间</td></tr><tr><td>' + title + '</td><td>' + industry + '</td><td>' + spec + '</td><td>' + unit + '</td><td>' + date + '</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;height:25%"><tr>含税信息价</tr><tr><td>当前价格</td><td>上期价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td></tr><tr><td>' + str(
                tax_information) + '</td><td>' + str(tax_upprice) + '</td><td>' + str(tax_avg) + '</td><td>' + str(
                tax_max) + '</td><td>' + str(
                tax_min) + '</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;height:25%"><tr>除税信息价</tr><tr><td>当前价格</td><td>上期价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td></tr><tr><td>' + str(
                notax_price) + '</td><td>' + str(notax_upprice) + '</td><td>' + str(notax_avg) + '</td><td>' + str(
                notax_max) + '</td><td>' + str(notax_min) + '</td></tr></table></table></p>'
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
                           (11, 0, 1, 'admin', main_title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0,
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
