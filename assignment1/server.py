import socket
import sys
from thread import *

HOST = ''
PORT = 8889

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'socket created'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Bind socket to local host
try:
		s.bind((HOST, PORT))
except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Error message : ' + str(msg[1])
		sys.exit()
print 'Socket bind complete'

#socket listening
s.listen(10)
print 'socket is listening'

#function for handling connections
def clientthread(conn):
	conn.send('Welcome to the server. Type something and hit enter\n')

	while True:
		data = conn.recv(1024)
		reply = 'OK .. ' + data
		if not data:
			break

		conn.sendall(reply)
	conn.close()
			
while 1:
	conn, addr = s.accept()
	print 'connected with ' + addr[0] + ':' + str(addr[1]) 			

	start_new_thread(clientthread, (conn,))
s.close()