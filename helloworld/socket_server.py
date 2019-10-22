# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socketserver
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        '''try内的代码就是要实现的功能，目前是实现小写转大写，可以自定义，
        try是在客户端结束时不报错
        '''
        try:
             while True:
                self.data = self.request.recv(1024).strip()
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                self.request.sendall(self.data.upper())
        except ConnectionResetError as e:
            print(e)
if __name__ == "__main__":
    HOST, PORT = "localhost", 6969
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
