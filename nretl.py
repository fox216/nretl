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
		'''
		long hand
		for x in socket_data:
			hex_data_element = binascii.b2a_hex(x)
			print hex_data_element
		'''
		# rewrite as list comprehension
		hex_map = ''.join([binascii.b2a_hex(x) for x in socket_data])
		print hex_map

		print "Hex Format...."
		'''
		# Long hand
		for y in socket_data:
			hex_data_element = hex(ord(y))
			print hex_data_element
		'''
		# rewrite as list comprehension
		hex_map_format = ''.join([hex(ord(y)) for y in socket_data]) 
		print hex_map_format

		# Decode binary string into hex array. 
		# Parse array to decode moteino data
		# Test Message Type 10 on all Sensors

		hex_map_array = [hex(ord(y)) for y in socket_data]
		print hex_map_array
		try:
			mote_addr = int(hex_map_array[1])
			mote_payload_length = int(hex_map_array[2]) 
			mote_payload_type = int(hex_map_array[3]) 

			print "Recieved msg from {0}\n - Length: {1}\n - Type: {2}".format(mote_addr, mote_payload_length, mote_payload_type)
		except:
			pass 
		
		

if __name__ == '__main__':
	# Run server
	HOST,PORT = "0.0.0.0", 9999
	server = SocketServer.TCPServer((HOST,PORT), TCPHandler)
	server.serve_forever()

