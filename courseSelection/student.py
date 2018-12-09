# -*- coding:utf-8 -*-
"""
学生

报名
查看档案
"""
__author__ = "Cliff.wang"

from schoolMember import SchoolMember

class Student(SchoolMember):

    def __init__(self, name, sex, age, *hobby):
        super().__init__(name, sex, age)
        self.hobbies = hobby

    def signUp(self, grade):
        pass
