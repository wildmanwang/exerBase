# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import hashlib

data = "123"
md5 = hashlib.md5()
md5.update(data.encode("utf-8"))
print(md5.hexdigest())
