# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socket

def handle_request(client):
    buf = client.recv(1024)
    client.send(bytes("HTTP/1.1 200 OK\r\n\r\n", encoding="utf-8"))
    f = open(r"static\page1.html", "rb")
    data = f.read()
    f.close()
    client.send(data)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 8000))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()

if __name__ == "__main__":
    main()
