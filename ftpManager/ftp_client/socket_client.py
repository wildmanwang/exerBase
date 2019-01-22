# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket
import os
import json
import hashlib

class FtpClient(object):

    def __init__(self):
        self.host = "localhost"
        self.port = 9999
        self.name = ""
        self.path = "\\"
        self.client = socket.socket()

    def connect(self, host, port):
        self.client.connect((host, port))

    def interactive(self):
        """
        客户端交互
        :return:
        """
        if not self.login():
            return

        self.connect(self.host, self.port)

        while True:
            strCmd = input(">>>:").strip()
            if strCmd == "":
                continue
            if strCmd.upper() == "EXIT":
                break
            elif hasattr(self, "cmd_{cmd}".format(cmd=strCmd.split()[0])):
                func = getattr(self, "cmd_{cmd}".format(cmd=strCmd.split()[0]))
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
            "put filename newfilename":"上传文件",
            "get filename newfilename":"下载文件",
            "exit":"退出"
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
        return True

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
        cmdList = strCmd.split()
        if len(cmdList) < 2:
            print("请指定上传文件名")
            return

        if os.path.isfile(cmdList[1]):
            fileSize = os.path.getsize(cmdList[1])
            fileInfo = {
                "action":"put",
                "fileName":cmdList[2] if len(cmdList) >= 3 else cmdList[1],
                "fileSize":fileSize
            }
            self.client.send(json.dumps(fileInfo).encode())
            responseData = self.__getResponse()
            if responseData["code"] == 100:  #开始上传
                f = open(cmdList[1], "rb")
                sendedSize = 0
                md5 = hashlib.md5()
                for line in f:
                    self.client.send(line)
                    sendedSize += len(line)
                    md5.update(line)
                f.close()
                responseData = self.__getResponse()
                if responseData["code"] == 101:
                    self.client.send(md5.hexdigest().encode())
                    responseData = self.__getResponse()
        else:
            print(cmdList[1], " is not exists.")

    def cmd_get(self, strCmd):
        """
        下载文件
        :param strCmd:
        :return:
        """
        cmdList = strCmd.split()
        if len(cmdList) < 2:
            print("请指定下载文件名")
            return

        fileInfo = {
            "action":"get",
            "fileName":cmdList[1]
        }
        self.client.send(json.dumps(fileInfo).encode())
        responseData = self.__getResponse()
        if responseData["code"] == 100:
            self.client.send(b"OK")
            responseData = self.__getResponse()
            if responseData["code"] != 103:
                return

            fileName = cmdList[2] if len(cmdList) >= 3 else cmdList[1]
            fileSize = responseData["size"]
            recievedSize = 0
            f = open(fileName, "wb")
            md5 = hashlib.md5()
            while fileSize - recievedSize > 0:
                if fileSize - recievedSize >= 1024:
                    curSize = 1024
                else:
                    curSize = fileSize - recievedSize
                curData = self.client.recv(curSize)
                f.write(curData)
                recievedSize += len(curData)
                md5.update(curData)
            f.close()
            self.client.send(md5.hexdigest().encode())
            self.__getResponse()

    def __getResponse(self):
        """
        获取服务器响应
        :return:
        """
        data = self.client.recv(1024).strip()
        data = json.loads(data.decode())
        print("{code}\t{info}".format(code=data["code"], info=data["info"]))
        return data

if __name__ == "__main__":
    client = FtpClient()
    client.interactive()
