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
        code = input("请输入登录代码>>")
        password = input("请输入登录密码>>")
        strCmd = "login {code} {password}".format(code=code, password=password)
        if self.login(strCmd):
            func(strCmd, *args, **kwargs)
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
                self.help()

    def help(self):
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
        strHelp = "没有找到对应的指令。帮助如下："
        for item in listHelp:
            strHelp += "\n{key}\t{value}".format(key=item, value=listHelp[item])
        print(strHelp)

    def reg(self, strCmd):
        """
        注册
        :param strCmd:reg <code> <name> <password>
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

    def login(self, strCmd):
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
                self.path.append(self.code)
                print("{name}，欢迎你".format(name=self.name))
                return True
            else:
                return False
        else:
            return False

    def logout(self):
        """
        登出
        :return:
        """
        if len(self.code) > 0:
            print("{name}，再来哦")
            self.code = ""
            self.name = ""
            self.path = []
        else:
            print("路人，请登录")

    @authenticate
    def cmd_pwd(self, strCmd):
        pass

    @authenticate
    def cmd_cd(self, strCmd):
        pass

    @authenticate
    def cmd_dir(self, strCmd):
        pass

    @authenticate
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
                    if int(sendedSize / fileSize * 100 / 5) > step:
                        print("█", end="", flush=True)
                        step += 1
                f.close()
                responseData = self.__getResponse()
                if responseData["code"] == 101:
                    self.__putMsg(md5.hexdigest())
                    responseData = self.__getResponse()
        else:
            print(cmdList[1], " is not exists.")

    @authenticate
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

        cmdInfo = {
            "action":"get",
            "fileName":cmdList[1]
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
                if int(recievedSize / fileSize * 100 / 5) > step:
                    print("█", end="", flush=True)
                    step += 1
            f.close()
            print("")
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
