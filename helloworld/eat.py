# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import time

def eat(name):
    print("老板，在下{name}，来一笼包子！".format(name=name))
    while True:         #生成器，有限循环
        item = yield    #遇到yield退出生成器，并记录退出点
        print("{item}包子被{name}吃了。".format(item=item, name=name))

def produce():
    print("包子铺开门迎客啦！")
    outList = ['韭菜包', '雪菜包', '猪肉包', '豆沙包', '叉烧包']
    guest1 = eat("张三")      #生成器对象赋值
    next(guest1)                #生成器执行
    guest2 = eat("李四")
    next(guest2)
    for item in outList:
        time.sleep(1)           #模拟执行耗时任务
        print("做了2个{item}包子。".format(item=item))
        guest1.send(item)       #生成器执行
        guest2.send(item)

produce()
