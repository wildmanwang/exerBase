# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import os
import configparser

class User(object):

    def __init__(self, id):
        pass

class UserManager(object):

    def __init__(self, configfile):
        self.configfile = configfile
        self.config = configparser.ConfigParser()
        self.config.read(self.configfile, encoding="utf-8")

        self.rootPath = self.config.get("general", "rootPath").rstrip("\\")
        self.initSize = self.config.get("general", "initSize")
        self.increaseSize = self.config.get("general", "initSize")

    def userReg(self, code, name, password):
        """
        注册用户
        :param name:
        :param password:
        :return:
        """
        # 判断数据合法性
        code = code.strip()
        try:
            data = self.config.get(code, "name")
            return False, "用户{code}已存在".format(code=code)
        except Exception as e:
            pass
        name = name.strip()
        if not len(name) > 0:
            return False, "用户名{name}无效".format(name=name)

        # 创建用户空间
        path = "{root}\\{code}".format(root=self.rootPath, code=code)
        if os.path.exists(path):
            return False, "用户{code}已存在".format(code=code)
        os.mkdir(path)

        # 保存数据
        self.config.add_section(code)
        self.config.set(code, "name", name)
        self.config.set(code, "password", password)
        self.config.set(code, "storageSize", self.initSize)
        self.config.write(open(self.configfile, "w", encoding="utf-8"))
        return True, "用户[{code}]{name}注册成功".format(code=code, name=name)

    def userLogin(self, code, password):
        """
        用户登录
        :param code:
        :param password:
        :return:
        """
        code = code.strip()
        try:
            data = self.config.get(code, "password")
            name = self.config.get(code, "name")
            if data == password:
                return True, name, "登录成功"
            else:
                return False, "", "密码错误"
        except Exception as e:
            return False, code, "用户不存在"

    def password(self, code, pwold, pwnew):
        """
        修改密码
        :param code:
        :param pwold:
        :param pwnew:
        :return:
        """
        try:
            data = self.config.get(code, "password")
            name = self.config.get(code, "name")
            if data == pwold:
                self.config.set(code, "password", pwnew)
                self.config.write(open(self.configfile, "w", encoding="utf-8"))
                return True, name, "修改密码成功"
            else:
                return False, name, "原密码输入错误"
        except Exception as e:
            return False, code, "用户不存在"

    def mkDir(self, path, name):
        """
        创建目录
        :param path:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)
        curPath = os.path.join(curPath, name)
        # 判断目录是否存在
        if not os.path.exists(curPath):
            os.mkdir(curPath)
            return True, "目录创建成功"
        else:
            return False, "目录已存在"

    def delDir(self, path, name):
        """
        删除目录
        :param path:
        :param name:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)
        curPath = os.path.join(curPath, name)
        # 判断目录是否存在
        if os.path.exists(curPath):
            files = os.listdir(curPath)
            if len(files) > 0:
                return False, "目录非空，不能删除"
            try:
                os.rmdir(curPath)
            except Exception as e:
                return False, "删除目录失败"
            return True, "目录删除成功"
        else:
            return False, "目录不存在"

if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    manager = UserManager(path + "\\user")
    print(manager.rootPath)
