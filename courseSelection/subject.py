# -*- coding:utf-8 -*-
"""
课程

建立课程档案
"""
__author__ = "Cliff.wang"

class Subject(object):

    def __init__(self, school):
        self.school = school
        self.fields = []
        num = 0
        for item in self.school.subjects:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.fields.append("sID")
        self.sID = "S" + ("00" + str(num))[-3:]
        self.fields.append("name")
        self.name = input("Input name(x to cancel):")       #课程名称
        if self.name.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("weeks")
        self.weeks = input("Input weeks(x to cancel):")     #学完该课程要多少周
        if self.weeks.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("chapter")
        self.chapter = input("Input chapter(x to cancel):") #包含多少次成绩
        if self.chapter.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("fee")
        self.fee = input("Input fee(x to cancel):")         #学费
        if self.fee.upper() == "X":
            raise Exception("User cancelled operation.")
        self.status = True
        self.school.subjects.append(self)
