import re
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import time
import pymysql


def crawle():
    url = 'https://member.zjtcn.com/common/login.html?url=https://js.zjtcn.com/facx/c0000_t25_d201906_p100_k_qa_qi.html'

    browser = webdriver.Chrome('C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    wait = WebDriverWait(browser, 5)
    browser.get(url)
    username = browser.find_element_by_id('memberID')
    username.send_keys('13766734707')

    pwd = browser.find_element_by_id('pwd')
    pwd.send_keys('13766734707')
    action = ActionChains(browser)
    source = browser.find_element_by_xpath('//*[@id="slider1"]/div/div[2]')  # 需要滑动的元素
    action.click_and_hold(source).perform()  # 鼠标左键按下不放
    action.move_by_offset(400, 0)  # 需要滑动的坐标
    time.sleep(5)
    action.release().perform()  # 释放鼠标
    time.sleep(5)
    # 敲enter键
    pwd.send_keys(Keys.RETURN)
    time.sleep(5)

    conn = pymysql.connect(host='localhost', user='root', password='ok', db='lz_crawler')
    cursor = conn.cursor()
    selectUrlsSql = 'SELECT title, url FROM zaojiatongxinxijia where url not in (select url from top_good_zaojiatongxinxijia)'
    cursor.execute(selectUrlsSql)
    UrlsArray = cursor.fetchall()  # 获取所有对像的url
    for url in UrlsArray:
        detailUrl = url[0]
        detailUrl = "https://js.zjtcn.com/facx/c0000_t0101_d201906_p1_k_qa_qi.html"  # 钢筋
        browser.get(detailUrl)
        detailhtml = browser.page_source
        print(11)
    #         time.sleep(7)
    #         detailhtml = browser.page_source
    #         doc = pq(detailhtml)
    #         title1 = re.search(r"infomStdName = \'(.*?)\'", detailhtml)
    #         title = title1.group(1)
    #         print(title)
    #         specificationType = doc('#li_mdtail > span:nth-child(4)').text()
    #         print(specificationType)
    #         unit = doc('#li_mdtail > span:nth-child(6)').text()
    #         print(unit)
    #         industry = doc('#li_mdtail > span:nth-child(2)').text()
    #         print(industry)
    #         taxInformation1 = re.search(r'<div.*?id="currentPrice".*?>(.*?)</div>', detailhtml)
    #         taxInformation = taxInformation1.group(1)
    #         print(taxInformation)
    #         company = doc(
    #             '#main > div.scj-box-left > div:nth-child(1) > div.e-box.clearfix > div > div.top.clearfix > div.title-name > div > span').text()
    #         print(company)
    #
    #         taxUpprice1 = re.search(r'<span.*?id="upprice".*?>.*?(.*?)</span>', detailhtml)
    #         taxUpprice = taxUpprice1.group(1)
    #         print(taxUpprice)
    #         taxAvg1 = re.search(r'<span.*?id="avgprice".*?>.*?(.*?)</span>', detailhtml)
    #         taxAvg = taxAvg1.group(1)
    #         print(taxAvg)
    #         taxMax1 = re.search(r'<span.*?id="maxprice".*?>.*?(.*?)</span>', detailhtml)
    #         taxMax = taxMax1.group(1)
    #         print(taxMax)
    #         taxMin1 = re.search(r'<span.*?id="minprice".*?>.*?(.*?)</span>', detailhtml)
    #         taxMin = taxMin1.group(1)
    #         print(taxMin)
    #
    #         notaxInformation1 = re.search(r'<div.*?id="currentPriceTax".*?>(.*?)</div>', detailhtml)
    #         notaxInformation = notaxInformation1.group(1)
    #         print(notaxInformation)
    #
    #         notaxUpprice1 = re.search(r'<span.*?id="uppricenotax".*?>.*?(.*?)</span>', detailhtml)
    #         notaxUpprice = notaxUpprice1.group(1)
    #         print(notaxUpprice)
    #         notaxAvg1 = re.search(r'<span.*?id="avgpricenotax".*?>.*?(.*?)</span>', detailhtml)
    #         notaxAvg = notaxAvg1.group(1)
    #         print(notaxAvg)
    #         notaxMax1 = re.search(r'<span.*?id="maxpricenotax".*?>.*?(.*?)</span>', detailhtml)
    #         notaxMax = notaxMax1.group(1)
    #         print(notaxMax)
    #         notaxMin1 = re.search(r'<span.*?id="minpricenotax".*?>.*?(.*?)</span>', detailhtml)
    #         notaxMin = notaxMin1.group(1)
    #         print(notaxMin)
    #
    #         infomIssueDate1 = re.search(r"infomIssueDate = \'(.*?)\'", detailhtml)
    #         infomIssueDate = infomIssueDate1.group(1)
    #         print(infomIssueDate)
    #
    #         if taxUpprice not in '***':
    #             taxUpprice = taxUpprice.replace('<em>¥</em>', '')
    #             taxAvg = taxAvg.replace('<em>¥</em>', '')
    #             taxMax = taxMax.replace('<em>¥</em>', '')
    #             taxMin = taxMin.replace('<em>¥</em>', '')
    #             notaxUpprice = notaxUpprice.replace('<em>¥</em>', '')
    #             notaxAvg = notaxAvg.replace('<em>¥</em>', '')
    #             notaxMax = notaxMax.replace('<em>¥</em>', '')
    #             notaxMin = notaxMin.replace('<em>¥</em>', '')
    #             try:
    #                 countSql = 'select count(*) from top_good_zaojiatongxinxijia where url = "%s" ' % (url)
    #                 cursor.execute(countSql)
    #                 Count = cursor.fetchone()[0]
    #                 if Count < 1:
    #                     insertSql = "INSERT INTO top_good_zaojiatongxinxijia (company, industry, infomIssueDate, notaxAvg, notaxInformation, notaxMax, notaxMin, notaxUpprice, specificationType, taxAvg, taxInformation, taxMax, taxMin, taxUpprice, title, unit, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
    #                         company, industry, infomIssueDate, notaxAvg, notaxInformation, notaxMax, notaxMin,
    #                         notaxUpprice,
    #                         specificationType, taxAvg, taxInformation, taxMax, taxMin, taxUpprice, title, unit,
    #                         detailUrl)
    #                     cursor.execute(insertSql)
    #                     conn.commit()
    #                     print('存储到数据库成功')
    #                 deletesql = "DELETE from top_good_zaojiatongxinxijia where notaxUpprice like '%*%'"
    #                 cursor.execute(deletesql)
    #             except Exception as e:
    #                 print(e.args)
    #                 conn.rollback()
    #                 print('存储到数据库失败')
    # finally:
    # browser.close()


if __name__ == '__main__':
    crawle()
