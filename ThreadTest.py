import threading
from time import ctime, sleep


def super_player(file, time):
    for i in range(2):
        print('Start playing : %s! %s' % (file, ctime()))


list = {'爱情买卖.mp3': 3, '阿凡达': 4, '我和你.mp3': 4}

threads = []

files = range(len(list))


for file, time in list.items():
    t = threading.Thread(target=super_player, args=(file, time))
    threads.append(t)

if __name__ == '__main__':
    for i in files:
        threads[i].start()
    for i in files:
        threads[i].join()

    print("all over %s" % ctime())
