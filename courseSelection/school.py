# -*- coding:utf-8 -*-
"""
学校

学校管理员界面
    登录
        创建学校
        选择学校
            课程管理
                查看课程列表
                创建课程
                修改课程
                退出课程管理
            班级管理
                查看班级列表
                创建班级
                修改班级
                退出班级管理
            老师管理
                查看老师列表
                招聘老师
                修改老师档案
                解聘老师
                退出老师管理
            在读学生管理
            退出学校
        修改密码
        退出登录
    退出
"""
__author__ = "Cliff.wang"

class School(object):

    def __init__(self, name, addr):
        self.name = name            #名称
        self.addr = addr            #地址
        self.gradesOld = []         #曾经开过的课程
        self.grades = []            #当前有效课程
        self.teachers = []          #教职工列表
        self.students = []          #学生列表

    def offerCourses(self):
        pass

    def openSubject(self):
        pass

    def hireStaff(self):
        pass
