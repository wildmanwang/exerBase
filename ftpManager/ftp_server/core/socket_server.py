# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socketserver
import json
import hashlib
import sys, os

pathRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pathConf = os.path.join(pathRoot, "conf")
sys.path.append(pathConf)
import config

class FtpServer(socketserver.BaseRequestHandler):

    ResponseDict = {
        100:"命令解析成功",
        101:"文件接收成功",
        102:"文件校验成功",
        103:"开始发送数据",
        199:"操作成功",
        200:"命令解析失败",
        201:"个人空间不足",
        202:"权限不足",
        203:"指定文件不存在",
        204:"文件校验失败",
        209:"用户取消操作",
        299:"操作失败"
    }

    #def __init__(self, request, client_address, server):
    #    super().__init__(self, request, client_address, server)
    #    userManager = UserManager(pathConf)

    def handle(self):
        """
        处理客户端交互
        :return:
        """
        while True:
            try:
                data = self.__getMsg("dict")
                if hasattr(self, "srv_{action}".format(action=data["action"])):
                    func = getattr(self, "srv_{action}".format(action=data["action"]))
                    self.__putInter(100)
                    func(data)
                else:
                    self.__putInter(200)
                    continue
            except Exception as e:
                print(e)
                return

    def srv_login(self, args):
        """
        登录
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        code = args["code"]
        password = args["password"]
        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, name, info = userManager.userLogin(code, password)
        if result:
            self.__putInter(199, name=name, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_pwd(self, args):
        pass

    def srv_cd(self, args):
        pass

    def srv_dir(self, args):
        pass

    def srv_put(self, args):
        """
        响应上传文件
        :param args:
        :return:
        """
        fileName = args["fileName"]
        fileSize = args["fileSize"]
        filePath = args["path"]
        if len(filePath) == 0:
            self.__putInter(202)

        recievedSize = 0
        tmp = pathRoot
        for i in filePath:
            tmp = os.path.join(tmp, i)
        fileName = os.path.join(tmp, fileName)
        f = open(fileName, "wb")
        md5 = hashlib.md5()
        while fileSize - recievedSize > 0:
            if fileSize - recievedSize >= 1024:
                curSize = 1024
            else:
                curSize = fileSize - recievedSize
            curData = self.request.recv(curSize)
            f.write(curData)
            recievedSize += len(curData)
            md5.update(curData)
        f.close()
        self.__putInter(101)
        codeTrans = self.__getMsg()
        codeCompu = md5.hexdigest()
        if codeTrans == codeCompu:
            self.__putInter(102)
        else:
            self.__putInter(204)
            os.remove(fileName)

    def srv_get(self, args):
        """
        响应下载文件
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        fileName = args["fileName"]
        if not os.path.isfile(fileName):
            self.__putInter(203)
            return

        self.__putInter(103, size=os.path.getsize(fileName))
        f = open(fileName, "rb")
        md5 = hashlib.md5()
        for line in f:
            self.request.send(line)
            md5.update(line)
        f.close()
        codeCompu = md5.hexdigest()
        codeTrans = self.__getMsg()
        if codeCompu == codeTrans:
            self.__putInter(102)
        else:
            self.__putInter(204)

    def __getMsg(self, type="str", size=1024):
        """
        接收信息
        :return:
        """
        if type != "dict" and type != "str":
            raise Exception("Invalid message format.")
        data = self.request.recv(size).strip()
        data = data.decode()
        if type == "dict":
            data = json.loads(data)
        return data

    def __putInter(self, code, **kwargs):
        """
        发送交互信息
        :return:
        """
        data = {"code":code, "info":FtpServer.ResponseDict[code]}
        data.update(kwargs)
        self.request.send(json.dumps(data).encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), FtpServer)
    server.serve_forever()
