# -*- coding:utf-8 -*-
"""
学生：编码、姓名、性别、出生日期、注册日期

{
    "1":    "注册--register",
    "2":    "登录--login",
    "21":       "选择学校--selectSchool",
    "211":          "查看可报名课程--showSubject",
    "213":          "查看我的班级--showGrade",
    "22":       "修改密码--password",
    "20"        "退出登录--logout",
    "0":    "退出--exit"
}
"""
__author__ = "Cliff.wang"

from school import School
from schoolMember import SchoolMember

class Student(SchoolMember):

    menu = {
        "1": "注册-reg",
        "2": "报名-signUp",
        "3": "查看课程-printSubjects",
        "4": "查看我的班级-printGrades",
        "5": "查看我的成绩-printCard",
        "6": "查看我的资料-printSelf",
        "7": "修改密码-password",
        "0": "退出登录-",
    }

    def __init__(self, school):
        self.title = "student"
        super().__init__(school)
        self.enrollDate = input("Input enroll date(x to cancel):")
        if self.enrollDate.upper() == "X":
            raise Exception("User cancelled operation.")
        num = 0
        for item in self.school.students:
            if int(item.schoolID[-3:]) > num:
                num = int(item.schoolID[-3:])
        num += 1
        self.schoolID = "3" + ("00" + str(num))[-3:]
        self.status = True
        self.mems = self.school.students
        self.school.students.append(self)

    def add(self):
        mem = Student(self.school)
        School.dataDump(self.school)
        print("{title} {name} is added success.".format(title=self.title.capitalize(), name=mem.name))
