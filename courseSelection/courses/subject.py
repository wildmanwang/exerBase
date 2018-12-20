# -*- coding:utf-8 -*-
"""
课程

建立课程档案
"""
__author__ = "Cliff.wang"

from courses.schoolObject import SchoolObject

class Subject(SchoolObject):

    def __init__(self, school):

        super().__init__(school)

        num = 0
        for item in self.school.subjects:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.fields.append("sID")
        self.sID = "S" + ("00" + str(num))[-3:]
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

    def add(self):
        mem = Subject(self.school)
        self.school.bModified = True
        print("{title} {name} is added success.".format(title=self.title.capitalize(), name=self.name))
