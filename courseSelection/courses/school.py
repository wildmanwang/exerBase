# -*- coding:utf-8 -*-
"""
学校

"""
__author__ = "Cliff.wang"

import pickle
import os

from courses.manager import Manager


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
        self.bModified = False          #是否被修改，修改后要保存
        self.bLogin = False             #是否已登录 True：已登录 False：未登录
        self.iLoginType = 0              #登录类型 0：未登录 1：管理员 2：老师 3：学生
        self.sloginID = ""               #登录账号

    @classmethod
    def dataDump(cls, obj):
        f = open("data\\{name}.dat".format(name=obj.name), "wb")
        pickle.dump(obj, f)
        f.close()
        obj.bModified = False

    @classmethod
    def dataLoad(cls, name):
        f = open("data\\{name}.dat".format(name=name), "rb")
        newObject = pickle.load(f)
        f.close()
        print(newObject.name, newObject.addr)
        return newObject

    def login(self):
        print("Login info".center(30, "-"))
        sID = input("Input your sID:")
        password = input("Input your password:")
        if sID[:1] == "1":
            members = self.managers
        elif sID[:1] == "2":
            members = self.teachers
        elif sID[:1] == "3":
            members = self.students
        else:
            raise Exception("Invalid school ID.")
        bSuccess = False
        for item in members:
            if item.sID == sID and item.pwd == password:
                bSuccess = True
                break
        if bSuccess:
            self.bLogin = True
            self.iLoginType = int(sID[:1])
            self.sloginID = sID
            if self.iLoginType == 1:
                print("Welcome to courses selection system for Managers")
            elif self.iLoginType == 2:
                print("Welcome to courses selection system for Teachers")
            elif self.iLoginType == 3:
                print("Welcome to courses selection system for Students")
            else:
                raise Exception("Login type invalid.")
        else:
            raise Exception("School ID eror or password error.")
        return item

    def logout(self):
        sInput = input("Are you sure exit?yes/no")
        if sInput.upper() == "YES":
            print("{name} logged out.".format(name=self.sloginID.capitalize()))
            self.bLogin = False
            self.iLoginType = 0
            self.sloginID = ""
        else:
            print("Log out is cancel.")

    @classmethod
    def schoolAdd(cls):
        try:
            school = School()
        except Exception as e:
            print(str(e))
        else:
            Manager(school)
            School.dataDump(school)

if __name__ == "__main__":
    if 1 == 1:
        School.schoolAdd()
