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

    menu = {
        "1": "选择学校",
        "11": "注册",
        "12": "登录",
        "121": "查看课程",
        "122": "查看我的班级",
        "123": "查看我的详情",
        "13": "修改密码",
        "10": "退出登录",
        "0": "退出"
    }

    def __init__(self, school):
        super().__init__(school)
        self.schoolID = ""
        self.status = True
