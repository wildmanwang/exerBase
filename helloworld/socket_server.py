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
        dataRecv = conn.recv(1024)
        dataRecv = dataRecv.decode("utf-8")
        if not dataRecv:
            print("addr:[{addr}] is lost.".format(addr=addr))
            break
        sResult = os.popen(dataRecv).read()
        print(sResult)
        iLen = len(sResult)
        sResult = sResult.encode("utf-8")
        conn.send(str(iLen).encode("utf-8"))
        conn.send(sResult)

server.close()
