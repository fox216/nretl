#!/usr/bin/env python
#
# IoT Binary senor data ETL
#

import sys, json, os
import SocketServer
from ctypes import *
import binascii



class TCPHandler(SocketServer.BaseRequestHandler):
	# TCD Socket handler
	def handle(self):
		self.data = self.request.recv(1024).strip()

		#print "{} wrote:".format(self.client_address[0])

		#print self.data

		
		## Dump data as ascii values
		socket_data = self.data
		ascii_map = map(ord, socket_data)
		print ascii_map

		## Dump data as hex values
		#socket_data = self.data
		#hex_map = hex(map(ord, socket_data))
		#print hex_map

		#hex_data = socket_data.replace(' ','').decode('hex')
		#print hex_data
		for x in socket_data:
			hex_data_element = binascii.b2a_hex(x)
			print hex_data_element


		

if __name__ == '__main__':
	# Run server
	HOST,PORT = "0.0.0.0", 9999
	server = SocketServer.TCPServer((HOST,PORT), TCPHandler)
	server.serve_forever()

