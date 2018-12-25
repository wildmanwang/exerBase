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
        sInput = input("No school!\nYou want to create a school?yes/no")
        if sInput.upper() == "YES":
            School.schoolAdd()
    else:
        num = 0
        for item in schs:
            num += 1
            ls_menu += "{num}\t{name}\n".format(num=num, name=item[:-4])
        ls_menu += "Input your choice:"
        sInput = input(ls_menu)
        while not sInput.isdigit() or int(sInput) < 1 or int(sInput) > num:
            sInput = input(ls_menu)
        name = schs[int(sInput) - 1][:-4]
        school = School.dataLoad(sPathData, name)
        sChoose = input("1 Reg student\n2 Login\nInput your choice:")
        if sChoose == "1":
            try:
                school.add("student")
            except Exception as e:
                print(str(e))
            else:
                School.dataDump(sPathData, school)
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
                bSuperMenu = mem.hasChildren(curLevel + sChoose)
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
                        if len(curLevel) > 0:
                            sSuper = mem.menu[curLevel].split("-")[1]
                        else:
                            sSuper = ""
                        sFun = mem.menu[curLevel + sChoose].split("-")[1]
                        if len(sSuper) > 0 and sFun.upper() in ("PRINTLIST", "ADD", "MODIFY", "DELETE"):
                            getattr(mem.school, sFun)(sSuper)
                        elif sFun.upper() in ("GRADESETSUBJECT", "GRADESETTEACHER", "GRADESTART"):
                            getattr(mem.school, sFun)()
                        else:
                            getattr(mem, sFun)()
                        if school.bModified:
                            School.dataDump(sPathData, school)
                    except Exception as e:
                        print(str(e))
