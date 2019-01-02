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
        data = conn.recv(1024)
        if not data:
            print("addr:[{addr}] is lost.".format(addr=addr))
            break
        print("recv:", data.decode("utf-8"))
        myData = "哦哦，" + data.decode("utf-8")
        conn.send(myData.encode("utf-8"))

server.close()
