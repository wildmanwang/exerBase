# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket

server = socket.socket()
server.bind(("localhost", 1212))
server.listen()
while True:
    conn, addr = server.accept()
    while True:
        dataRecv = conn.recv(1024)
        if not dataRecv:
            print("addr:[{addr}] is lost.".format(addr=addr))
            break
        print("{addr}:{data}".format(addr=addr, data=dataRecv.decode("utf-8")))
        dataSend = "哦哦，" + dataRecv.decode("utf-8")
        print("I said:", dataSend)
        conn.send(dataSend.encode("utf-8"))

server.close()
