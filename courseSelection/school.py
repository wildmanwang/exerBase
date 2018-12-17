# -*- coding:utf-8 -*-
"""
学校

"""
__author__ = "Cliff.wang"

import pickle
import os

from manager import Manager
from teacher import Teacher
from student import Student

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
        self.bLogin = False              #是否已登录 True：已登录 False：未登录
        self.iLoginType = 0              #登录类型 0：未登录 1：管理员 2：老师 3：学生
        self.sloginID = ""               #登录账号

    def printList(self, title):
        if title == "manager":
            mems = self.managers
        elif title == "teacher":
            mems = self.teachers
        else:
            mems = self.students
        sOutput = "{school}'s {title} list:\n".format(school=self.name, title=title)
        for item in mems:
            sOutput += "ID:{id}\tName:{name}\tSex:{sex}\tBirthdate:{birthDate}\n".format(
                id=item.schoolID,
                name=item.name,
                sex=item.sex,
                birthDate=item.birthDate
            )
        print(sOutput)

    def add(self, title):
        if title == "manager":
            mem = Manager(self)
        elif title == "teacher":
            mem = Teacher(self)
        elif title == "student":
            mem = Student(self)
        else:
            raise Exception("Invalid object type.")
        School.dataDump(self)
        print("{title} {name} is added success.".format(title=title.capitalize(), name=mem.name))

    def modify(self, title):
        if title == "manager":
            mems = self.managers
        elif title == "teacher":
            mems = self.teachers
        else:
            mems = self.students
        bFind = False
        sInput = input("Input the ID of {title} you wanto modify:".format(title=title))
        for item in mems:
            if item.schoolID == sInput:
                mem = item
                bFind = True
        if not bFind:
            raise Exception("{title}'s ID is invalid.".format(title=title.capitalize()))
        mem.name = input("Input {title}'s name(x to cancel):".format(title=title))
        if mem.name.upper() == "X":
            raise Exception("User cancelled operation.")
        mem.sex = input("Input {title}'s sex(x to cancel):".format(title=title))
        if mem.sex.upper() == "X":
            raise Exception("User cancelled operation.")
        mem.birthDate = input("Input {title}'s birthDate(x to cancel):".format(title=title))
        if mem.birthDate.upper() == "X":
            raise Exception("User cancelled operation.")
        School.dataDump(self)
        print("{title} {name} is saved success.".format(title=title.capitalize(), name=mem.name))

    def delete(self, title):
        if title == "manager":
            mems = self.managers
        elif title == "teacher":
            mems = self.teachers
        else:
            mems = self.students
        bFind = False
        sInput = input("Input the {title}'s ID you wanto delete:".format(title=title))
        for item in mems:
            if item.schoolID == sInput:
                mem = item
                bFind = True
        if not bFind:
            raise Exception("{title}'s ID is invalid.".format(title=title.capitalize()))
        if sInput == mem.schoolID:
            raise Exception("You can't delete yourself.")
        sInput = input("Are you sure to delete {title} {name}({ID})?yes/no".format(title=title, name=mem.name, ID=mem.schoolID))
        if sInput.upper() != "YES":
            raise Exception("User cancelled operation.")
        mems.remove(mem)
        School.dataDump(self)
        print("{title} {name} is deleted success.".format(title=title.capitalize(), name=mem.name))

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
        print("Login info".center(30, "-"))
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
        bSuccess = False
        for item in members:
            if item.schoolID == schoolID and item.pwd == password:
                bSuccess = True
                break
        if bSuccess:
            self.bLogin = True
            self.iLoginType = int(schoolID[:1])
            self.sloginID = schoolID
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

if __name__ == "__main__":
    pass
