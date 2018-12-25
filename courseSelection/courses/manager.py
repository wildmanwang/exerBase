#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
学校管理员
"""

__author__ = 'Cliff Wang'

from courses.schoolMember import SchoolMember

class Manager(SchoolMember):

    menu = {
        "1": "管理员管理-manager",
        "11": "查看管理员列表-printList",
        "12": "新增管理员-add",
        "13": "修改管理员-modify",
        "14": "删除管理员-delete",
        "10": "退出管理员管理-",
        "2": "课程管理-subject",
        "21": "查看课程列表-printList",
        "22": "新增课程-add",
        "23": "修改课程-modify",
        "24": "删除课程-delete",
        "20": "退出课程管理-",
        "3": "老师管理-teacher",
        "31": "查看老师列表-printList",
        "32": "招聘老师-add",
        "33": "修改老师-modify",
        "34": "删除老师-delete",
        "30": "退出老师管理-",
        "4": "班级管理-grade",
        "41": "查看班级列表-printList",
        "42": "新增班级-add",
        "43": "修改班级-modify",
        "44": "删除班级-delete",
        "45": "指定课程-gradeSetSubject",
        "46": "指定老师-gradeSetTeacher",
        "47": "开课-gradeStart",
        "40": "退出班级管理-",
        "5": "学生管理-student",
        "51": "查看学生列表-printList",
        "54": "开除学生-delete",
        "50": "退出学生管理-",
        "6": "查看我的资料-printSelf",
        "7": "修改密码-password",
        "0": "退出登录-",
    }

    def __init__(self, school):
        self.title = "manager"
        super().__init__(school)
        num = 0
        for item in self.school.managers:
            if int(item.sID[-3:]) > num:
                num = int(item.sID[-3:])
        num += 1
        self.sID = "1" + ("00" + str(num))[-3:]
        self.status = True
        self.school.managers.append(self)

if __name__ == "__main__":
    pass
