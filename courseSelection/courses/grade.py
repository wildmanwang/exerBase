# -*- coding:utf-8 -*-
"""
班级

开班
查看全班成绩
"""
__author__ = "Cliff.wang"

from courses.schoolObject import SchoolObject

class Grade(SchoolObject):

    def __init__(self, school):
        self.title = "grade"
        super().__init__(school)

        num = 0
        for item in self.school.grades:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.fields.append("sID")
        self.sID = "G" + ("00" + str(num))[-3:]
        self.fields.append("startDate")
        self.startDate = input("Input startDate(x to cancel):") #开班日期
        if self.startDate.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("subject")
        self.subject = "<Not yet set up>"
        self.fields.append("teacher")
        self.teacher = "<Not yet set up>"
        self.fields.append("status")
        self.status = False
        self.school.grades.append(self)
        self.students = []
