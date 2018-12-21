#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
程序入口
"""

import os, sys
from courses.main import course_main
from courses.school import School

if __name__ == "__main__":
    # 获取项目根目录
    if 1 == 1:              # 编程环境
        sFile = __file__
    else:                   # 可执行环境
        sFile = sys.executable
    sPathRoot = os.path.dirname(os.path.dirname(os.path.abspath(sFile)))
    sys.path.append(sPathRoot)
    course_main(sPathRoot)
