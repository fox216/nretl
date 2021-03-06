#!/usr/bin/env python
#
# IoT Binary senor data ETL
#

import sys, json, os
import socket
import binascii
import array
import struct
import time
		
		

if __name__ == '__main__':
	# Run server
	

	HOST,PORT = "pi07.emb.net", 9050
	#HOST,PORT = "10.20.42.91", 9050
	#HOST,PORT = "10.20.42.113", 9000 # pi09
	''' Turn on zone 1 for 5 Min '''
	#in_byte_data = [0,50,3,20,0,21]
	#in_byte_data = [0,50,3,20,1,10]
	#in_byte_data = [0,50,3,20,2,10] 	# ok relay 2
	#in_byte_data = [0,50,3,20,3,10]  	# ok relay 3
	
	#in_byte_data = [0,50,3,20,4,21]	# ok Relay 8
	#in_byte_data = [0,50,3,20,5,10]
	#in_byte_data = [0,50,3,20,6,5]
	#in_byte_data = [0,50,3,20,7,10]	
	#in_byte_data = [0,50,3,20,8,10]
	#in_byte_data = [0,50,3,20,9,21]
	
	''' Run Front Program Run zones 1-4'''
	#in_byte_data = [0,50,3,30,67,20]
	
	''' Run All Program Run zones 1-9 for 2 Min Each'''
	#in_byte_data = [0,50,3,30,65,5]

	''' Run All Program Run Back zones '''
	in_byte_data = [0,50,3,30,66,20]
	
	# convert int to hex format
	data_raw = ''.join('{:02x}'.format(x) for x in in_byte_data)
	# Format data stream to hex
	data_hex = binascii.unhexlify(data_raw)
	# Setup Socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect 
	sock.connect((HOST,PORT))
	sock.sendall(data_hex)

	# Close Connection
	time.sleep(1)
	sock.close()		
	


