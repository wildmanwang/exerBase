# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from urllib import request
import gevent, time
from gevent import monkey

monkey.patch_all()          #把当前程序的全部IO操作标记出来，使gevent能够识别并自动切换协程

def spide_fun(url):
    print("Get:%s" % url)
    resp = request.urlopen(url)
    data = resp.read()
    print("%d bytes recieved from %s." % (len(data), url))

urls = [
    "https://www.python.org",
    "https://www.yahoo.com",
    "https://github.com"
]

time_serial = time.time()
for url in urls:
    spide_fun(url)
print("同步cost:", time.time() - time_serial)

time_parallel = time.time()
gevent.joinall([
    gevent.spawn(spide_fun, "https://www.python.org"),
    gevent.spawn(spide_fun, "https://www.yahoo.com"),
    gevent.spawn(spide_fun, "https://github.com")
])
print("异步cost:", time.time() - time_parallel)
