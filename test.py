#!/usr/bin/python 


import sys, json, os
import SocketServer
import threading

class jsonHandler(SocketServer.BaseRequestHandler):
	def handler(self):
		print "JSON"
		print self.request.recv(1024).strip()

class serialHandler(SocketServer.BaseRequestHandler):
	def handler(self):
		print "Serial"
		print  self.request.recv(1024).strip()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class ForkTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
	HOST = "0.0.0.0"
	S1_PORT = 9000
	S2_PORT = 9050
	server_S1 = ThreadedTCPServer((HOST, S1_PORT), jsonHandler)
	server_S2 = ThreadedTCPServer((HOST, S2_PORT), serialHandler)
	server_S1_thread = threading.Thread(target=server_S1.serve_forever)
	server_S2_thread = threading.Thread(target=server_S2.serve_forever)
	server_S1_thread.setDaemon(True)
	server_S2_thread.setDaemon(True)
	 
	server_S1_thread.start()
	server_S2_thread.start()
