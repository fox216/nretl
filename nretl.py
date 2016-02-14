#!/usr/bin/env python
#
# IoT Binary senor data ETL
#

import sys, json, os
import SocketServer
from ctypes import *
import binascii
import array
import struct

class msg_10 (Structure):
	_fields_ = []


class TCPHandler(SocketServer.BaseRequestHandler):
	# TCD Socket handler

	def handle(self):
		self.data = self.request.recv(1024).strip()
		#print "{} wrote:".format(self.client_address[0])
		## Dump data as ascii values
		socket_data = self.data
		#print "Read Header ..."
		try:
			mote_header = map(ord, socket_data[:-3])

			if mote_header[0] == 0:
				#print "Valid Message"
				mote_addr = int(mote_header[1])
				mote_payload_length = int(mote_header[2]) 
				mote_payload_type = int(mote_header[3]) 				
					
			'''
			Convert BIG ENDIAN Data to Little ENDIAN 

			Data:

			Fields 	-> 	Mote:Length:Type:Converted_Long:Raw_Data
			Data 	-> 	44:5:10:394950000:70758a17
			
			Example 1
			Payload: 70758a17 <- transmission & parsing is correct	

			MILLIS_COUNT = struct.unpack('<L', '70758a17'.decode('hex'))[0] = 394950000

			Example 2

			Full: 0020050a15cd5b07
			Payload: 15cd5b07 <- transmission & parsing is correct	
			
			MILLIS_COUNT = struct.unpack('<L', '15cd5b07'.decode('hex'))[0] = 123456789

			'''
			hex_map = ''.join([binascii.b2a_hex(x) for x in socket_data[4:]])
			#print "Payload: {0}".format(hex_map)
			

			MILLIS_COUNT = struct.unpack('<L', hex_map.decode('hex'))[0]

			# Format Node:Length:Type:Millis:Hex Payload
			print "{0}:{1}:{2}:{3}:{4}".format(
				mote_addr, 
				mote_payload_length, 
				mote_payload_type,
				MILLIS_COUNT,
				hex_map
				)
		except:
			pass
		
		

if __name__ == '__main__':
	# Run server
	try:
		HOST,PORT = "0.0.0.0", 9999
		server = SocketServer.TCPServer((HOST,PORT), TCPHandler)
		server.allow_reuse_address = True
		server.serve_forever()
	except:
		print "Got call to shutdown "
		server.server_close()
		server.shutdown()


