# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import hashlib

m = hashlib.md5()
m.update(b"test")
print(m.hexdigest())
print(b"abc".decode())
ss = m.digest()
print(type(ss))
ss = ss.decode()
print(ss)
