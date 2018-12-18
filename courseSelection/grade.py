# -*- coding:utf-8 -*-
"""
班级

开班
查看全班成绩
"""
__author__ = "Cliff.wang"

class Grade(object):

    def __init__(self, school):
        self.school = school            #学校
        self.fields = []
        num = 0
        for item in self.school.grades:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.fields.append("sID")
        self.sID = "G" + ("00" + str(num))[-3:]
        self.fields.append("name")
        self.name = input("Input name(x to cancel):")       #班级名称
        if self.name.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("startDate")
        self.startDate = input("Input startDate(x to cancel):") #开班日期
        if self.startDate.upper() == "X":
            raise Exception("User cancelled operation.")
        self.status = False
        self.school.grades.append(self)
