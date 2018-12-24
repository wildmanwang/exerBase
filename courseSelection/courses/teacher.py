# -*- coding:utf-8 -*-
"""
老师
"""
__author__ = "Cliff.wang"

from courses.schoolMember import SchoolMember

class Teacher(SchoolMember):

    menu = {
        "1": "查看我的班级-printGrades",
        "2": "查看学生列表-printStudents",
        "3": "录入学生成绩-modifyCard",
        "4": "查看学生详情-printCard",
        "5": "辞职-resign",
        "6": "查看我的资料-printSelf",
        "7": "修改密码-password",
        "0": "退出登录-",
    }

    def __init__(self, school):
        self.title = "teacher"
        super().__init__(school)
        num = 0
        for item in self.school.teachers:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.sID = "2" + ("00" + str(num))[-3:]
        self.fields.append("salary")
        self.salary = input("Input salary(x to cancel):")
        if self.salary.upper() == "X":
            raise Exception("User cancelled operation.")
        self.grades = []
        self.status = True
        self.school.teachers.append(self)

    def printGrades(self):
        self.school.printObjects("grade", self.grades)

    def printStudents(self):
        grade = self.school.chooseObject("grade", self.grades)
        self.school.printObjects("student", grade.students)

    def modifyCard(self):
        grade = self.school.chooseObject("grade", self.grades)
        student = self.school.chooseObject("student", grade)
        self.school.modifyObject("student", student)

    def printCard(self):
        grade = self.school.chooseObject("grade", self.grades)
        student = self.school.chooseObject("student", grade)
        student.printSelf()

    def resign(self):
        pass

if __name__ == "__main__":
    l1 = ['a', 'b', 'c']
    l2 = ['d', 'e']
    l3 = l1 + l2
    print(l3)