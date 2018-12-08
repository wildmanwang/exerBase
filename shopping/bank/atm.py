#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ATM机：
查询余额
取现
还款
"""

__author__ = 'Cliff Wang'

from card import bankClass

curCard = bankClass("", "")
while True:
    while curCard.IDNumber == "":
        sNumber = ""
        while True:
            sNumber = input("Input your card number:")
            sNumber = sNumber.strip()
            if len(sNumber) != 12:
                print("The card number is invalid.")
            else:
                break
        sPassword = input("Input the password:")
        curCard = bankClass(sNumber, sPassword)
        if len(curCard.info) > 0:
            print(curCard.info)

    sMenu = "Welcome to ATM, input your choice:\n" \
            "1. Query balance.\n" \
            "2. Tack cash.\n" \
            "3. Repay cash.\n" \
            "4. Transaction Record.\n" \
            "0. Exit.\n"
    sChoice = input(sMenu)
    if sChoice == "1":
        curCard.card_query()
        print(curCard.info)
    elif sChoice == "2":
        sInput = input("How much you want to tack:")
        if not sInput.isnumeric():
            print("The number is invalid.")
            continue
        curCard.card_business("takecash", int(sInput))
        if len(curCard.info) > 0:
            print(curCard.info)
        else:
            print("取款成功")
    elif sChoice == "3":
        sInput = input("Give me the money:")
        if not sInput.isnumeric():
            print("The number is invalid.")
            continue
        curCard.card_business("repay", int(sInput))
        if len(curCard.info) > 0:
            print(curCard.info)
        else:
            print("还款成功")
    elif sChoice == "4":
        curCard.card_record()
        print(curCard.info)
    elif sChoice == "0":
        curCard.card_logout()
    else:
        print("Input is invalid.")
