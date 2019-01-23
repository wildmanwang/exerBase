# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import time
import random

totleSize = 329827065
recievedSize = 0
step = 0
while totleSize - recievedSize < 0:
    recievedSize += random.randint(10, 1024)
    time.sleep(0.1)
    print("█", end="", flush=True)

print(int(19/100 * 100 / 5))
print(divmod(16, 100))