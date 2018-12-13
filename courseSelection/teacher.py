# -*- coding:utf-8 -*-
"""
老师
"""
__author__ = "Cliff.wang"

from schoolMember import SchoolMember

class Teacher(SchoolMember):

    def __init__(self, school):
        super().__init__(school)
        self.menu = {
            "1": "登录学校",
            "11": "选择我的班级",
            "111": "查看学生列表",
            "112": "录入学生成绩",
            "113": "查看学生详情",
            "114": "退出班级管理",
            "115": "查看我的资料",
            "116": "辞职",
            "117": "修改密码",
            "110": "退出班级",
            "10": "退出登录",
            "0": "退出"
        }
        bCancel = False
        if not bCancel:
            self.salary = input("Input salary(x to cancel):")
            if self.name.upper() == "X":
                bCancel = True
        self.grades = []
        self.schoolID = ""
        self.status = True

    def showAll(self, grade):
        pass

    def inputScore(self, grade, student, chapter, score):
        pass

if __name__ == "__main__":
    t1 = Teacher("Jack", '1', 28, 20000.00)
    print(t1.name, t1.salary)
