#!/usr/bin/env python
#
# IoT Binary senor data ETL
#

import sys, json, os
import SocketServer
from ctypes import *




class TCPHandler(SocketServer.BaseRequestHandler):
	# TCD Socket handler
	def handle(self):
		self.data = self.request.recv(1024).strip()

		print "{} wrote:".format(self.client_address[0])

		#print self.data
		socket_data = self.data
		hex_map = map(ord, socket_data)
		print hex_map

		

if __name__ == '__main__':
	# Run server
	HOST,PORT = "0.0.0.0", 9999
	server = SocketServer.TCPServer((HOST,PORT), TCPHandler)
	server.serve_forever()

