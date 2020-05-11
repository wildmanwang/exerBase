# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

def fun1(x):
    if x > 0:
        print(x)
        fun1(x - 1)

def fun2(x):
    if x > 0:
        fun2(x - 1)
        print(x)

# fun2(5)
for i in range(3, -2, -1):
    print(i)