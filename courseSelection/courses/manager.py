#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
学校管理员
"""

__author__ = 'Cliff Wang'

from courses.schoolMember import SchoolMember

class Manager(SchoolMember):

    menu = {
        "1": "管理员管理-manager",
        "11": "查看管理员列表-printList",
        "12": "新增管理员-add",
        "13": "修改管理员-modify",
        "14": "删除管理员-delete",
        "10": "退出管理员管理-",
        "2": "课程管理-subject",
        "21": "查看课程列表-printList",
        "22": "新增课程-add",
        "23": "修改课程-modify",
        "24": "删除课程-delete",
        "20": "退出课程管理-",
        "3": "老师管理-teacher",
        "31": "查看老师列表-printList",
        "32": "招聘老师-add",
        "33": "修改管理员-modify",
        "34": "删除老师-delete",
        "30": "退出老师管理-",
        "4": "班级管理-grade",
        "41": "查看班级列表-printList",
        "42": "新增班级-add",
        "43": "修改班级-modify",
        "44": "删除班级-delete",
        "45": "指定课程-setSubject",
        "46": "指定老师-setTeacher",
        "47": "开课-start",
        "40": "退出班级管理-",
        "5": "学生管理-student",
        "51": "查看学生列表-printList",
        "54": "开除学生-delete",
        "50": "退出学生管理-",
        "6": "查看我的资料-printSelf",
        "7": "修改密码-password",
        "0": "退出登录-",
    }

    def __init__(self, school):
        self.title = "manager"
        super().__init__(school)
        num = 0
        for item in self.school.managers:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.sID = "1" + ("00" + str(num))[-3:]
        self.status = True
        self.school.managers.append(self)

    def printList(self):
        if title == "manager":
            mems = self.school.managers
        elif title == "teacher":
            mems = self.school.teachers
        elif title == "student":
            mems = self.school.students
        elif title == "subject":
            mems = self.school.subjects
        elif title == "grade":
            mems = self.school.grades
        else:
            raise Exception("Invalid object type.")
        sOutput = "{school}'s {title} list:\n".format(school=self.school.name, title=self.title) + "\n".rjust(40, "=")
        for item in mems:
            for col in item.fields:
                if col.upper() in ("PASSWORD"):
                    continue
                sOutput += "{title}:{value}\t".format(title=col.capitalize(), value=getattr(item, col))
            sOutput += "\n"
        sOutput += "\n".rjust(40, "=")
        print(sOutput)

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
        print("{title} {name} is added success.".format(title=title.capitalize(), name=mem.name))

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
        bFind = False
        sInput = input("Input the ID of {title} you wanto modify:".format(title=title))
        for item in mems:
            if item.sID == sInput:
                mem = item
                bFind = True
        if not bFind:
            raise Exception("{title}'s ID is invalid.".format(title=title.capitalize()))
        for col in mem.fields:
            if col.upper() in ("SID", "PASSWORD", "SUBJECT", "TEACHER", "STATUS"):
                continue
            sTmp = input("Input {title}'s {col}(x to cancel):".format(title=title, col=col))
            if sTmp.upper() == "X":
                raise Exception("User cancelled operation.")
            setattr(mem, col, sTmp)
        self.bModified = True
        print("{title} {name} is saved success.".format(title=title.capitalize(), name=mem.name))

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
        bFind = False
        sInput = input("Input the {title}'s ID you wanto delete:".format(title=title))
        for item in mems:
            if item.sID == sInput:
                mem = item
                bFind = True
        if not bFind:
            raise Exception("{title}'s ID is invalid.".format(title=title.capitalize()))
        if sInput == self.sloginID:
            raise Exception("You can't delete yourself.")
        sInput = input("Are you sure to delete {title} {name}({ID})?yes/no".format(title=title, name=mem.name, ID=mem.sID))
        if sInput.upper() != "YES":
            raise Exception("User cancelled operation.")
        mems.remove(mem)
        self.bModified = True
        print("{title} {name} is deleted success.".format(title=title.capitalize(), name=mem.name))

    def setSubject(self):
        # 选择班级
        if len(self.grades) == 0:
            raise Exception("Please create grades first.")
        sOutPut = "Select a grade:\n"
        for item in self.grades:
            sOutPut += "{code}\t{name}.\n".format(code=item.sID, name=item.name)
        sInput = input(sOutPut)
        bFind = False
        for item in self.grades:
            if item.sID == sInput:
                grade = item
                bFind = True
                break
        if not bFind:
            raise Exception("Input invalid.")
        # 选择课程
        if len(self.subjects) == 0:
            raise Exception("Please create subjects first.")
        sOutPut = "Select a subject:\n"
        for item in self.subjects:
            sOutPut += "{code}\t{name}.\n".format(code=item.sID, name=item.name)
        sInput = input(sOutPut)
        bFind = False
        for item in self.subjects:
            if item.sID == sInput:
                subject = "[{code}]{name}".format(code=item.sID, name=item.name)
                bFind = True
                break
        if not bFind:
            raise Exception("Input invalid.")
        # 设置课程
        grade.subject = subject
        # 保存
        self.bModified = True
        print("Grade[{grade}] is setted subject[{subject}] success.".format(grade=grade.name, subject=item.name))

    def setTeacher(self):
        # 选择班级
        if len(self.grades) == 0:
            raise Exception("Please create grade first.")
        sOutPut = "Select a grade:\n"
        for item in self.grades:
            sOutPut += "{code}\t{name}.\n".format(code=item.sID, name=item.name)
        sInput = input(sOutPut)
        bFind = False
        for item in self.grades:
            if item.sID == sInput:
                grade = item
                bFind = True
                break
        if not bFind:
            raise Exception("Input invalid.")
        # 选择老师
        if len(self.teachers) == 0:
            raise Exception("Please hire teachers first.")
        sOutPut = "Select a teacher:\n"
        for item in self.teachers:
            sOutPut += "{code}\t{name}.\n".format(code=item.sID, name=item.name)
        sInput = input(sOutPut)
        bFind = False
        for item in self.teachers:
            if item.sID == sInput:
                teacher = "[{code}]{name}".format(code=item.sID, name=item.name)
                bFind = True
                break
        if not bFind:
            raise Exception("Input invalid.")
        # 设置课程
        grade.teacher = teacher
        # 保存
        self.bModified = True
        print("Grade[{grade}] is setted teacher[{teacher}] success.".format(grade=grade.name, teacher=item.name))

    def start(self):
        # 选择班级
        if len(self.grades) == 0:
            raise Exception("Please create grade first.")
        sOutPut = "Select a grade:\n"
        for item in self.grades:
            sOutPut += "{code}\t{name}.\n".format(code=item.sID, name=item.name)
        sInput = input(sOutPut)
        bFind = False
        for item in self.grades:
            if item.sID == sInput:
                grade = item
                bFind = True
                break
        if not bFind:
            raise Exception("Input invalid.")
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

if __name__ == "__main__":
    pass
