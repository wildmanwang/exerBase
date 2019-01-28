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

    def srv_reg(self, args):
        """
        响应注册
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        code = args("code")
        name = args("name")
        password = args("password")
        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, info = userManager.userReg(code, name, password)
        if result:
            self.__putInter(199, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_login(self, args):
        """
        响应登录
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

    def srv_password(self, args):
        """
        响应修改密码
        :param args:{"action":"password", "pwold":pwold, "pwnew":pwnew}
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        code = args["code"]
        pwold = args["pwold"]
        pwnew = args["pwnew"]
        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, name, info = userManager.password(code, pwold, pwnew)
        if result:
            self.__putInter(199, name=name, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_mkdir(self, args):
        """
        响应创建目录
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        dirname = args["dirname"]
        filepath = args["path"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, info = userManager.mkDir(filepath, dirname)
        if result:
            self.__putInter(199, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_deldir(self, args):
        """
        响应删除目录
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        dirname = args["dirname"]
        filepath = args["path"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, info = userManager.delDir(filepath, dirname)
        if result:
            self.__putInter(199, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_renamedir(self, args):
        """
        响应重命名目录
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        filepath = args["path"]
        oldname = args["oldname"]
        newname = args["newname"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, info = userManager.renameDir(filepath, oldname, newname)
        if result:
            self.__putInter(199, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_delfile(self, args):
        """
        响应删除文件
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        filepath = args["path"]
        filename = args["filename"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, info = userManager.delFile(filepath, filename)
        if result:
            self.__putInter(199, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_renamefile(self, args):
        """
        响应删除文件
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        filepath = args["path"]
        oldname = args["oldname"]
        newname = args["newname"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, info = userManager.renameFile(filepath, oldname, newname)
        if result:
            self.__putInter(199, info=info)
        else:
            self.__putInter(299, info=info)

    def srv_cd(self, args):
        """
        切换目录
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        filepath = args["path"]
        pathname = args["pathname"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, newpath, info = userManager.cd(filepath, pathname)
        if result:
            self.__putInter(199, info=info, newpath=newpath)
        else:
            self.__putInter(299, info=info)

    def srv_dir(self, args):
        """
        显示文件列表
        :param args:
        :return:
        """
        responseData = self.__getMsg()
        if responseData != "OK":
            self.__putInter(209)
            return

        filepath = args["path"]
        if len(filepath) == 0:
            self.__putInter(202, info="当前目录无效")
            return

        userManager = config.UserManager(os.path.join(pathConf, "user"))
        result, paths, files, info = userManager.dir(filepath)
        if result:
            self.__putInter(199, info=info, paths=paths, files=files)
        else:
            self.__putInter(299, info=info)

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
            return

        recievedSize = 0
        tmp = os.path.join(pathRoot, "data")
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
        filePath = args["path"]
        tmp = os.path.join(pathRoot, "data")
        for i in filePath:
            tmp = os.path.join(tmp, i)
        fileName = os.path.join(tmp, fileName)
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
