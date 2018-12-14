#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
学校管理员
"""

__author__ = 'Cliff Wang'

from schoolMember import SchoolMember
from school import School

class Manager(SchoolMember):

    menu = {
        "1": "登录学校",
        "11": "管理员管理",
        "111": "查看管理员列表",
        "112": "新增管理员",
        "113": "修改管理员",
        "114": "删除管理员",
        "110": "退出管理员管理",
        "12": "课程管理",
        "121": "查看课程列表",
        "122": "新增课程",
        "123": "修改课程",
        "124": "删除课程",
        "120": "退出课程管理",
        "13": "班级管理",
        "131": "查看班级列表",
        "132": "新增班级",
        "133": "修改班级",
        "134": "删除班级",
        "130": "退出班级管理",
        "14": "老师管理",
        "141": "查看老师列表",
        "142": "招聘老师",
        "143": "修改管理员",
        "144": "删除老师",
        "140": "退出老师管理",
        "15": "学生管理",
        "151": "查看学生列表",
        "154": "开出学生",
        "150": "退出学生管理",
        "16": "修改密码",
        "10": "退出登录",
        "0": "退出"
    }

    def __init__(self, school, title):
        super().__init__(school, title)
        num = 0
        for item in school.managers:
            if int(item.schoolID[-3:]) > num:
                num = int(item.schoolID[-3:])
        self.schoolID = "1" + ("00" + str(num))[-3:]
        self.status = True
        school.managers.append(self)

    @classmethod
    def schoolAdd(cls):
        try:
            school = School()
        except Exception as e:
            print(str(e))
        else:
            person = Manager(school, "Manager")
            school.managers.append(person)
            School.dataDump(school)

if __name__ == "__main__":
    Manager.schoolAdd()
