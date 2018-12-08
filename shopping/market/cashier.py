#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
收银机
"""
__author__ = 'Cliff Wang'

import sys, os

sys.path.append(os.path.join(os.path.abspath(".."), "bank"))
from card import bankClass

itemList = [
    {"name": "Item01", "price": 100.00},
    {"name": "Item02", "price": 200.00},
    {"name": "Item03", "price": 300.00},
    {"name": "Item04", "price": 400.00}
]

cartList = []
amtOught = 0.00
amtPaid = 0.00

def menu_item():
    """
    显示购物菜单
    :return:购物选项
    """
    sMenu = ""
    no = 0
    for item in itemList:
        no += 1
        sMenu += "{no}. {name} ￥{price}\n".format(no=no, name=item["name"], price=item["price"])
    sMenu += \
        "S. Show shopping cart\n" \
        "P. Power off."
    print(sMenu)
    sInput = input("Input your choice:")
    return sInput.strip()

def menu_checkout():
    """
    显示结账菜单
    :return:结账选项
    """
    if len(cartList) == 0:
        print("The cart is empty.")
        return "2"
    amt = 0.00
    sMenu = "".center(50, "=")
    sMenu += "\nYou've chosen following items:\n" + "".center(50, "-")
    for item in cartList:
        sMenu += "\n{name},price={price},qty={qty},amt={amt}".format(name=item["name"], price=item["price"],
                                                                     qty=item["qty"], amt=item["price"] * item["qty"])
    sMenu += "\n"
    sMenu += "".center(50, "-")
    sMenu += "\nTotal amt is ￥{amt}\n".format(amt=amtOught)
    sMenu += "1. Check out.\n"
    sMenu += "2. Continue shopping.\n"
    sMenu += "0. Cancel bill.\n"
    sMenu += "".center(50, "=")
    print(sMenu)
    sInput = input("Input your choice:")
    return sInput.strip()

def menu_pay():
    """
    支付菜单
    :return:支付选项
    """
    global amtOught, amtPaid
    sMenu = "".center(50, "=")
    sMenu += "\nYou should pay ￥{amt},Choose payment:".format(amt=amtOught-amtPaid)
    sMenu += "\n1. Cash"
    sMenu += "\n2. Bank Card"
    sMenu += "\n0. Cancel"
    print(sMenu)
    sInput = input("Input your choice:")
    return sInput.strip()

def item_add(no):
    """
    加购物车
    :param no:商品序号
    :return:
    """
    if no >= 1 and no <= len(itemList):
        bFound = False
        for item in cartList:
            if item["name"] == itemList[no - 1]["name"]:
                item["qty"] += 1
                global amtOught
                bFound = True
        if not bFound:
            cartList.append({"name": itemList[no - 1]["name"], "price": itemList[no - 1]["price"], "qty": 1})
        amtOught += itemList[no - 1]["price"]
    else:
        print("You choose a invalid item.")

def check_out():
    """
    结账处理
    :return:{1:"单据结账完成", 0:"单据未结账", -1:"购物车无商品，不需结账"}
    """
    global amtOught, amtPaid
    if len(cartList) == 0:
        return -1
    elif amtOught == amtPaid:
        while len(cartList) > 0:
            cartList.pop()
        amtOught = 0
        amtPaid = 0
        print("*** Checked out ***".center(50, "-"))
        return 1
    else:
        return 0

def pay_cash():
    """
    现金支付
    :return:
    """
    global amtOught, amtPaid
    sInput = input("You should pay cash:￥{amt}".format(amt=amtOught-amtPaid) + ",Input your number:")
    if sInput.isnumeric():
        if int(sInput) > amtOught - amtPaid:
            print("Give change:￥{amt}".format(amt=int(sInput)-(amtOught - amtPaid)))
            amtPaid = amtOught
        else:
            print("Paid cash ￥{amt}".format(amt=int(sInput)))
            amtPaid += int(sInput)
    else:
        print("Input invalid.")

    #调用结账
    return check_out()

def pay_bank():
    """
    银行卡支付
    :return:
    """
    global amtOught, amtPaid

    sNumber = input("You should pay:￥{amt}".format(amt=amtOught-amtPaid) + ",Input bank card number:")
    sNumber = sNumber.strip()
    if len(sNumber) != 12:
        print("The card number is invalid.")
        return -1
    sPassword = input("Input the password:")
    curCard = bankClass(sNumber, sPassword)
    if len(curCard.info) > 0:
        print(curCard.info)
        return -1

    curCard.card_business("consume", amtOught-amtPaid, "Shopping Mall")
    if len(curCard.info) > 0:
        print(curCard.info)
    else:
        print("Paid bank card ￥{amt}".format(amt=amtOught-amtPaid))
        amtPaid = amtOught

    #调用结账
    return check_out()

def bill_cancel():
    """
    取消单据
    :return:
    """
    global amtOught, amtPaid
    if len(cartList) == 0:
        print("The cart is empty.")
        return -1
    else:
        amtOught = 0
        amtPaid = 0
        while len(cartList) > 0:
            cartList.pop()
        print("Bill has cancelled.")

while True:
    sInput = menu_item()
    if sInput.isnumeric():
        #选择了商品
        item_add(int(sInput))
    elif sInput.upper() == "S":
        #显示购物车及结账信息
        sInput = menu_checkout()
        if sInput == "1":
            #结账
            iChecked = -1
            while True:
                sPay = menu_pay()
                if sPay == "1":
                    iChecked = pay_cash()
                elif sPay == "2":
                    iChecked = pay_bank()
                elif sPay == "0":
                    break
                else:
                    print("Input invalid.")
                    continue
                if iChecked == 1:
                    break
        elif sInput == "2":
            #继续选择商品
            continue
        elif sInput == "0":
            #整单取消
            bill_cancel()
            continue
        else:
            print("Input invalid.")
            continue
    elif sInput.upper() == "P":
        break