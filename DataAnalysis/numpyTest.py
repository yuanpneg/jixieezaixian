import numpy as np
from functools import reduce


def main():
    # lst = [[1, 3, 5], [2, 4, 6]]
    print(type(list))
    # np_list = np.array(lst, dtype=float)
    # print(type(np_list))
    # print(np_list.shape)
    # print(np_list.ndim)
    # print(np_list.dtype)
    # print(np_list.itemsize)
    # print(np_list.size)
    # print(np.zeros([2, 4]))
    # print(np.random.rand(2, 4))
    # print(np.random.randint(1, 10, 3))
    # print(np.random.choice([10, 20, 30, 2, 8]))
    #
    # print(np.random.beta(1, 10, 100))
    # print(np.arange(1, 11).reshape([2, -1]))
    # print(np.exp(lst))
    # lst = np.array([
    #     [[1, 2, 3, 4], [5, 6, 7, 8]],
    #     [[9, 10, 11, 12], [13, 14, 15, 16]],
    #     [[17, 18, 19, 20], [21, 22, 23, 24]]
    # ])
    #
    # print(lst.sum(axis=2))
    # print(lst.sum(axis=1))
    # print(lst.sum(axis=0))
    #
    # from numpy.linalg import *
    # print(np.eye(3))
    # lst = np.array()


def f(x):
    return x * x


def mul(x, y):
    return x * y


def prod(numbers):
    return reduce(mul, numbers)


if __name__ == '__main__':
    numbers = [3, 5, 7, 9]
    print('3 * 5 * 7 * 9 =', prod(numbers))
    if prod([3, 5, 7, 9]) == 945:
        print('测试成功!')
    else:
        print('测试失败!')
