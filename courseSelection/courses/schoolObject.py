# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

class SchoolObject(object):

    def __init__(self, school):
        self.school = school
        self.title = "schoolObject" # 子类中替换
        self.fields = []
        self.fields.append("sID")
        self.sID = ""                  # 编码在子类中赋值
        self.fields.append("name")
        self.name = input("Input {title}'s name(x to cancel):".format(title=self.title))
        if self.name.upper() == "X":
            raise Exception("User cancelled operation.")
        self.status = False

    def printList(self):
        if self.title == "manager":
            mems = self.school.managers
        elif self.title == "teacher":
            mems = self.school.teachers
        elif self.title == "student":
            mems = self.school.students
        elif self.title == "subject":
            mems = self.school.subjects
        elif self.title == "grade":
            mems = self.school.grades
        else:
            raise Exception("Invalid object type.")
        sOutput = "{school}'s {title} list:\n".format(school=self.school.name, title=self.title) + "\n".rjust(40, "=")
        for item in mems:
            for col in item.fields:
                if col.upper() not in ("PASSWORD"):
                    sOutput += "{title}:{value}\t".format(title=col.capitalize(), value=getattr(item, col))
            sOutput += "\n"
        sOutput += "\n".rjust(40, "=")
        print(sOutput)

    def modify(self):
        if self.title == "manager":
            mems = self.school.managers
        elif self.title == "teacher":
            mems = self.school.teachers
        elif self.title == "student":
            mems = self.school.students
        elif self.title == "subject":
            mems = self.school.subjects
        elif self.title == "grade":
            mems = self.school.grades
        else:
            raise Exception("Invalid object type.")
        bFind = False
        sInput = input("Input the ID of {title} you wanto modify:".format(title=self.title))
        for item in mems:
            if item.sID == sInput:
                mem = item
                bFind = True
        if not bFind:
            raise Exception("{title}'s ID is invalid.".format(title=self.title.capitalize()))
        for col in mem.fields:
            if col.upper() in ("SID", "PASSWORD", "SUBJECT", "TEACHER", "STATUS"):
                continue
            sTmp = input("Input {title}'s {col}(x to cancel):".format(title=self.title, col=col))
            if sTmp.upper() == "X":
                raise Exception("User cancelled operation.")
            setattr(mem, col, sTmp)
        self.bModified = True
        print("{title} {name} is saved success.".format(title=self.title.capitalize(), name=mem.name))

    def delete(self):
        if self.title == "manager":
            mems = self.school.managers
        elif self.title == "teacher":
            mems = self.school.teachers
        elif self.title == "student":
            mems = self.school.students
        elif self.title == "subject":
            mems = self.school.subjects
        elif self.title == "grade":
            mems = self.school.grades
        else:
            raise Exception("Invalid object type.")
        bFind = False
        sInput = input("Input the {title}'s ID you wanto delete:".format(title=self.title))
        for item in mems:
            if item.sID == sInput:
                mem = item
                bFind = True
        if not bFind:
            raise Exception("{title}'s ID is invalid.".format(title=self.title.capitalize()))
        if sInput == self.school.sloginID:
            raise Exception("You can't delete yourself.")
        sInput = input("Are you sure to delete {title} {name}({ID})?yes/no".format(title=self.title, name=mem.name, ID=mem.sID))
        if sInput.upper() != "YES":
            raise Exception("User cancelled operation.")
        mems.remove(mem)
        self.bModified = True
        print("{title} {name} is deleted success.".format(title=self.title.capitalize(), name=mem.name))
