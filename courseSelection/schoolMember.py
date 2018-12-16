# -*- coding:utf-8 -*-
"""
学校成员

打印菜单
保存数据
读取数据
"""
__author__ = "Cliff.wang"

class SchoolMember(object):

    menu = {
        "1": "登录",
        "0": "退出"
    }

    def __init__(self, school):
        self.school = school
        bCancel = False
        if not bCancel:
            self.name = input("Input {title}'s name(x to cancel):".format(title=self.title))
            if self.name.upper() == "X":
                bCancel = True
        if not bCancel:
            self.pwd = input("Input {title}'s password(x to cancel):".format(title=self.title))
            if self.pwd.upper() == "X":
                bCancel = True
        if not bCancel:
            self.sex = input("Input {title}'s sex(x to cancel):".format(title=self.title))
            if self.sex.upper() == "X":
                bCancel = True
        if not bCancel:
            self.birthDate = input("Input {title}'s birthDate(x to cancel):".format(title=self.title))
            if self.birthDate.upper() == "X":
                bCancel = True
        self.schoolID = ""          #编码在子类中赋值。没有编码的对象创建不成功
        self.status = False

    def printMenu(self, menuSuper):
        strPrt = "Choose a option:\n"
        level = len(menuSuper) + 1
        for key, item in self.menu.items():
            if len(key) == level and key[:level - 1] == menuSuper:
                strPrt += "\t{num}\t{menu}\n".format(num=key[-1:], menu=item.split("-")[0])
        print(strPrt)

if __name__ == "__main__":
    import time, datetime
