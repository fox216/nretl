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

		#print self.data

		
		## Dump data as ascii values
		socket_data = self.data
		#ascii_map = map(ord, socket_data)
		#print ascii_map

		## Dump data as hex values
		#socket_data = self.data
		#hex_map = hex(map(ord, socket_data))
		#print hex_map

		#hex_data =
		#socket_data.replace(' ','').decode('hex')
		#print hex_data
		'''
		long hand
		for x in socket_data:
			hex_data_element = binascii.b2a_hex(x)
			print hex_data_element
		
		# rewrite as list comprehension
		hex_map = ''.join([binascii.b2a_hex(x) for x in socket_data])
		print hex_map

		print "Hex Format...."
		
		# Long hand
		for y in socket_data:
			hex_data_element = hex(ord(y))
			print hex_data_element
		
		# rewrite as list comprehension
		hex_map_format = ''.join([hex(ord(y)) for y in socket_data]) 
		print hex_map_format

		# Decode binary string into hex array. 
		# Parse array to decode moteino data
		# Test Message Type 10 on all Sensors

		hex_map_array = [hex(ord(y)) for y in socket_data]
		
		hex_map_array = map(ord, socket_data)
		print hex_map_array

		try:

			mote_addr = int(hex_map_array[1])
			mote_payload_length = int(hex_map_array[2]) 
			mote_payload_type = int(hex_map_array[3]) 

			print "Recieved msg from {0}\n - Length: {1}\n - Type: {2}".format(mote_addr, mote_payload_length, mote_payload_type)
		except:
			pass 
		
		
		Convert BIG ENDIAN Hex to LONG
	
		msg_long = ''.join(hex_map_array[4:])
		
		print msg_long
		msg_long = '0x{0}'.format(msg_long)
		print msg_long
		#long_data = struct.unpack('>L', msg_long)	
		#print long_data
		'''
		#print "Read Header ..."
		try:
			mote_header = map(ord, socket_data[:-3])

			if mote_header[0] == 0:
				#print "Valid Message"
				mote_addr = int(mote_header[1])
				mote_payload_length = int(mote_header[2]) 
				mote_payload_type = int(mote_header[3]) 

		

				#if mote_payload_type == 10:
					#print "Process Payload type 10"
					#hex_map = ''.join([binascii.b2a_hex(x) for x in socket_data[4:]])
					#conv_ascii = binascii.unhexlify(hex_map)
					#end_conv = array.array('h', conv_ascii)
					#end_conv.byteswap()
					
					#print "Little Endian"
					#s = struct.Struct('<L')
					#mills_count = (s.unpack_from(end_conv))[0]
					#print ' - {0}'.format(mills_count)

					
					#print "Big Endian"
					#s = struct.Struct('>L')
					#print(s.unpack_from(end_conv))[0]
				
					
			'''
			Notes: Conversion process is mangling values. 
			
			Full: 0020050a15cd5b07
			
			Payload: 15cd5b07 <- transmission & parsing is correct	
			
			MILLIS_COUNT = struct.unpack('<L', '15cd5b07'.decode('hex'))[0] = 123456789

			32:5:10:1527190989 <- Not whatever this is....
			'''


			
			#hex_map = ''.join([binascii.b2a_hex(x) for x in socket_data])
			#print "Full: {0}".format(hex_map)
			hex_map = ''.join([binascii.b2a_hex(x) for x in socket_data[4:]])
			#print "Payload: {0}".format(hex_map)
			
			# Basic Convert from Little Endian .....
			#
			#START HERE

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


