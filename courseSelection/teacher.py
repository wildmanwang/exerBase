# -*- coding:utf-8 -*-
"""
老师
"""
__author__ = "Cliff.wang"

from schoolMember import SchoolMember

class Teacher(SchoolMember):

    menu = {
        "1": "选择我的班级-",
        "11": "查看学生列表-printList",
        "12": "录入学生成绩-modify",
        "13": "查看学生详情-printStudent",
        "10": "退出班级管理-",
        "2": "辞职-",
        "3": "查看我的资料-printSelf",
        "4": "修改密码-password",
        "0": "退出登录-",
    }

    def __init__(self, school):
        self.title = "teacher"
        super().__init__(school)
        bCancel = False
        if not bCancel:
            self.salary = input("Input salary(x to cancel):")
            if self.name.upper() == "X":
                bCancel = True
        self.grades = []
        num = 0
        for item in self.school.teachers:
            if int(item.schoolID[-3:]) > num:
                num = int(item.schoolID[-3:])
        num += 1
        self.schoolID = "2" + ("00" + str(num))[-3:]
        self.status = True

    def showAll(self, grade):
        pass

    def inputScore(self, grade, student, chapter, score):
        pass

if __name__ == "__main__":
    print("123456-abc".split("-")[1])
