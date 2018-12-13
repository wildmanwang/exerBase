#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
学校管理员

学校管理员界面
    登录
        创建学校
        选择学校
            管理员管理
                查看管理员
                创建管理员
                修改管理员
                退出管理员管理
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
            学生管理
                查看学生列表
                开除学生
            退出学校
        修改密码
        退出登录
    退出
"""

__author__ = 'Cliff Wang'

from schoolMember import SchoolMember

class manager(SchoolMember):

    def __init__(self, id, name, pwd, sex, birthDate):
        super().__init__(id, name, pwd, sex, birthDate)

