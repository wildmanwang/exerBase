# -*- coding:utf-8 -*-
"""
实现信用卡管理，主要功能包括：
登录
开卡
消费
取现
转账
还款
挂失
修改密码
查询
注销
"""
__author__ = "Cliff.wang"

import os, pickle, hashlib, configparser, functools, json
from datetime import datetime, date

sRootPath = os.path.dirname(os.path.abspath(__file__))

class bankClass():
    """
    银行卡属性
    IDNumber        卡号
    name            姓名
    sex             性别：{1:'男', 0:'女'}
    password        密码
    line            信用额度
    tackcash        取现额度
    balance         当前余额
    validdate       有效期至
    state           状态：['正常', '挂失', '过期', '注销']
    info            报错信息
    """

    CreditLine = 0.00           #信用额度
    CashPercent = 0.00          #取现额度
    ValidYears = 0               #有效年限

    def card_log(self, remark):
        """
        操作日志
        :param remark:日志内容
        :return:
        """
        f = open(os.path.join(os.path.join(sRootPath, "logs"), self.IDNumber + ".log"), "a+", encoding="utf-8")
        f.write("\n" + remark)
        f.close()

    def card_refresh(func):
        """
        刷新卡状态，通常用于业务操作之前
        :return:
        """
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            if self.state in ["挂失", "过期", "注销"]:
                pass
            elif self.validdate < date.today():
                self.state = "过期"
            self.info = ""
            return func(self, *args, **kw)
        return wrapper

    def __init__(self, idnumber, password):
        """
        卡登录
        :param idnumber:卡号
        :param password:密码
        """
        conf = configparser.ConfigParser()
        if len(conf.read(os.path.join(sRootPath, "conf.ini"), encoding="utf-8")) == 0:
            self.IDNumber = ""
            self.info = "读取配置文件失败."
            return
        bankClass.CreditLine = conf.getfloat("card", "creditline")
        bankClass.ValidYears = conf.getint("card", "validyears")
        if idnumber is None or idnumber == "":
            self.IDNumber = ""
            self.info = "请输入卡号."
            return
        else:
            try:
                f = open(os.path.join(os.path.join(sRootPath, "accounts"), idnumber + ".data"), "rb")
                obj = pickle.load(f)
            except FileNotFoundError:
                self.IDNumber = ""
                self.info = "账号或密码错误."
                return
            enc = hashlib.sha256()
            enc.update(password.encode("utf-8"))
            if enc.hexdigest() != obj.password:
                self.IDNumber = ""
                self.info = "账号或密码错误."
                return
            self.IDNumber = obj.IDNumber
            self.name = obj.name
            self.sex = obj.sex
            self.password = obj.password
            self.line = obj.line
            self.takecash = obj.takecash
            self.balance = obj.balance
            self.validdate = obj.validdate
            self.state = obj.state
            self.info = ""

    def card_dump(self):
        """
        数据保存
        :return:错误信息
        """
        if len(self.IDNumber) > 0:
            with open(os.path.join(os.path.join(sRootPath, "accounts"), self.IDNumber + ".data"), "wb") as f:
                pickle.dump(self, f)
        else:
            self.info = "账号还没有登录."

    def card_logout(self):
        """
        登出
        :return:
        """
        if len(self.IDNumber) > 0:
            self.IDNumber = ""
            self.name = ""
            self.sex = 0
            self.password = ""
            self.line = 0.00
            self.takecash = 0.00
            self.balance = 0.00
            self.validdate = None
            self.state = ""
            self.info = ""

    def card_open(self, name, sex, password):
        """
        开卡
        :param name:姓名
        :param sex:性别 {1:"男", 0:"女"}
        :param password:卡密码
        :return:
        """
        self.IDNumber = ""
        self.name = name
        self.sex = sex
        self.info = ""
        if password is None or password.strip() == "":
            password = "123456"
        else:
            password = password.strip()
        enc = hashlib.sha256()
        enc.update(password.encode("utf-8"))
        self.password = enc.hexdigest()
        self.line = bankClass.CreditLine
        self.takecash = 0.00
        self.balance = 0.00
        self.validdate = date.today()
        self.state = "正常"
        conf = configparser.ConfigParser()
        if len(conf.read(os.path.join(sRootPath, "conf.ini"), encoding="utf-8")) == 0:
            self.info = "读取配置文件失败."
            return
        maxnumber = conf.getint("card", "maxnumber") + 1
        conf.set("card", "maxnumber", str(maxnumber))
        with open(os.path.join(sRootPath, "conf.ini"), "w", encoding="utf-8") as f:
            conf.write(f)
        self.IDNumber = datetime.now().strftime("%Y%m%d") + str(maxnumber).rjust(4, "0")
        self.validdate = date(date.today().year + bankClass.ValidYears, date.today().month, date.today().day)
        self.card_dump()
        self.card_log("开卡人[{name}], 信用额度[{line}]".format(name = self.name, line = self.line))
        return self.info

    @card_refresh
    def card_business(self, busitype, amt=0.0, remark="", *other, **parms):
        """
        卡业务处理
        :param busitype:业务类型
        :param amt: 发生金额
        :param remark: 业务备注
        :param other: 其它参数列表
        :param parms: 其它参数字典
        :return:
        """
        if busitype is None or len(busitype) == 0:
            self.info = "没有指定业务类型."
            return self.info
        conf = configparser.ConfigParser()
        if len(conf.read(os.path.join(sRootPath, "conf.ini"), encoding="utf-8")) == 0:
            self.info = "读取配置文件失败."
            return self.info
        if busitype not in conf.options("business"):
            self.info = "业务类型[{type}]无效.".format(type=busitype)
            return self.info
        dConfig = json.loads(conf.get("business", busitype), encoding="utf-8")
        if self.state not in dConfig["statefrom"].split("/"):
            self.info = "[{state}]状态下不能做[{type}]业务.".format(state=self.state, type=dConfig["name"])
            return self.info
        dDirec = dConfig["direction"]       #金额变动方向

        #额度判断
        dLimit = dConfig["limit"]  # 额度比例
        dFee = amt * dConfig["feerate"] #费用
        if dLimit >= 0:
            dLine = self.line * dLimit  # 可用额度
            if amt - dFee * dDirec > dLine:
                self.info = "[{type}]额度不够：可用额度[{line}]，发生额[{amt}].".format(type=dConfig["name"], line=dLine, amt=amt-dFee*dDirec)
                return self.info
        if busitype == "cancel":    #注销业务特殊判断
            if self.balance < 0:
                self.info = "您还有欠费，不能[{type}].".format(type=dConfig["name"])
                return self.info

        #余额变更
        if dDirec == 1 or dDirec == -1:
            self.balance = self.balance + amt * dDirec - dFee

        #修改密码特殊处理
        if busitype == "password":
            if len(other) < 2:
                self.info = "请提供原密码和新密码."
                return self.info
            enc = hashlib.sha256()
            enc.update(other[0].encode("utf-8"))
            if enc.hexdigest() != self.password:
                self.info = "原密码错误."
                return self.info
            enc = hashlib.sha256()
            enc.update(other[1].encode("utf-8"))
            self.password = enc.hexdigest()

        #状态变更
        if len(dConfig["stateto"]) > 0:
            if dConfig["stateto"] in ["正常", "挂失", "过期", "注销"]:
                self.state = dConfig["stateto"]
            else:
                self.info = "转入状态无效."
                return self.info

        #保存
        self.card_dump()
        if len(self.info) > 0:
            return self.info

        #日志记录
        sTmp = "[{type}]，时间[{time}]".format(type=dConfig["name"], time=datetime.now())
        if amt > 0:
            sTmp += "，金额[{amt}]".format(amt=amt)
        if dFee > 0:
            sTmp += "，费用[{fee}]".format(fee=dFee)
        sTmp += "，余额[{balance}]".format(balance=self.balance)
        if len(remark) > 0:
            sTmp += "，备注[{remark}]".format(remark=remark)
        self.card_log(sTmp)

        return ""

    @card_refresh
    def card_query(self):
        """
        查询余额
        :return:查询结果
        """

        #返回查询结果
        self.info = "卡号[{idnumber}]，状态[{state}]，姓名[{name}]，余额[{balance}]，信用额度[{line}]".format(idnumber = self.IDNumber, state = self.state, name = self.name, balance = self.balance, line = self.line)

        return self.info

    @card_refresh
    def card_record(self):
        """
        查询交易记录
        :return:查询结果
        """

        self.info = "".center(50, "=") + "\n"
        self.info += "卡号[{idnumber}]，姓名[{name}]，状态[{state}]".format(idnumber=self.IDNumber, name=self.name, state=self.state) + "\n"
        self.info += "".center(50, "-") + "\n"
        with open(os.path.join(os.path.join(sRootPath, "logs"), self.IDNumber + ".log"), "rb") as f:
            for line in f.readlines():
                self.info += line.decode("utf-8")
        self.info += "\n"
        self.info += "".center(50, "-") + "\n"
        self.info += "查询时间[{time}]".format(time=datetime.now()) + "\n"
        self.info += "".center(50, "=") + "\n"
        return self.info

if __name__ == "__main__":
    if 1==2:
        c1 = bankClass("", "")
        c1.card_open("大英儿", 1, "123456")
        print(c1.card_query())
    elif 1==1:
        c1 = bankClass("201808180001", "123456")
        c2 = bankClass("201808180002", "123456")
        if len(c1.info) > 0 or len(c2.info) > 0:
            print(c1.info)
            print(c2.info)
        else:
            print(c1.card_business("cancel", 0.0, ""))
            #print(c2.card_business("losscancel", 0.0, ""))
            print(c1.card_record())
            #print(c2.card_record())
            #print(c1.card_repay(2000.00))
            #print(c1.card_trans("201808180002", 400.00))
    else:
        c1 = bankClass("201808180001", "123456")
        c1.card_business("repay", 100.0, "")
        if len(c1.info) > 0:
            print(c1.info)
