# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socketserver
import json

class ftpServer(socketserver.BaseRequestHandler):

    def handle(self):
        """
        处理客户端交互
        100     命令解析成功
        101     准备接收文件
        102     准备发送文件
        200     命令解析失败
        201     个人空间不足
        202     权限不足
        :return:
        """
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                self.data = json.loads(self.data.decode("utf-8"))
                self.action = self.data["action"]
                if hasattr(self, "srv_{action}".format(action=self.action)):
                    func = getattr(self, "srv_{action}".format(action=self.action))
                    self.request.send(json.dumps({"code":100, "info":"收到指令，准备就绪"}).encode("utf-8"))
                    func(self.data)
                else:
                    self.request.send(json.dumps({"code":200, "info":"无法解析的命令"}).encode("utf-8"))
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
        接收上传文件
        :param args:
        :return:
        """
        fileName = args["fileName"]
        fileSize = args["fileSize"]
        recievedSize = 0
        f = open(fileName.split(".")[0] + "_new." + fileName.split(".")[1], "wb")
        while fileSize - recievedSize > 0:
            if fileSize - recievedSize >= 1024:
                curSize = 1024
            else:
                curSize = fileSize - recievedSize
            curData = self.request.recv(curSize)
            f.write(curData)
            recievedSize += curSize
            print("{num}/{sum}".format(num=recievedSize, sum=fileSize))
        f.close()

    def srv_get(self, args):
        pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), ftpServer)
    server.serve_forever()
