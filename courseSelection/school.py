# -*- coding:utf-8 -*-
"""
学校

"""
__author__ = "Cliff.wang"

class School(object):

    def __init__(self, name, addr, phone):
        self.name = name            #名称
        self.addr = addr            #地址
        self.phone = phone          #电话
        self.managers = []          #管理员列表， 编码格式：1###
        self.subjects = []          #课程列表，编码格式：S###
        self.grades = []            #班级列表，编码格式：G###
        self.teachers = []          #老师列表，编码格式：2###
        self.students = []          #学生列表，编码格式：3###

    def showManagers(self):
        pass

    def showSubjects(self):
        pass

    def showGrades(self):
        pass

    def showTeachers(self):
        pass

    def showStudents(self):
        pass
