# 工程造价（参考价）
from wp_file.MysqlHelper import MysqlHelper
import time
from urllib.parse import quote


def insertData():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'wordpress', 'utf8')
    sql = 'select * from top_good_zaojiatongcankaojia'
    cost_msg = mh.find(sql)
    select_max_sql = "select MAX(id) as id from wp_posts"
    if len(cost_msg) > 0:
        for cost in cost_msg:
            date = cost['updatetime']  # 发布日期
            title = cost['materialRef_name'] # 标题名称
            post_name = quote(title, 'tuf-8')
            first_title = cost['title']
            city = cost['region']  # 城市/省
            unit = cost['unit']  # 单位
            timeArray = int(time.mktime(time.strptime(str(date).split(" ")[0], '%Y-%m-%d')))
            avg = cost['avg']  # 均价
            price_min = cost['min']  # 最小值
            price_max = cost['max']  # 最大值
            upanddown = cost['upanddown']  # 涨跌价
            source = cost['source']  # 来源
            spec = cost['specificationType']  # 商品类型
            main_title = title + "&nbsp;&nbsp;&nbsp;" + spec + "&nbsp;&nbsp;&nbsp;" + source + "&nbsp;&nbsp;&nbsp;" + city
            post_content = '<p><table border="1" cellspacing="0" style="width:100%;text-align:center;height:20%"><tr>' + first_title + \
                           '</tr> <tr><td>产品名称</td><td>规格型号</td><td>单位</td><td>更新时间</td><td>城市</td><td>来源</td></tr><tr><td>' + title + '</td><td>' + spec + '</td><td>' + unit + '</td><td>' + date + '</td><td>' + city + '</td><td>' + source + '</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;height:20%"><tr style="width:100%;text-align:center;height:15%">参考价（单位：元）</tr><tr><td>最小价格</td><td>最大价格</td><td>平均价格</td><td>涨跌价格</td></tr><tr><td>' + str(
                price_min) + '</td><td>' + str(price_max) + '</td><td>' + str(avg) + '</td><td>' + str(
                upanddown) + '</td>'
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
