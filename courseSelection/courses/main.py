#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
程序入口
"""

__author__ = 'Cliff Wang'

import os
from courses.school import School

def course_main(sPathRoot):
    sPathData = os.path.join(sPathRoot, "data")
    schs = [i for i in os.listdir(sPathData) if i[-4:] == ".dat"]
    ls_menu = "Select a school:\n"
    num = len(schs)
    if num == 0:
        ls_menu = "No school!"
    else:
        for item in schs:
            ls_menu += "{num}\t{name}\n".format(num=num, name=item[:-4])
        sInput = input(ls_menu)
        while not sInput.isdigit() or int(sInput) < 1 or int(sInput) > num:
            sInput = input(ls_menu)
        name = schs[int(sInput) - 1][:-4]
        school = School.dataLoad(sPathData, name)
        try:
            mem = school.login()
        except Exception as e:
            print(str(e))
        else:
            curLevel = ""
            sChoose = "N"
            while curLevel + sChoose != "0":
                mem.printMenu(curLevel)
                sChoose = input("Input your choice:")
                bSuperMenu = False
                for key in mem.menu.keys():
                    iLen = len(curLevel + sChoose)
                    if key[:iLen] == curLevel + sChoose and len(key) > iLen:
                        bSuperMenu = True
                        break
                if bSuperMenu:
                    curLevel = curLevel + sChoose
                elif sChoose == "0":
                    if len(curLevel) > 0:
                        curLevel = curLevel[:len(curLevel) - 1]
                        sChoose = "N"
                    else:
                        school.logout()
                        if school.bLogin:
                            sChoose = "N"
                else:
                    try:
                        sFun = mem.menu[curLevel + sChoose].split("-")[1]
                        getattr(mem, sFun)()
                        if school.bModified:
                            School.dataDump(sPathData, school)
                    except Exception as e:
                        print(str(e))
