# -*- coding:utf-8 -*-
"""
学生：编码、姓名、性别、出生日期、注册日期
"""
__author__ = "Cliff.wang"

from datetime import date
from courses.schoolMember import SchoolMember

class Student(SchoolMember):

    menu = {
        "1": "报名-signUp",
        "2": "查看课程-printSubjects",
        "3": "查看班级-printGrades",
        "4": "查看我的资料-printSelf",
        "5": "修改密码-password",
        "0": "退出登录-",
    }

    def __init__(self, school):
        self.title = "student"
        super().__init__(school)
        num = 0
        for item in self.school.students:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.sID = "3" + ("00" + str(num))[-3:]
        self.fields.append("enrollDate")
        self.enrollDate = date.today()
        self.fields.append("score")
        self.score = -1
        self.status = True
        self.school.students.append(self)

    def signUp(self):
        subs = [item for item in self.school.grades if item.status]
        grade = self.school.chooseObject("grade", subs)
        grade.students.append(self)
        self.school.bModified = True
        print("You sign up the grade:{name} success.".format(name=grade.name))

    def printSubjects(self):
        subs = [item for item in self.school.subjects if item.status]
        self.school.printObjects("subject", subs)

    def printGrades(self):
        subs = [item for item in self.school.grades if item.status]
        self.school.printObjects("grade", subs)


if __name__ == "__main__":
    print("".center(40, "="))
