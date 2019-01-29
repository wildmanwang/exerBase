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
        self.config.set(code, "storaged", "0M")
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
        if os.path.exists(curPath):
            return False, "目录已存在"
        try:
            os.mkdir(curPath)
        except Exception as e:
            return False, "创建目录失败"
        return True, "目录创建成功"

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
        if not os.path.exists(curPath):
            return False, "目录不存在"
        files = os.listdir(curPath)
        if len(files) > 0:
            return False, "目录非空，不能删除"
        try:
            os.rmdir(curPath)
        except Exception as e:
            return False, "删除目录失败"
        return True, "目录删除成功"

    def renameDir(self, path, oldname, newname):
        """
        重命名目录
        :param path:
        :param oldname:
        :param newname:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)
        oldPath = os.path.join(curPath, oldname)
        if not os.path.exists(oldPath):
            return False, "原目录不存在"
        newPath = os.path.join(curPath, newname)
        if os.path.exists(newPath) and os.path.isdir(newPath):
            return False, "已存在同名目录"
        try:
            os.rename(oldPath, newPath)
        except Exception as e:
            return False, "重命名目录失败"
        return True, "重命名目录成功"

    def delFile(self, path, filename):
        """
        删除文件
        :param path:
        :param filename:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)
        curPath = os.path.join(curPath, filename)
        # 判断文件是否存在
        if not os.path.exists(curPath):
            return False, "文件不存在"
        if not os.path.isfile(curPath):
            return False, "对象为非文件"
        try:
            os.remove(curPath)
        except Exception as e:
            return False, "删除文件失败"
        return True, "文件删除成功"

    def renameFile(self, path, oldname, newname):
        """
        重命名文件
        :param path:
        :param oldname:
        :param newname:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)
        oldPath = os.path.join(curPath, oldname)
        if not os.path.exists(oldPath):
            return False, "原文件不存在"
        if not os.path.isfile(oldPath):
            return False, "对象为非文件"
        newPath = os.path.join(curPath, newname)
        if os.path.exists(newPath) and os.path.isfile(newPath):
            return False, "已存在同名文件"
        try:
            os.rename(oldPath, newPath)
        except Exception as e:
            return False, "重命名文件失败"
        return True, "重命名文件成功"

    def cd(self, path, pathname):
        """
        切换目录
        :param path:
        :param pathname:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)

        newpath = path
        if pathname == "..":
            if len(path) < 2:
                return False, None, "已经是根目录，无权获取上层目录"
            newpath.pop()
        else:
            distpath = os.path.join(curPath, pathname)
            if not os.path.exists(distpath):
                return False, None, "目标目录不存在"
            if not os.path.isdir(distpath):
                return False, None, "指定对象非目录"
            newpath.append(pathname)
        return True, newpath, "切换目录成功"

    def dir(self, path):
        """
        显示文件列表
        :param path:
        :return:
        """
        # 获取所在目录
        curPath = self.rootPath
        for i in path:
            curPath = os.path.join(curPath, i)

        list = os.listdir(curPath)
        pathlist = []
        filelist = []
        for i in list:
            if os.path.isdir(i):
                pathlist.append(i)
            else:
                filelist.append(i)
        return True, pathlist, filelist, "获取列表成功"

    def getSize(self, code):
        """
        获取用户空间数据
        :param code:
        :return:
        """
        pass

    def setSize(self, storagesize=-1, storaged=-1):
        """
        更新用户空间数据
        :param storagesize:
        :param storaged:
        :return:
        """
        pass

if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    manager = UserManager(path + "\\user")
    print(manager.rootPath)
