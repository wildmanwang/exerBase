# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import socketserver

class ftpServer(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
            except Exception as e:
                print(e)

    def srv_pwd(self, strCmd):
        pass

    def srv_cd(self, strCmd):
        pass

    def srv_dir(self, strCmd):
        pass

    def srv_put(self, strCmd):
        pass

    def srv_get(self, strCmd):
        pass
