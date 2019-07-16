
from apscheduler.schedulers.blocking import BlockingScheduler
import pymysql
from recruit.config import *
import selenium

headers = {
    'Host': 'top.baidu.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
cursor = conn.cursor()

def main():
    pass



if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=4)
    scheduler.start()
