# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket
sock = socket.socket()
#sock.connect(('120.78.197.182',51102))
sock.connect(('localhost',6969))
flag = False
while not flag:
    data = input(">>:").strip()
    if data == "b":flag = True
    if len(data) == 0:continue
    sock.send(data.encode())
    recv_data = sock.recv(8096)
    print("recv:",recv_data.decode())

sock.close()
