from xpinyin import Pinyin


pin = Pinyin()
test1 = pin.get_pinyin("大河向东流")   #默认分割符为-
print(test1.replace("-",""))




