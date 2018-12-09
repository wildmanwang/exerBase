# -*- coding:utf-8 -*-
"""
学校

创建学校
开设课程
创建班级
招聘老师
"""
__author__ = "Cliff.wang"

class School(object):

    def __init__(self, name, addr):
        self.name = name            #名称
        self.addr = addr            #地址
        self.gradesOld = []         #曾经开过的课程
        self.grades = []            #当前有效课程
        self.teachers = []          #教职工列表
        self.students = []          #学生列表

    def offerCourses(self):
        pass

    def openSubject(self):
        pass

    def hireStaff(self):
        pass
