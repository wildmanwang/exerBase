# -*- coding:utf-8 -*-
"""
学校成员

打印菜单
保存数据
读取数据
"""
__author__ = "Cliff.wang"

import pickle

class SchoolMember(object):

    def __init__(self, school):
        self.menu = {
            "1":"登录",
            "0":"退出"
        }

        bCancel = False
        if not bCancel:
            self.name = input("Input name(x to cancel):")
            if self.name.upper() == "X":
                bCancel = True
        if not bCancel:
            self.pwd = input("Input password(x to cancel):")
            if self.pwd.upper() == "X":
                bCancel = True
        if not bCancel:
            self.sex = input("Input sex(x to cancel):")
            if self.sex.upper() == "X":
                bCancel = True
        if not bCancel:
            self.birthDate = input("Input birthDate(x to cancel):")
            if self.birthDate.upper() == "X":
                bCancel = True
        self.schoolID = ""          #编码在子类中赋值。没有编码的对象创建不成功
        self.status = False

    def login(self):
        pass

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

    def dataDump(self, objType, name, obj):
        f = open("data\\{objType}\\{name}.dat".format(objType=objType, name=name), "wb")
        pickle.dump(obj, f)
        f.close()

    def dataLoad(self, objType, name):
        f = open("data\\{objType}\\{name}.dat".format(objType=objType, name=name), "rb")
        newObject = pickle.load(f)
        f.close()

        return newObject

    def logout(self):
        pass

if __name__ == "__main__":
    import time, datetime
