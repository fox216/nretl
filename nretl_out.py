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

	HOST,PORT = "10.20.42.238", 9000
	''' Turn on zone 1 for 5 Min '''
	#in_byte_data = [0,64,3,20,0,5]
	''' Run Front Program Run zones 1-4'''
	in_byte_data = [0,64,3,30,70,34]
	''' Run All Program Run zones 1-9'''
	#in_byte_data = [0,64,3,30,65,34]
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
	


