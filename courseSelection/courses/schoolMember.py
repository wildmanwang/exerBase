# -*- coding:utf-8 -*-
"""
学校成员

打印菜单
保存数据
读取数据
"""
__author__ = "Cliff.wang"

from courses.schoolObject import SchoolObject

class SchoolMember(SchoolObject):

    menu = {
        "0": "退出"
    }

    def __init__(self, school):

        super().__init__(school)

        self.fields.append("pwd")
        self.pwd = input("Input {title}'s password(x to cancel):".format(title=self.title))
        if self.pwd.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("sex")
        self.sex = input("Input {title}'s sex(x to cancel):".format(title=self.title))
        if self.sex.upper() == "X":
            raise Exception("User cancelled operation.")
        self.fields.append("birthDate")
        self.birthDate = input("Input {title}'s birthDate(x to cancel):".format(title=self.title))
        if self.birthDate.upper() == "X":
            raise Exception("User cancelled operation.")

    def printMenu(self, menuSuper):
        strPrt = "Choose a option:\n"
        level = len(menuSuper) + 1
        for key, item in self.menu.items():
            if len(key) == level and key[:level - 1] == menuSuper:
                strPrt += "\t{num}\t{menu}\n".format(num=key[-1:], menu=item.split("-")[0])
        print(strPrt)

    def hasChildren(self, flag):
        bChildren = False
        iLen = len(flag)
        for key in self.menu.keys():
            if key[:len(flag)] == flag and len(key) > iLen:
                bChildren = True
                break
        return bChildren

    def printSelf(self):
        sOutput = "{title} {name}'s info".format(title=self.title.capitalize(), name=self.name).center(40, "=") + "\n"
        for col in self.fields:
            if col.upper() == "PWD" or col.upper() == "PASSWORD":
                continue
            sOutput += "{col}{space}:{value}\n".format(col=col.capitalize().rjust(15, " "), space=" " * 5, value=getattr(self, col).ljust(20, " "))
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
        if self.sID[:1] == "1":
            mems = self.school.managers
        elif self.sID[:1] == "2":
            mems = self.school.teachers
        else:
            mems = self.school.students
        for item in mems:
            if item.sID == self.sID:
                item.pwd = sPwNew
                self.school.bModified = True
                print("Your password is modified.")
                break

if __name__ == "__main__":
    pass
