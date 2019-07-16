import time
import datetime
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pymysql
from recruit.config import *

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H734T8RC07W33G7D"
proxyPass = "90D30C8BC19B2430"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


def get_page_index(kw, page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    indexUrl = 'https://search.51job.com/list/000000,000000,0000,26%252C51%252C09%252C50,1,99,' + kw + ',2,' + page + \
               '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=' \
               '0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    try:
        response = requests.get(indexUrl, headers=headers)
        response.encoding = 'gbk'
        print(indexUrl)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


def parse_page_index(html):
    soup = BeautifulSoup(html, 'html.parser')
    for urllist in soup.select('.el p span'):
        detailUrlList = urllist.select('a')[0]['href']
        yield detailUrlList


def get_page_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页失败')
        return None


def Tianyan(company):
    # proxy = get_proxy()
    # if proxy == None:
    #     return Tianyan(company)
    # proxies = {
    #     'http': 'http://46.101.145.206:3128'
    # }
    data = {
        'key': company
    }
    headers = {
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    url = 'https://www.tianyancha.com/search?' + urlencode(data)
    # print(url)
    try:
        response = requests.get(url, headers=headers)
        time.sleep(1)
        # print(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


def parse_page_detail(detailUrlHtml):
    doc = pq(detailUrlHtml)
    title = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > h1').text()  # 标题
    company = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.cname > a.catn').text()  # 公司名称
    salary1 = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > strong').text()
    salaryList = salary1.split("/")
    salary = salaryList[0]  # 薪资
    region1 = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.msg.ltype').text()
    regionList = region1.split("  |  ")
    strTime = ''
    experience = ''
    people = ''
    education = ''
    region = ''
    for region in regionList:
        if '发布' in region:
            strTime1 = region
            strTimeList = strTime1.split("发布")
            strTime = "2019-" + strTimeList[0] + " 00:00"  # 发布时间
        if '经验' in region:
            experience = region  # 工作经验
        if '人' in region:
            people = region  # 招收人数
        if '大专' in region or '本科' in region or '中专' in region:
            education = region  # 招收人数
    region = regionList[0].split("-")[0]  # 地区
    description1 = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(1) > div > p')  # 任职要求
    descriptions = str(description1)
    pattern = re.compile(' style=\"(.*?)\"')
    description = pattern.sub('', descriptions).replace(' ', '').replace('	', '').replace('&#13;', '').replace('\'',
                                                                                                                  '')
    companyProfile = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(3) > div').text()  # 公司简介
    mainCompany = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(3)').attr(
        'title')  # 公司主营
    numberOfCompanies = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(2)').attr(
        'title')  # 公司人数
    companyNature = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(1)').attr(
        'title')  # 公司性质
    workplace1 = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(2) > div > p').text()  # 工作地址
    workplace = ''
    if workplace1 != '':
        workplaceList = workplace1.split("上班地址：")
        workplace = region + workplaceList[1]  # 地址
        workplace = workplace.replace("-", "")
    jobhighlights = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > div').text()
    company = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.cname > a.catn').text()  # 公司
    positiontitle = doc(
        'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > h1').attr(
        'title')  # 标题

    time1 = time.strptime(strTime, "%Y-%m-%d %H:%M")
    time2 = time.strftime("%Y-%m-%d", time1)
    todayDate = datetime.date.today()
    today = todayDate.strftime("%Y-%m-%d")
    oneday = datetime.timedelta(days=1)
    # yesterdayDate = todayDate - oneday
    # yesterday=yesterdayDate.strftime("%Y-%m-%d")
    # twoday = datetime.timedelta(days=2)
    # beforeYesterdayDate = todayDate - twoday
    # beforeYesterday=beforeYesterdayDate.strftime("%Y-%m-%d")
    timeDate = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    time3 = time.strptime(timeDate, "%Y-%m-%d %H:%M")
    addtime = int(time.mktime(time3))  # time3
    edittime = int(time.mktime(time3))  # time3
    authstatus = 0
    authfailreason = ""
    authtime = 0
    hits = 0
    userid = 0
    regionid = 0
    latitude = ""
    longitude = ""
    webname = '前程'
    positionid = ""
    print(time2)
    try:
        # or time2 == yesterday or time2 == beforeYesterday
        if time2 == today:
            # 执行sql
            countSql = 'select count(*) from qiancheng where company = "%s"  and title = "%s"' % (company, title)
            cursor.execute(countSql)
            Count = cursor.fetchone()[0]
            if Count < 1:
                if '项目经理' in title:
                    positiontitle = '项目经理'
                if '项目主管' in title:
                    positiontitle = '项目经理'
                if '隧道' in title:
                    positiontitle = '隧道工程师'
                if '土建勘察' in title:
                    positiontitle = '地质勘察'
                if '结构工程师' in title:
                    positiontitle = '结构工程师'
                if '园林/景观设计' in title:
                    positiontitle = '园林/景观设计'
                if '室内设计' in title:
                    positiontitle = '室内设计师'
                if '现场' in title:
                    positiontitle = '现场工程师'
                if '水电' in title:
                    positiontitle = '水电工程师'
                if '绘图' in title:
                    positiontitle = '绘图员'
                if '动画设计' in title:
                    positiontitle = '平面/动画设计/多媒体制作'
                if '绿化' in title:
                    positiontitle = '绿化工程师'
                if '高级建筑师' in title:
                    positiontitle = '总建筑师/高级建筑师/主创建筑师'
                if '古建筑设计' in title:
                    positiontitle = '古建筑设计师'
                if '施工图设计' in title:
                    positiontitle = '施工图设计师'
                if '方案' in title:
                    positiontitle = '方案设计师'
                if '建筑助理' in title:
                    positiontitle = '助理建筑师'
                if '建模' in title:
                    positiontitle = '建模'
                if '渲染' in title:
                    positiontitle = '渲染'
                if '后期' in title:
                    positiontitle = '后期制作'
                if '苗场' in title:
                    positiontitle = '苗场技术员'
                if '建造' in title:
                    positiontitle = '建造师'
                if '项目管理' in title:
                    positiontitle = '项目管理工程师'
                if '责任' in title:
                    positiontitle = '责任工程师'
                if '顾问' in title:
                    positiontitle = '咨询/评估/顾问'
                if '工长' in title:
                    positiontitle = '工长'
                if '调试员' in title:
                    positiontitle = '调试员/工程师'
                if '混凝土' in title:
                    positiontitle = '混凝土工程师'
                if '岩土' in title:
                    positiontitle = '岩土/地质工程师'
                if '建筑材料' in title:
                    positiontitle = '建筑材料工程师'
                if '调度员' in title:
                    positiontitle = '调度员'
                if '地基' in title:
                    positiontitle = '地基工程师'
                if '桩基' in title:
                    positiontitle = '桩基工程师'
                if '管道' in title:
                    positiontitle = '管道工程师'
                if '爆破' in title:
                    positiontitle = '爆破工程师'
                if '监理' in title:
                    positiontitle = '监理员/工程师'
                if '爆破' in title:
                    positiontitle = '爆破工程师'
                if '隧道设计' in title:
                    positiontitle = '铁路隧道设计'
                if '铁路结构' in title:
                    positiontitle = '铁路结构设计'
                if '信号设计' in title:
                    positiontitle = '信号设计'
                if '铁路线路' in title:
                    positiontitle = '铁路线路设计'
                if '防水' in title:
                    positiontitle = '防水工程师'
                if '轨道' in title:
                    positiontitle = '轨道工程师'
                if '地下采暖' in title:
                    positiontitle = '地下采暖设计'
                if '精装' in title:
                    positiontitle = '精装设计师/工程师'
                if '软装' in title:
                    positiontitle = '软装设计师'
                if '照明' in title:
                    positiontitle = '照明工程师'
                if '消防' in title:
                    positiontitle = '消防工程师'
                if '木工' in title:
                    positiontitle = '木工'
                if '水暖' in title:
                    positiontitle = '水暖工程师'
                if '模板' in title:
                    positiontitle = '模板工'
                if '钣金' in title:
                    positiontitle = '钣金工'
                if '抹灰' in title:
                    positiontitle = '抹灰工'
                if '起重' in title:
                    positiontitle = '起重工'
                if '砌筑' in title:
                    positiontitle = '砌筑工'
                if '检测' in title:
                    positiontitle = '检测员'
                if '质检' in title:
                    positiontitle = '质检员'
                if '木工' in title:
                    positiontitle = '木工'
                if '维修' in title:
                    positiontitle = '维修/检修'
                if '加固' in title:
                    positiontitle = '加固工程师'
                if '幕墙' in title:
                    positiontitle = '幕墙设计师/工程师'
                if '燃气' in title:
                    positiontitle = '燃气工程师'
                if 'IE' in title:
                    positiontitle = 'IE工程师'
                if 'LED' in title:
                    positiontitle = 'LED工程师'
                if '机电' in title:
                    positiontitle = '机电工程师'
                if '安装' in title:
                    positiontitle = '安装工程师'
                if '机电' in title:
                    positiontitle = '机电工程师'
                if '排水' in title:
                    positiontitle = '城市给排水工程师'
                if '计量' in title:
                    positiontitle = '计量员/计量工程师'
                if '招投' in title:
                    positiontitle = '招投标员/工程师'
                if '机械操作' in title:
                    positiontitle = '工程机械操作手'
                if '工程车司机' in title:
                    positiontitle = '工程车司机'
                if '劳务员' in title:
                    positiontitle = '劳务员'
                if '物业人员' in title:
                    positiontitle = '物业人员'
                if '混凝土' in title:
                    positiontitle = '混凝土工'
                if '油漆' in title:
                    positiontitle = '油漆工'
                if '线路工程' in title:
                    positiontitle = '线路工程师'
                if '暖通空调' in title:
                    positiontitle = '暖通空调工程师'
                if '家具设计' in title:
                    positiontitle = '家具设计师'
                if '通信管线' in title:
                    positiontitle = '通信管线工程师'
                if '通信管线' in title:
                    positiontitle = '通信管线工程师'
                if '沥青' in title:
                    positiontitle = '沥青/养护人员'
                if '养护' in title:
                    positiontitle = '沥青/养护人员'
                if '钢结构' in title:
                    positiontitle = '钢结构工程师'
                if '弱电' in title:
                    positiontitle = '弱电工程师'
                if '弱电' in title:
                    positiontitle = '弱电工程师'
                if '强电' in title:
                    positiontitle = '强电工程师'
                if '布线' in title:
                    positiontitle = '综合布线'
                if '土建' in title:
                    positiontitle = "土建工程师"
                if '技术员' in title:
                    positiontitle = '技术员/技术负责人'
                if '预算员' in title:
                    positiontitle = '预算员/工程师'
                if '安全员' in title:
                    positiontitle = '安全员/工程师'
                if '资料员' in title:
                    positiontitle = '资料员'
                if '材料员' in title:
                    positiontitle = '材料员'
                if '施工员' in title:
                    positiontitle = '施工员'
                if '质检员' in title:
                    positiontitle = '质检员'
                if '测量员' in title:
                    positiontitle = '测量/测绘工程师'
                if '质量员' in title:
                    positiontitle = '质检员'
                if '建造师' in title:
                    positiontitle = '建造师'
                if '总工' in title:
                    positiontitle = '总工程师/高级工程师'
                if '造价' in title:
                    positiontitle = '造价员/工程师'
                if '招投标员' in title:
                    positiontitle = '招投标员/工程师'
                if '平面设计师' in title:
                    positiontitle = '平面设计师'
                if '建筑设计师' in title:
                    positiontitle = '建筑师/建筑设计师'
                # tianYanHtml = Tianyan(company)
                # telephone = ""
                # if tianYanHtml != None:
                #     tiYandq = pq(tianYanHtml)
                #     telephone = tiYandq(
                #         "#web-content > div > div.container-left > div > div.result-list > div:nth-child(1) > div > div.content > div.contact > div:nth-child(1) > span:nth-child(2)").text()
                #     if tiYandq == None:
                #         telephone = ""
                #         print("telephone~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                # print(telephone)
                print(title)
                print(webname)
                print(company)
                print(description)
                if workplace != '' or description != '' or description.strip() or company.strip() or positiontitle.strip() or workplace.strip() or salary.strip() or workplace.strip():
                    insertSql = 'INSERT INTO qiancheng (webname, title, company, positionid, positiontitle, experience, salary, description, workplace, region, education, people, companyProfile, mainCompany, companyNature, numberOfCompanies, jobHighlights, addtime, edittime, authstatus, authfailreason, authtime, hits, userid, regionid, latitude, longitude) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "\'%s\'", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", \'%s\', "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                        webname, title, company, positionid, positiontitle, experience, salary, description, workplace,
                        region,
                        education, people, companyProfile, mainCompany, companyNature, numberOfCompanies, jobhighlights,
                        addtime,
                        edittime, authstatus, authfailreason, authtime, hits, userid, regionid, latitude, longitude
                    )
                    cursor.execute(insertSql)
                print('存储到数据库成功')
                # updateTelephone = 'update qiancheng set telephone =SUBSTRING_INDEX(telephone,"-",2) where company = "%s" ' % (
                #     company)
                updatePositionId = 'update tp_job_position p,qiancheng r set r.positionid=p.id where r.positiontitle=p.title and company="%s"' % (
                    company)
                # selectCharacters = 'select * from characters'
                # cursor.execute(selectCharacters)
                # characterList = cursor.fetchall()
                # for characters in characterList:
                #     updateDescription = 'update qiancheng set description = replace(description,"%s","") where company="%s"' % (
                #         characters[0], company)
                #     cursor.execute(updateDescription)
                isNullPositionIdSql = 'select positionid from qiancheng where company ="%s"' % (company)
                cursor.execute(isNullPositionIdSql)
                isNull = cursor.fetchone()[0]
                if isNull == None:
                    # selectPositionTitle = 'SELECT title FROM tp_job_position'
                    # cursor.execute(selectPositionTitle)
                    # positionTitleList = cursor.fetchall()
                    # for postionTitle in positionTitleList:
                    updatePositionIdSql = "update tp_job_position p,qiancheng r set r.positionid=p.positionid where r.positiontitle=p.title and company='%s' " % (
                        company)
                    cursor.execute(updatePositionIdSql)
                # cursor.execute(updateTelephone)
                cursor.execute(updatePositionId)
                nullPositionIdSql = 'select positionid from qiancheng where company ="%s"' % (company)
                cursor.execute(nullPositionIdSql)
                isNull2 = cursor.fetchone()[0]
                if isNull2 == '':
                    delectsql = 'delete from qiancheng where company ="%s"' % (company)
                    cursor.execute(delectsql)
                delectsql = 'delete from qiancheng where description=""or description is null or workplace is null or workplace ="" or salary="" or positionid="" or length(description)<200'
                cursor.execute(delectsql)
                conn.commit()
    except Exception as e:
        print(e.args)
        conn.rollback()
        print('存储到数据库失败')


def main(kw, page):
    indexHtml = get_page_index(kw, page)
    detailUrlList = parse_page_index(indexHtml)
    for detailUrl in detailUrlList:
        print(detailUrl)
        strs = 'https://jobs.51job.com'
        if strs in detailUrl:
            detailUrlHtml = get_page_detail(detailUrl)
            if detailUrlHtml:
                parse_page_detail(detailUrlHtml)


if __name__ == '__main__':
    # '技术员', '质检员', '质量员', '测量员', '建造师', '预算员', '安全员', '资料员', '材料员', '施工员， 调度员, 水暖工程师
    # 木工, 油漆工, 总工, 水电工程师, 造价员 砌筑工 消防工程师  平面设计师 建筑设计师'
    # kwlist = ['技术员', '质检员', '质量员', '测量员', '建造师', '预算员', '安全员', '资料员', '材料员', '施工员','总工','造价员',
    # '消防工程师','平面设计师','建筑设计师']
    kwlist = ['平面设计师']
    groups = [x * 1 for x in range(GROUP_START, GROUP_END + 1)]
    for kw in kwlist:
        for page in groups:
            print('kw:' + kw)
            main(kw, str(page))
            time.sleep(1)