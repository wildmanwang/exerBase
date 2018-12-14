# -*- coding:utf-8 -*-
"""
学校

"""
__author__ = "Cliff.wang"

import pickle
import os

class School(object):

    def __init__(self):
        bCancel = False
        if not bCancel:             #名称
            self.name = input("Input school's name(x to cancel):")
            if self.name.upper() == "X":
                bCancel = True
        if os.path.exists("data\\{name}.dat".format(name=self.name)):
            raise Exception("School [{name}] exists already.".format(name=self.name))
        bCancel = False
        if not bCancel:             #地址
            self.addr = input("Input school's addr(x to cancel):")
            if self.addr.upper() == "X":
                bCancel = True
        bCancel = False
        if not bCancel:             #电话
            self.phone = input("Input school's phone(x to cancel):")
            if self.phone.upper() == "X":
                bCancel = True
        self.managers = []          #管理员列表， 编码格式：1###
        self.subjects = []          #课程列表，编码格式：S###
        self.grades = []            #班级列表，编码格式：G###
        self.teachers = []          #老师列表，编码格式：2###
        self.students = []          #学生列表，编码格式：3###
        bLogin = False              #是否已登录 True：已登录 False：未登录
        iLoginType = 0              #登录类型 0：未登录 1：管理员 2：老师 3：学生
        sloginID = ""               #登录账号

    @classmethod
    def dataDump(cls, obj):
        f = open("data\\{name}.dat".format(name=obj.name), "wb")
        pickle.dump(obj, f)
        f.close()

    @classmethod
    def dataLoad(cls, name):
        f = open("data\\{name}.dat".format(name=name), "rb")
        newObject = pickle.load(f)
        f.close()
        print(newObject.name, newObject.addr)
        return newObject

    def login(self):
        schoolID = input("Input your schoolID:")
        password = input("Input your password:")
        if schoolID[:1] == "1":
            members = self.managers
        elif schoolID[:1] == "2":
            members = self.teachers
        elif schoolID[:1] == "3":
            members = self.students
        else:
            raise Exception("Invalid school ID.")

    def logout(self):
        pass

    def showManagers(self):
        pass

    def showSubjects(self):
        pass

    def showGrades(self):
        pass

    def showTeachers(self):
        pass

    def showStudents(self):
        pass

if __name__ == "__main__":
    pass
