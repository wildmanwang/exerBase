# -*- coding:utf-8 -*-
"""
课程

建立课程档案
"""
__author__ = "Cliff.wang"

class Subject(object):

    def __init__(self, name, weeks, chapter, tuition):
        self.name = name                #课程名称
        self.weeks = weeks              #学完该课程要多少周
        self.chapter = chapter          #包含多少次成绩
        self.tuition = tuition          #学费
