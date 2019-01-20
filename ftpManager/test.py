# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
listHelp = {
    "cd pathname":"切换目录",
    "put filename":"上传文件",
    "get filename":"下载文件"
}
strHelp = ""
for item in listHelp:
    strHelp += (item + "\t" + listHelp[item] + "\n")
print(strHelp)