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

from schoolMember import SchoolMember

class Student(SchoolMember):

    def __init__(self, name, sex, age, *hobby):
        super().__init__(name, sex, age)
        self.hobbies = hobby

    def signUp(self, grade):
        pass
