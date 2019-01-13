# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket
import os

server = socket.socket()
server.bind(("localhost", 1212))
server.listen()
while True:
    conn, addr = server.accept()
    while True:
        try:
            dataRecv = conn.recv(1024)
        except ConnectionResetError as e:
            print("Err:", e)
            break
        dataRecv = dataRecv.decode("utf-8")
        sResult = os.popen(dataRecv).read()
        print(sResult)
        iLen = len(sResult)
        sResult = sResult.encode("utf-8")
        conn.send(str(iLen).encode("utf-8"))
        conn.recv(1024)                     # 防止粘包
        conn.send(sResult)

server.close()
