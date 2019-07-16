# 工程造价（市场价）
from wp_file.MysqlHelper import MysqlHelper
import time

def insertData():
    mh = MysqlHelper('localhost', 'root', 'ok', 'ultrax', 'utf8')
    sql = 'select * from top_good_zaojiatongshichangjia limit 100'
    cost_msg = mh.find(sql)
    select_max_sql = "select MAX(aid) as id from pre_portal_article_title"
    if len(cost_msg) > 0:
        for cost in cost_msg:
            title = cost['title']  # 商品名
            brand = cost['brand']  # 品牌
            if brand == "":
                brand = '--'
            city = cost['city']  # =城市
            unit = cost['unit']  # 单位
            company = cost['supplier']  # 公司
            date = cost['updatetime']  # 日期
            timeArray = int(time.mktime(time.strptime(date, '%Y-%m')))
            fac_tax_pre = cost['facTaxPrevious']  # 市场价（含税） 上月
            fac_tax_avg = cost['facTaxAverage']  # 市场价（含税） 平均
            fac_tax_hight = cost['facTaxHighest']  # 市场价（含税） 最大值
            fac_tax_low = cost['facTaxLowest']  # 市场价（含税） 最小值
            current_tax_fac = cost['currentPriceFacTax']  # 市场价（含税）

            fac_pre = cost['facPrevious']  # 市场价（除税） 上月
            fac_avg = cost['facAverage']  # 市场价（除税） 平均
            fac_hight = cost['facHighest']  # 市场价（除税） 最大值
            fac_low = cost['facLowest']  # 市场价（除税） 最小值
            current_fac = cost['currentPriceFac']  # 市场价（除税）

            ref_tax_pre = cost['refTaxPrevious']  # 建议价（含税） 上月
            ref_tax_avg = cost['refTaxAverage']  # 建议价（含税） 平均
            ref_tax_hight = cost['refTaxHighest']  # 建议价（含税） 最大值
            ref_tax_low = cost['refTaxLowest']  # 建议价（含税） 最小值
            current_tax_ref = cost['currentPriceRefTax']  # 建议价（含税）

            ref_pre = cost['refPrevious']  # 建议价（除税） 上月
            ref_avg = cost['refAverage']  # 建议价（除税） 平均
            ref_hight = cost['refHighest']  # 建议价（除税） 最大值
            ref_low = cost['refLowest']  # 建议价（除税） 最小值
            current_ref = cost['currentPriceRef']  # 建议价（除税）

            spec = cost['spec']  # 商品类型
            rate = cost['taxRate']  # 税率
            main_title = title + "&nbsp;&nbsp;&nbsp;" + spec + "&nbsp;&nbsp;&nbsp;"
            pre_content = '<p><table border="1" cellspacing="0" style="width:100%;text-align:center;"><tr>供应商：' + company + '</tr> <tr><td>名称</td><td>规格型号</td><td>品牌</td><td>单位</td><td>城市</td><td>更新时间</td></tr><tr><td>' + title + '</td><td>' + spec + '</td><td>' + brand + '</td><td>' + unit + '</td><td>' + city + '</td><td>' + date + '</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;"><tr>市场价（含税）</tr><tr><td>当前价格</td><td>上月价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td><td>税率</td></tr><tr><td>' + str(
                current_tax_fac) + '</td><td>' + str(fac_tax_pre) + '</td><td>' + str(fac_tax_avg) + '</td><td>' + str(
                fac_tax_hight) + '</td><td>' + str(
                fac_tax_low) + '</td><td>'+rate+'</td></tr></table><table border="1" cellspacing="0" style="width:100%;text-align:center;"><tr>市场价（除税）</tr><tr><td>当前价格</td><td>上月价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td><td>税率</td></tr><tr><td>' + str(
                current_fac) + '</td><td>' + str(fac_pre) + '</td><td>' + str(fac_avg) + '</td><td>' + str(
                fac_hight) + '</td><td>' + str(fac_low) + '</td><td>'+rate+'</td></tr></table>' \
                                                          '<table border="1" cellspacing="0" style="width:100%;text-align:center;"><tr>建议价（含税）</tr><tr><td>当前价格</td><td>上月价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td><td>税率</td></tr><tr><td>' + str(
                current_tax_ref) + '</td><td>' + str(ref_tax_pre) + '</td><td>' + str(ref_tax_avg) + '</td><td>' + str(
                ref_tax_hight) + '</td><td>' + str(ref_tax_low) + '</td><td>'+rate+'</td></tr></table>' \
                                                                  '<table border="1" cellspacing="0" style="width:100%;text-align:center;"><tr>建议价（除税）</tr><tr><td>当前价格</td><td>上月价格</td><td>平均价格</td><td>最高价格</td><td>最低价格</td><td>税率</td></tr><tr><td>' + str(
                current_ref) + '</td><td>' + str(ref_pre) + '</td><td>' + str(ref_avg) + '</td><td>' + str(
                ref_hight) + '</td><td>' + str(ref_low) + '</td><td>'+rate+'</td></tr></table></table></p>'

            insert_title = "insert into pre_portal_article_title (catid,bid,uid,username,title,highlight,author,`from`,`fromurl`," \
                           "url,summary,pic,thumb," \
                           "remote,id,idtype,contents,allowcomment,owncomment,click1,click2,click3,click4," \
                           "click5,click6,click7,click8,tag,dateline,status,showinnernav,preaid,nextaid,htmlmade,htmlname,htmldir) VALUES " \
                           "('%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%s','%d','%d','%d','%d','%d','%d','%d'" \
                           ", '%d', '%d', '%d', '%d', '%d','%d', '%d', '%d', '%d', '%d', '%d', '%s', '%s')" % \
                           (9, 0, 1, 'admin', main_title, '|||', '', '', '', '', '', '', 0, 0, 0, '', 1, 1, 0, 0, 0, 0,
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
