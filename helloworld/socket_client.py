# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket

client = socket.socket()
sServer = "localhost"
client.connect((sServer, 1212))
while True:
    dataSend = input("I said:").strip()
    if len(dataSend) == 0:
        continue
    elif dataSend == "exit":
        break
    client.send(dataSend.encode("utf-8"))
    dataRecv = client.recv(1024)
    print("{addr}:{data}".format(addr=sServer, data=dataRecv.decode("utf-8")))
client.close()
