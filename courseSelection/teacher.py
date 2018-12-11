# -*- coding:utf-8 -*-
"""
老师

老师界面
    登录
        选择学校
            选择我的班级
                查看学生列表
                录入学生成绩
                查看学生详情
                退出班级管理
            退出学校
        查看我的信息
        辞职
        修改密码
        退出登录
    退出
"""
__author__ = "Cliff.wang"

from schoolMember import SchoolMember

class Teacher(SchoolMember):

    def __init__(self, name, sex, age, salary, *subjects):
        super().__init__(name, sex, age)
        self.salary = salary
        self.subjects = subjects
        self.grades = []

    def showAll(self, grade):
        pass

    def inputScore(self, grade, student, chapter, score):
        pass

if __name__ == "__main__":
    t1 = Teacher("Jack", '1', 28, 20000.00)
    print(t1.name, t1.salary)
