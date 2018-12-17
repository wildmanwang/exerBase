# -*- coding:utf-8 -*-
"""
学校成员

打印菜单
保存数据
读取数据
"""
__author__ = "Cliff.wang"

from school import School

class SchoolMember(object):

    menu = {
        "1": "登录",
        "0": "退出"
    }

    def __init__(self, school):
        self.school = school
        self.name = input("Input {title}'s name(x to cancel):".format(title=self.title))
        if self.name.upper() == "X":
            raise Exception("User cancelled operation.")
        self.pwd = input("Input {title}'s password(x to cancel):".format(title=self.title))
        if self.pwd.upper() == "X":
            raise Exception("User cancelled operation.")
        self.sex = input("Input {title}'s sex(x to cancel):".format(title=self.title))
        if self.sex.upper() == "X":
            raise Exception("User cancelled operation.")
        self.birthDate = input("Input {title}'s birthDate(x to cancel):".format(title=self.title))
        if self.birthDate.upper() == "X":
            raise Exception("User cancelled operation.")
        self.schoolID = ""          #编码在子类中赋值。没有编码的对象创建不成功
        self.status = False

    def printMenu(self, menuSuper):
        strPrt = "Choose a option:\n"
        level = len(menuSuper) + 1
        for key, item in self.menu.items():
            if len(key) == level and key[:level - 1] == menuSuper:
                strPrt += "\t{num}\t{menu}\n".format(num=key[-1:], menu=item.split("-")[0])
        print(strPrt)

    def printSelf(self):
        sOutput = "{title} {name}'s info".format(title=self.title.capitalize(), name=self.name).center(40, "=") + "\n"
        sOutput += "ID:".rjust(15, " ") + " " * 5 + self.schoolID.ljust(20, " ") + "\n"
        sOutput += "Name:".rjust(15, " ") + " " * 5 + self.name.ljust(20, " ") + "\n"
        sOutput += "Sex:".rjust(15, " ") + " " * 5 + self.sex.ljust(20, " ") + "\n"
        sOutput += "Birthdate:".rjust(15, " ") + " " * 5 + self.birthDate.ljust(20, " ") + "\n"
        sOutput += "end info".center(40, "=")
        print(sOutput)

    def password(self):
        sPwOld = input("Input old password:")
        if sPwOld != self.pwd:
            raise Exception("Invalid password.")
        sPwNew = input("Input new password:")
        sPwAgain = input("Input new password again:")
        if sPwNew != sPwAgain:
            raise Exception("Two inputs are different.")
        self.pwd = sPwNew
        if self.schoolID[:1] == "1":
            mems = self.school.managers
        elif self.schoolID[:1] == "2":
            mems = self.school.teachers
        else:
            mems = self.school.students
        for item in mems:
            if item.schoolID == self.schoolID:
                item.pwd = sPwNew
                School.dataDump(self.school)
                print("Your password is modified.")
                break

if __name__ == "__main__":
    import time, datetime
