# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket
import os
import json
import hashlib
import functools

def authenticate(func):
    """
    身份验证
    :return:
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if len(self.code) == 0:
            code = input("请输入登录代码>>")
            password = input("请输入登录密码>>")
            strCmd = "login {code} {password}".format(code=code, password=password)
            self.cmd_login(strCmd)
        if len(self.code) > 0:
            func(self, args[0])
    return wrapper

class FtpClient(object):

    def __init__(self):
        self.host = "localhost"
        self.port = 9999
        self.code = ""
        self.name = ""
        self.path = []
        self.client = socket.socket()

    def connect(self, host, port):
        self.client.connect((host, port))

    def interactive(self):
        """
        客户端交互
        :return:
        """
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
                self.cmd_help(strCmd)

    def cmd_help(self, strCmd):
        """
        显示命令帮助
        :return:
        """
        listHelp = {
            "reg"
            "cd pathname":"切换目录",
            "put filename newfilename":"上传文件",
            "get filename newfilename":"下载文件",
            "exit":"退出"
        }
        if strCmd == "help":
            strHelp = ""
        else:
            strHelp = "没有找到对应的指令。\n"
        strHelp += "FTP系统命令帮助如下："
        for item in listHelp:
            strHelp += "\n{key}\t{value}".format(key=item, value=listHelp[item])
        print(strHelp)

    def cmd_reg(self, strCmd):
        """
        注册
        :param strCmd:reg code name password
        :return:
        """
        cmdList = strCmd.split()
        if len(cmdList) < 3:
            print("请输入用户代码（必须）、用户名称（必须）、登录密码（默认123456）")
            return

        if len(cmdList) >=4:
            password = cmdList[3]
        else:
            password = "123456"
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        password = md5.hexdigest()
        cmdInfo = {
            "action":"reg",
            "code":cmdList[1],
            "name":cmdList[2],
            "password":password
        }
        self.__putMsg(cmdInfo)
        self.__getResponse()

    def cmd_login(self, strCmd):
        """
        登录
        :param strCmd:login <code> <password>
        :return:
        """
        cmdList = strCmd.split()
        if len(cmdList) < 2:
            print("请输入用户代码（必须）、密码（非必须）")
            return

        if len(cmdList) >=3:
            password = cmdList[2]
        else:
            password = "123456"
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        password = md5.hexdigest()
        cmdInfo = {
            "action":"login",
            "code":cmdList[1],
            "password":password
        }
        self.__putMsg(cmdInfo)
        responseData = self.__getResponse()
        if responseData["code"] == 100:
            self.__putMsg("OK")
            responseData = self.__getResponse()
            if responseData["code"] == 199:
                self.code = cmdList[1]
                self.name = responseData["name"]
                self.path = [self.code]
                print("{name}，欢迎你".format(name=self.name))
                return True
            else:
                return False
        else:
            return False

    def cmd_logout(self, strCmd):
        """
        登出
        :param strCmd:logout
        :return:
        """
        if len(self.code) > 0:
            print("{name}，再来哦".format(name=self.name))
            self.code = ""
            self.name = ""
            self.path = []
        else:
            print("路人，您还没登录")

    @authenticate
    def cmd_password(self, strCmd):
        """
        修改密码
        :param strCmd:password pwold pwnew
        :return:
        """
        cmdList = strCmd.split()
        if len(cmdList) < 3:
            print("请输入原密码（必须）、新密码（必须）")
            return

        pwold = cmdList[1]
        pwnew = cmdList[2]
        md5 = hashlib.md5()
        md5.update(pwold.encode("utf-8"))
        pwold = md5.hexdigest()
        md5 = hashlib.md5()
        md5.update(pwnew.encode("utf-8"))
        pwnew = md5.hexdigest()
        cmdInfo = {
            "action":"password",
            "code":self.code,
            "pwold":pwold,
            "pwnew":pwnew
        }
        self.__putMsg(cmdInfo)
        responseData = self.__getResponse()
        if responseData["code"] == 100:
            self.__putMsg("OK")
            responseData = self.__getResponse()

    @authenticate
    def cmd_cd(self, strCmd):
        """
        切换目录
        :param strCmd:cd path
        :return:
        """
        pass

    @authenticate
    def cmd_dir(self, strCmd):
        """
        显示当前目录文件
        :param strCmd:dir
        :return:
        """
        pass

    @authenticate
    def cmd_put(self, strCmd):
        """
        上传文件
        :param strCmd:put filename newfilename
        :return:
        """
        cmdList = strCmd.split()
        if len(cmdList) < 2:
            print("请指定上传文件名")
            return

        if os.path.isfile(cmdList[1]):
            fileSize = os.path.getsize(cmdList[1])
            cmdInfo = {
                "action":"put",
                "fileName":cmdList[2] if len(cmdList) >= 3 else cmdList[1],
                "fileSize":fileSize,
                "path":self.path
            }
            self.__putMsg(cmdInfo)
            responseData = self.__getResponse()
            if responseData["code"] == 100:  #开始上传
                f = open(cmdList[1], "rb")
                sendedSize = 0
                step = 0
                md5 = hashlib.md5()
                for line in f:
                    self.client.send(line)
                    sendedSize += len(line)
                    md5.update(line)
                    while int(sendedSize / fileSize * 100 / 5) > step:
                        print("█", end="", flush=True)
                        step += 1
                f.close()
                print("", flush=True)
                responseData = self.__getResponse()
                if responseData["code"] == 101:
                    self.__putMsg(md5.hexdigest())
                    responseData = self.__getResponse()
        else:
            print(cmdList[1], "is not exists.")

    @authenticate
    def cmd_get(self, strCmd):
        """
        下载文件
        :param strCmd:get filename newfilename
        :return:
        """
        cmdList = strCmd.split()
        if len(cmdList) < 2:
            print("请指定下载文件名")
            return

        cmdInfo = {
            "action":"get",
            "fileName":cmdList[1],
            "path":self.path
        }
        self.__putMsg(cmdInfo)
        responseData = self.__getResponse()
        if responseData["code"] == 100:
            self.__putMsg("OK")
            responseData = self.__getResponse()
            if responseData["code"] != 103:
                return

            fileName = cmdList[2] if len(cmdList) >= 3 else cmdList[1]
            fileSize = responseData["size"]
            recievedSize = 0
            f = open(fileName, "wb")
            step = 0
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
                while int(recievedSize / fileSize * 100 / 5) > step:
                    print("█", end="", flush=True)
                    step += 1
            f.close()
            print("", flush=True)
            self.__putMsg(md5.hexdigest())
            self.__getResponse()

    def __putMsg(self, msg):
        """
        发送命令
        :return:
        """
        if type(msg) == dict:
            self.client.send(json.dumps(msg).encode())
        elif type(msg) == str:
            self.client.send(msg.encode())
        else:
            raise Exception("Invalid message format.")

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
