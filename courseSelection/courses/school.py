# -*- coding:utf-8 -*-
"""
学校

"""
__author__ = "Cliff.wang"

import pickle
import os

from courses.manager import Manager
from courses.teacher import Teacher
from courses.student import Student
from courses.subject import Subject
from courses.grade import Grade

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
    def dataDump(cls, sPathData, obj):
        sFile = os.path.join(sPathData, "{name}.dat".format(name=obj.name))
        f = open(sFile, "wb")
        pickle.dump(obj, f)
        f.close()
        obj.bModified = False

    @classmethod
    def dataLoad(cls, sPathData, name):
        sFile = os.path.join(sPathData, "{name}.dat".format(name=name))
        f = open(sFile, "rb")
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

    def chooseObject(self, title, objs):
        if len(objs) == 0:
            raise Exception("No any {title} exists.".format(title=title))
        sOutPut = "Select a {title}:\n".format(title=title)
        for item in objs:
            sOutPut += "{code}\t{name}.\n".format(code=item.sID, name=item.name)
        sInput = input(sOutPut)
        bFind = False
        for item in objs:
            if item.sID == sInput:
                obj = item
                bFind = True
                break
        if not bFind:
            raise Exception("Input invalid.")
        return obj

    def printObjects(self, title, objs):
        sOutput = "{school}'s {title}s list:\n".format(school=self.name, title=title) + "\n".rjust(40, "=")
        for item in objs:
            for col in item.fields:
                if col.upper() not in ("PASSWORD"):
                    sOutput += "{title}:{value}\t".format(title=col.capitalize(), value=getattr(item, col))
            sOutput += "\n"
        sOutput += "\n".rjust(40, "=")
        print(sOutput)

    def modifyObject(self, title, obj):
        for col in obj.fields:
            if col.upper() in ("SID", "PASSWORD", "SUBJECT", "TEACHER", "STATUS"):
                continue
            sTmp = input("Input {title}'s {col}(x to cancel):".format(title=title, col=col))
            if sTmp.upper() == "X":
                raise Exception("User cancelled operation.")
            setattr(obj, col, sTmp)
        self.bModified = True
        print("{title} {name} is saved success.".format(title=title.capitalize(), name=obj.name))

    def printList(self, title):
        if title == "manager":
            mems = self.managers
        elif title == "teacher":
            mems = self.teachers
        elif title == "student":
            mems = self.students
        elif title == "subject":
            mems = self.subjects
        elif title == "grade":
            mems = self.grades
        else:
            raise Exception("Invalid object type.")
        self.printObjects(title, mems)

    def add(self, title):
        if title == "manager":
            mem = Manager(self)
        elif title == "teacher":
            mem = Teacher(self)
        elif title == "student":
            mem = Student(self)
        elif title == "subject":
            mem = Subject(self)
        elif title == "grade":
            mem = Grade(self)
        else:
            raise Exception("Invalid object type.")
        self.bModified = True
        print("{title} {name} is added success,sID=[{ID}].".format(title=title.capitalize(), ID=mem.sID, name=mem.name))

    def modify(self, title):
        if title == "manager":
            mems = self.managers
        elif title == "teacher":
            mems = self.teachers
        elif title == "student":
            mems = self.students
        elif title == "subject":
            mems = self.subjects
        elif title == "grade":
            mems = self.grades
        else:
            raise Exception("Invalid object type.")
        if len(mems) == 0:
            raise Exception("No any {title}.".format(title=title))
        mem = self.chooseObject(title, mems)
        self.modifyObject(title, mem)

    def delete(self, title):
        if title == "manager":
            mems = self.managers
        elif title == "teacher":
            mems = self.teachers
        elif title == "student":
            mems = self.students
        elif title == "subject":
            mems = self.subjects
        elif title == "grade":
            mems = self.grades
        else:
            raise Exception("Invalid object type.")
        mem = self.chooseObject(title, mems)
        if mem.sID == self.sloginID:
            raise Exception("You can't delete yourself.")
        sInput = input("Are you sure to delete {title} [{ID}]?yes/no".format(title=title, name=mem.name, ID=mem.sID))
        if sInput.upper() != "YES":
            raise Exception("User cancelled operation.")
        mems.remove(mem)
        self.bModified = True
        print("{title} {name} is deleted success.".format(title=title.capitalize(), name=mem.name))

    def gradeSetSubject(self):
        # 选择班级
        grade = self.chooseObject("grade", self.grades)
        # 选择课程
        subject = self.chooseObject("subject", self.subjects)
        sDisplay = "[{code}]{name}".format(code=subject.sID, name=subject.name)
        # 设置课程
        grade.subject = sDisplay
        # 保存
        self.bModified = True
        print("Grade[{grade}] is setted {subject} success.".format(grade=grade.name, subject=sDisplay))

    def gradeSetTeacher(self):
        # 选择班级
        grade = self.chooseObject("grade", self.grades)
        # 选择老师
        teacher = self.chooseObject("teacher", self.teachers)
        sDisplay = "[{code}]{name}".format(code=teacher.sID, name=teacher.name)
        # 设置课程
        grade.teacher = sDisplay
        # 保存
        self.bModified = True
        print("Grade[{grade}] is setted {teacher} success.".format(grade=grade.name, teacher=sDisplay))

    def gradeStart(self):
        # 选择班级
        grade = self.chooseObject("grade", self.grades)
        # 判断是否指定了课程及老师
        if grade.subject == "<Not yet set up>":
            raise Exception("Please set up subject first.")
        if grade.teacher == "<Not yet set up>":
            raise Exception("Please set up teacher first.")
        # 询问启动
        sInput = input("Are you sure you want to enable this grade[{name}]?yes/no".format(name=grade.name))
        if sInput.upper() != "YES":
            raise Exception("User cancelled operation.")
        # 启动
        grade.status = True
        # 保存
        self.bModified = True
        print("Grade[{grade}] is enabled success.".format(grade=grade.name))

    @classmethod
    def schoolAdd(cls):
        import sys
        sPathRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sPathData = os.path.join(sPathRoot, "data")
        try:
            school = School()
        except Exception as e:
            print(str(e))
        else:
            Manager(school)
            School.dataDump(sPathData, school)

if __name__ == "__main__":
    if 1 == 1:
        School.schoolAdd()
