# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

class SchoolObject(object):

    def __init__(self, school):
        self.school = school
        self.fields = []
        self.fields.append("sID")
        self.sID = ""                  # 编码在子类中赋值
        self.fields.append("name")
        self.name = input("Input {title}'s name(x to cancel):".format(title=self.title))
        if self.name.upper() == "X":
            raise Exception("User cancelled operation.")
        self.status = False
