from sphinx.util import requests
from pyquery import PyQuery as pq
from wp_file.MysqlHelper import MysqlHelper
from apscheduler.schedulers.blocking import BlockingScheduler

headers = {
    'Host': 'top.baidu.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}


def main():
    mh = MysqlHelper('47.110.88.64', 'root', 'admin963', 'zhizhudashi', 'utf8')

    url_list = [1, 342, 1679, 344, 11]
    for i in url_list:
        url = 'http://top.baidu.com/buzz?b=' + str(i) + '&c=513&fr=topbuzz_b42_c513'
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'gb2312'
            html = response.text
            doc = pq(html)
            new_names = doc(".list-title")
            for name in new_names.items():
                string = name.text()
                select_sql = 'select * from keywords where title = "%s"' % (string)
                id = mh.find_id(select_sql)
                if id != None and id != '' and id != 0:
                    continue
                else:
                    insert_sql = "insert into keywords (title,object_id) values ('%s',%d)" % (string, 1)
                    mh.cud(insert_sql)
            # f = open('百度热词.txt', 'a')
            # for name in new_names.items():
            #     string = name.text()
            #     f.write('\n' + str(string))
            # f.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=4)
    scheduler.start()
