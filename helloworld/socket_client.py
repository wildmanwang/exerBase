# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket

client = socket.socket()
sServer = "localhost"
client.connect((sServer, 1212))
while True:
    dataSend = input(">>>:").strip()
    if len(dataSend) == 0:
        continue
    elif dataSend == "exit":
        break
    client.send(dataSend.encode("utf-8"))
    dataRecv = client.recv(1024)
    client.send("收到数据".encode("utf-8"))     # 自动响应，防止粘包
    iRecv = 0
    sRecv = b""
    while iRecv < int(dataRecv.decode()):
        sTmp = client.recv(1024)
        sRecv += sTmp
        print(type(sTmp))
        print(sTmp.decode())
        iRecv += len(sTmp.decode())
    print(sRecv.decode("utf-8"))

client.close()
