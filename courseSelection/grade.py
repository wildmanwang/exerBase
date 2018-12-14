# -*- coding:utf-8 -*-
"""
班级

开班
查看全班成绩
"""
__author__ = "Cliff.wang"

class Grade(object):

    def __init__(self, school, name, subject, teacher, startDate):
        self.school = school            #学校
        self.name = name                #班级名称
        self.subject = subject          #课程名称
        self.teacher = teacher          #主讲老师
        self.startDate = startDate      #开班日期

    def showAll(self):
        pass
