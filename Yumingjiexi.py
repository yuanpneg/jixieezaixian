def main():
    f = open('域名解析.txt', 'a')
    for i in range(1, 981):
        string = str(i)+'.rui123.cn'
        f.write('\n' + string)
    f.close()


if __name__ == '__main__':
    main()
