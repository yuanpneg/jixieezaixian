import pandas as pd

import numpy as np

# a = np.arange(10)
# s= a[2:5:1]
# print(s)

a = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 7]])
print(a[..., 1])
# print(a[1,...])
print(a[..., 1:])
# print(a[...,2])

# ar = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 5]])
# print(ar.ndim)
# print(ar.shape)
# print(ar.size)
# print(ar.itemsize)
# print(ar.dtype)

# ar = np.linspace(1, 1, 10, dtype=int)
# print(ar)
#
# arr = np.logspace(1.0, 2.0, num=10)
# print(arr)
# ar = np.linspace(10,20,21)
# print(ar)
# print(np.zeros(3,5))
# ar = np.random.rand(5)
#
# print(ar)
#
# sr = pd.Series(ar, index=list('abcde'))
#
# print(list(sr.index))
# print(sr)
#
# print(type(sr))

# ar = np.random.random(4) * 100
# print(ar)
#
# sr = pd.Series(ar, index=['Jack', 'Marry', 'Tom', 'Zack'], name='作业1')
#
# idc = [90.0, 92.0, 89.0, 65.0]
#
# srr = pd.Series(idc, index=['Jack', 'Marry', 'Tom', 'Zack'], name='作业1')
# print(sr)
# print(srr)

# ar = np.random.randint(0, 100, 10)
# sr = pd.Series(ar, index=list('abcdefjhig'))
# print(sr)
# print(sr['b'])
# print(sr['c'])
# print(sr[3:6])
# print(sr.values > 50)
#
# st = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], index=list('abcdefjhig'))
# print(st)
