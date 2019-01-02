# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket

client = socket.socket()
client.connect(("localhost", 1212))
while True:
    sInput = input("What you say:").strip()
    if len(sInput) == 0:
        continue
    elif sInput == "exit":
        break
    client.send(sInput.encode("utf-8"))
    data = client.recv(1024)
    print("recv:", data.decode("utf-8"))
client.close()
