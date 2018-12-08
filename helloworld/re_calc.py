# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
"""
测试正则表达式
编写一个计算器，实现加减乘除以及括弧优先
"""

__author__ = 'Cliff Wang'

import re


def calcStrstandard(strcalc):
    """
    把计算式标准化，删除多余的空格等
    :param strcalc:
    :return:标准化的计算式
    """
    strcalc=re.sub(" ","",strcalc)          #替换空格
    strcalc=re.sub("（","\(",strcalc)        #替换全角（
    strcalc=re.sub("）","\)",strcalc)        #替换全角）
    return strcalc


def judgeOver(strcalc):
    """
    判断计算是否结束
    :param strcalc:
    :return:结束返回True，否则返回False
    """
    if re.match("\-?\d+\.?\d+",strcalc):
        #匹配一个数字
        return True
    else:
        #不是一个数字
        return False


def getBrackets(strcalc):
    """
    获取最里层括弧
    :param strcalc:
    :return: 获取最里层括弧的起始位和长度(start,len)，如果没有括弧，返回(-1,0)
    """
    obj = re.search("\([\d|\.|\+|\-|\*|\/]+\)",strcalc)
    if obj:
        return obj.start(),obj.end() - obj.start()
    else:
        return -1,0


def calcHigh(strcalc):
    """
    无括弧计算乘除
    :param strcalc:
    :return:有乘除时，返回经过一层计算后的计算结果以及True(result,True)，否则返回(str,False)
    """
    obj = re.search("(\-?[\d|\.]+)(\*|\/)(\-?[\d|\.]+)",strcalc)
    if obj:
        num1 = float(obj.group(1))
        num2 = float(obj.group(3))
        if obj.group(2) == "*":
            result = float(num1) * float(num2)
        else:
            result = float(num1) / float(num2)
        strcalc = re.sub("(\-?[\d|\.]+)(\*|\/)(\-?[\d|\.]+)",str(result),strcalc,count=1)
        obj = re.search("^\((\-?[\d|\.]+)\)$",strcalc)
        if obj:
            strcalc = re.sub("^\((\-?[\d|\.]+)\)$",obj.group(1),strcalc,count=1)
        return str(strcalc),True
    else:
        return strcalc,False


def calcLow(strcalc):
    """
    无括弧计算加减
    :param strcalc:
    :return: 有加减时，返回经过一层计算后的计算结果以及True(result,True)，否则返回(str,False)
    """
    obj = re.search("(\-?[\d|\.]+)(\+|\-)(\-?[\d|\.]+)",strcalc)
    if obj:
        num1 = obj.group(1)
        num2 = obj.group(3)
        if obj.group(2) == "+":
            result = float(num1) + float(num2)
        else:
            result = float(num1) - float(num2)
        strcalc = re.sub("(\-?[\d|\.]+)(\+|\-)(\-?[\d|\.]+)",str(result),strcalc,count=1)
        obj = re.search("^\((\-?[\d|\.]+)\)$",strcalc)
        if obj:
            strcalc = re.sub("^\((\-?[\d|\.]+)\)$",obj.group(1),strcalc,count=1)
        return str(strcalc), True
    else:
        return strcalc,False


def calcNoBrackets(strcalc):
    """
    无括弧计算
    :param strcalc:
    :return: 返回结果
    """
    strcalc,result = calcHigh(strcalc)
    while result:
        strcalc, result = calcHigh(strcalc)
    strcalc,result = calcLow(strcalc)
    while result:
        strcalc, result = calcLow(strcalc)
    return strcalc


while True:
    strinput = input("Input calc string:")
    #strinput = "3*2+5/(12-9)*(9+6*3/(12-8))"
    if strinput == 'Q':
        break
    strcalc = calcStrstandard(strinput)
    if strcalc == "":
        print("输入算式无效！")
    else:
        while not judgeOver(strcalc):
            strstart,strlen = getBrackets(strcalc)
            if strlen > 0:
                strtmp = strcalc[strstart:strstart+strlen]
                strtmp = calcNoBrackets(strtmp)
                strcalc = strcalc[0:strstart] + strtmp + strcalc[strstart+strlen:]
            else:
                strcalc = calcNoBrackets(strcalc)

        print("算式[{str1}]的结算结果是：{str2}".format(str1=strinput,str2=strcalc))
