#!/usr/bin/env python
#
# IoT Binary senor data ETL
#

import sys, json, os
import SocketServer




class TCPHandler(SocketServer.BaseRequestHandler):
	# TCD Socket handler
	def handle(self):
	self.data = self.request.recv(1024).strip()
	
	print "{} wrote:".format(self.client_address[0])
	
	print self.data












if __name__ == '__main__':
	# Run server
	HOST,PORT = "0.0.0.0", 9999
	server = SocketServer.TCPServer((HOST,PORT), TCPHandler)
	server.serve_forever()

