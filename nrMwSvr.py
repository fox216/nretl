#!/usr/bin/env python
#
# IoT Binary senor data ETL
#

import sys, json, os
import SocketServer
import binascii
import array
import struct

class SendToSerGateway():
	# Sends output to nodered serial handler
	def __init__(self):
		self.HOST = pi07.emb.net
		self.PORT = 9500


	def 


class MsgHandler(SocketServer.BaseRequestHandler):
	'''
	MsgHandler sevice listens on port 9050 for nodered msgs.
	handler processes both JSON and RAW binary input. 
	- Json messages are proccesed as commands from nodered http 
 	- RAW messages are procceed by commands from serial gateway.
	'''

	def handle(self):
		'''
		Generic handler for JSON & RAW Binary
		'''

		self.data = self.request.recv(1024).strip()
		#print "{} wrote:".format(self.client_address[0])
		## Dump data as ascii values
		socket_data = self.data
		
		try:
			'''
			Attempt to process message as JSON data 
			'''
			json_data = json.loads(socket_data)
			#DEBUG
			print json_data
		except:
			pass

		try:
			'''
			Attempt to process message as RAW Binary
			'''
			# Get mote header Bytes 1-3
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
			
			if mote_payload_type == 10:

				MILLIS_COUNT = struct.unpack('<L', hex_map.decode('hex'))[0]

				# Format Node:Length:Type:Millis:Hex Payload
				print "{0}:{1}:{2}:{3}:{4}".format(
					mote_addr, 
					mote_payload_length, 
					mote_payload_type,
					MILLIS_COUNT,
					hex_map
					)
			if mote_payload_type == 20:
				# Raw Message Format -> 00200f142abe00b9000000984100003f434b
				# Payload Only -> 2abe00b9000000984100003f434b

				'''
				C-Struct
				typedef struct { 
					// MESSAGE TYPE = 20
					// Size = 14 
					// Add collection message data types for node red parsing
					byte				bt;		//[1] Byte			
					int 				si;		//[2] Signed Int
					unsigned int 		ui;		//[2] Unsigned Int
					float 				fp; 	//[4] Float
					double				db; 	//[4] double
					char				sc;		//[1] Single character 
				} _ReportMsg;
				'''

				PAYLOAD = struct.unpack('<BhHffc', hex_map.decode('hex'))
				'''
				Note: Struct returns a tuple of values for conversion
				Test Values
				o_ReportMsg.bt = 42;
				o_ReportMsg.si = runCount;
				o_ReportMsg.ui = runCount - 5;
				o_ReportMsg.fp = runCount / 10;
				o_ReportMsg.db = runCount / runCount + runCount;
				o_ReportMsg.sc = 'K';
				
				** Conversion Note from 8 bit controller
				AVR Type 	Python Struct Type
				--------	-------------------
				byte 		B (unsigned char)
				int 		h (short)
				u_int 		H (unsigned short)
				float 		f (float)
				double 		f (float)
				char 		c (char)

				'''

				

				# Format Node:Length:Type:bt,si,ui,fp,db,sc:Hex Payload
				print "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}:{8}:{9}".format(
					mote_addr, 
					mote_payload_length, 
					mote_payload_type,
					PAYLOAD[0],
					PAYLOAD[1],
					PAYLOAD[2],
					PAYLOAD[3],
					PAYLOAD[4],
					PAYLOAD[5],
					hex_map
					)
		except:
			pass

		
		

if __name__ == '__main__':
	# Run server
	try:
		HOST,PORT = "0.0.0.0", 9999
		server = SocketServer.TCPServer((HOST,PORT), MsgHandler)
		server.allow_reuse_address = True
		server.serve_forever()
	except:
		print "Got call to shutdown "
		server.server_close()
		server.shutdown()


