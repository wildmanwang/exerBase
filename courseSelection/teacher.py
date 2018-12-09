# -*- coding:utf-8 -*-
"""
老师

查看我的班级
查看班级全部学生
录入学生成绩
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
