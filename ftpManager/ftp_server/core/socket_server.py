# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socketserver
import json
import hashlib
import os

class ftpServer(socketserver.BaseRequestHandler):

    ResponseDict = {
        100:"命令解析成功",
        101:"文件接收成功",
        102:"文件校验成功",
        103:"开始发送数据",
        200:"命令解析失败",
        201:"个人空间不足",
        202:"权限不足",
        203:"指定文件不存在",
        204:"文件校验失败",
        209:"用户取消操作"
    }

    def handle(self):
        """
        处理客户端交互
        :return:
        """
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                self.data = json.loads(self.data.decode())
                self.action = self.data["action"]
                if hasattr(self, "srv_{action}".format(action=self.action)):
                    func = getattr(self, "srv_{action}".format(action=self.action))
                    self.__putInter(100)
                    func(self.data)
                else:
                    self.__putInter(200)
                    continue
            except Exception as e:
                print(e)
                continue

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
        recievedSize = 0
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
        codeTrans = self.request.recv(1024).strip().decode()
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
        responseData = self.request.recv(1024).strip()
        responseData = responseData.decode()
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
        codeTrans = self.request.recv(1024).strip().decode()
        if codeCompu == codeTrans:
            self.__putInter(102)
        else:
            self.__putInter(204)

    def __getInter(self):
        """
        获取交互信息
        :return:
        """
        pass

    def __putInter(self, code, **kwargs):
        """
        发送交互信息
        :return:
        """
        data = {"code":code, "info":ftpServer.ResponseDict[code]}
        data.update(kwargs)
        self.request.send(json.dumps(data).encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), ftpServer)
    server.serve_forever()
