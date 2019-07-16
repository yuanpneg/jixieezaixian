import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# socre = np.array([[80, 88], [81, 98], [85, 80], [82, 84]])
#
# q = np.array([[0.4], [0.6]])
#
# result = np.dot(socre, q)
#
# print(result)
# print('--------------------------------------------')
# v1 = [[0, 1, 2, 3, 4, 5],
#       [6, 7, 8, 9, 10, 11]]
# print(v1)
#
# v2 = [[12, 13, 14, 15, 16, 17],
#       [18, 19, 20, 21, 22, 23]]
#
# result1 = np.vstack((v1, v2))
# result2 = np.hstack((v1,v2))
# print(result2)
# print(result1)

print(pd.Series(np.arange(4, 10)))

print(pd.Series([11, 12, 13], index=['北京', '上海', '深圳']))

print(pd.Series({"北京": 11, "上海": 12, "深圳": 14}))

data_3_4 = pd.DataFrame(np.arange(10, 22).reshape(3, 4))

print(data_3_4)
print('-------------------------------')
print(data_3_4[3][0:4])

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
pro_name = ["C++", "PYTHON", "JAVA", "GO", "SWIFT"]
pro_time = [10, 15, 5, 3, 1]
plt.pie(pro_time, labels=pro_name, autopct="%3.2f", colors=["#ea6f5a", "#509839", "#0c8ac5", "#d29922", "#fdf6e3"])

plt.title(u"学习时间分配")

plt.axis("equal")

plt.legend(loc="best")

plt.savefig("./pro_learn.png")

plt.show()
