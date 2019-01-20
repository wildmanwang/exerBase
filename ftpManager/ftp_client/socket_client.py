# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket
import os
import json

class FtpClient(object):

    def __init__(self):
        self.name = ""
        self.path = "\\"
        self.client = socket.socket()

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def interactive(self):
        """
        客户端交互
        :return:
        """
        if not self.login():
            return

        while True:
            strCmd = input(">>>:").strip()
            if strCmd == "":
                continue
            if hasattr(self, "cmd_{cmd}".format(cmd=strCmd.split()[0])):
                func = getattr(self, "cmd_{cmd}".format(cmd=strCmd.split([0])))
                func(strCmd)
            else:
                self.help()

    def help(self):
        """
        显示命令帮助
        :return:
        """
        listHelp = {
            "cd pathname":"切换目录",
            "put filename":"上传文件",
            "get filename":"下载文件"
        }
        strHelp = "没有找到对应的指令。帮助如下："
        for item in listHelp:
            strHelp += "\n{key}\t{value}".format(key=item, value=listHelp[item])
        print(strHelp)

    def login(self):
        """
        登录
        :return:bool
        """

    def cmd_pwd(self, strCmd):
        pass

    def cmd_cd(self, strCmd):
        pass

    def cmd_dir(self, strCmd):
        pass

    def cmd_put(self, strCmd):
        """
        上传文件
        :param strCmd:
        :return:
        """
        fileName = strCmd.split[1]
        if os.path.isfile(fileName):
            fileSize = os.stat(fileName).st_size
            fileInfo = {
                "action":"put",
                "fileName":fileName,
                "fileSize":fileSize,
                "overridden":True
            }
            self.client.send(json.dumps(fileInfo).encode("utf-8"))
            strResponse = self.client.recv(1024)
            #根据不同的返回码处理不同的情况
        else:
            print(fileName, " is not exists.")

    def cmd_get(self, strCmd):
        pass

client = FtpClient()
client.help()
