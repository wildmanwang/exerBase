# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import gevent

def fun1():
    print("Running in fun1...")
    gevent.sleep(5)
    print("Fun1 is over.")

def fun2():
    print("Running in fun2...")
    gevent.sleep(3)
    print("Fun2 is over.")

def fun3():
    print("Running in fun3...")
    gevent.sleep(4)
    print("Fun3 is over.")

gevent.joinall([
    gevent.spawn(fun1),
    gevent.spawn(fun2),
    gevent.spawn(fun3)
])
