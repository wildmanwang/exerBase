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

    def __init__(self, school, title):
        self.school = school
        self.title = title
        bCancel = False
        if not bCancel:
            self.name = input("Input {title}'s name(x to cancel):".format(title=title))
            if self.name.upper() == "X":
                bCancel = True
        if not bCancel:
            self.pwd = input("Input {title}'s password(x to cancel):".format(title=title))
            if self.pwd.upper() == "X":
                bCancel = True
        if not bCancel:
            self.sex = input("Input {title}'s sex(x to cancel):".format(title=title))
            if self.sex.upper() == "X":
                bCancel = True
        if not bCancel:
            self.birthDate = input("Input {title}'s birthDate(x to cancel):".format(title=title))
            if self.birthDate.upper() == "X":
                bCancel = True
        self.schoolID = ""          #编码在子类中赋值。没有编码的对象创建不成功
        self.status = False

    def printMenu(self, menuTitle, menuSuper):
        if not menuTitle:
            strPrt = "Choose a option:\n"
        elif menuTitle[-1:] == ":" or menuTitle[-1:] == "：":
            strPrt = menuTitle + "\n"
        else:
            strPrt = menuTitle + ":\n"
        level = len(menuSuper) + 1
        for key, item in self.menu.items():
            if len(key) == level and key[:level - 1] == menuSuper:
                strPrt += "\t{num}\t{menu}\n".format(num=key[-1:], menu=item)
        print(strPrt)

if __name__ == "__main__":
    import time, datetime
