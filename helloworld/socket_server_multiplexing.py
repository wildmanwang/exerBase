# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import select                       #多路复用select模式
import socket
import queue

server = socket.socket()
server.bind(("localhost", 1212))
server.listen(1000)

server.setblocking(False)

msg_dict = {}                       #记录每个连接待发信息

inputs = [server,]                  #自己也要被监控，server也是一个fd
outputs = []

while True:
    print("Wait for next event...")
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)   #如果没有任何inputs项的数据就绪，程序会阻塞在这里
    for s in readable:              #每个s都是一个socket
        if s is server:             #如果是server数据就绪，表示来了新的连接
            conn, client_addr = server.accept()
            print("New connection from:", client_addr)
            conn.setblocking(False)
            inputs.append(conn)     #把新连接放入多路复用的输入列表
            msg_dict[conn] = queue.Queue()      #自动生成一个空的信息字典项
        else:                       #表示连接发来了数据
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                print("客户端开了", s)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                del msg_dict[s]
            else:
                print("收到来自[%s]的数据：" % s.getpeername()[0], data)
                msg_dict[s].put(data)
                if s not in outputs:    #为了降低耦合度，不在这里发数据，后面统一发
                    outputs.append(s)
    for w in writeable:
        try:
            next_msg = msg_dict[w].get_nowait()
        except queue.Empty:
            print("Client [%s]" % w.getpeername()[0], " queue is empty.")
            outputs.remove(w)
        else:
            print("Send message to [%s]:" % w.getpeername()[0], next_msg)
            w.send(next_msg)
    for e in exceptional:
        print("Handling exception for ", e.getpeername()[0])
        inputs.remove(e)
        if e in outputs:
            outputs.remove(e)
        del msg_dict[e]
