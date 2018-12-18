# -*- coding:utf-8 -*-
"""
老师
"""
__author__ = "Cliff.wang"

from schoolMember import SchoolMember

class Teacher(SchoolMember):

    menu = {
        "1": "选择我的班级-chooseGrade",
        "2": "查看学生列表-printList",
        "3": "录入学生成绩-modify",
        "4": "查看学生详情-printStudent",
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

if __name__ == "__main__":
    l1 = ['a', 'b', 'c']
    l2 = ['d', 'e']
    l3 = l1 + l2
    print(l3)
