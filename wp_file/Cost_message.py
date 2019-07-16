# 工程造价（信息价）
from wp_file.MysqlHelper import MysqlHelper
import time
from urllib.parse import quote



def insertData():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    sql = 'select * from top_good_zaojiatongxinxijia limit 1000'
    cost_msg = mh.find(sql)
    select_max_sql = "select MAX(id) as id from wp_posts"
    if len(cost_msg) > 0:
        for cost in cost_msg:
            title = cost['title']  # 商品名
            title_split = str(title)[0:16]
            post_name = quote(title_split, 'utf-8')
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
            post_content = '<p><table border="1" cellspacing="0" style="width:100%;text-align:center;height:25%"><tr>' + source + '</tr> <tr><td>名称</td><td>行业</td><td>规格型号</td><td>单位</td><td>更新时间</td></tr><tr><td>' + title + '</td><td>' + industry + '</td><td>' + spec + '</td><td>' + unit + '</td><td>' + date + '</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;height:25%"><tr>含税信息价</tr><tr><td>当前价格</td><td>上期价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td></tr><tr><td>' + str(
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
            insert = "insert into wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status, " \
                     "ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt,post_content_filtered, post_parent, " \
                     "guid, menu_order, post_type, post_mime_type, comment_count) VALUES " \
                     "('%d',now(),now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),'%s','%s','%s','%s','%s','%s','%d')" % \
                     (
                         1, post_content, main_title, '', 'publish', 'open', 'open', '', post_name, '', '', '', 0, '', 0,
                         'post',
                         '',
                         0)
            mh.cud(insert)
            max_id = mh.find(select_max_sql)
            id = int(max_id[0]['id'])
            insert_term = "insert into wp_term_relationships (object_id, term_taxonomy_id) VALUES ('%d','%d')" % (id, 10)
            mh.cud(insert_term)


if __name__ == '__main__':
    insertData()
