#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Cliff Wang'

from urllib.request import urlopen

data = urlopen("http://www.baidu.com")
print(data.read().decode("utf-8"))
