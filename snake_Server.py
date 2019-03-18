import socket
import pygame
import random
from pygame.locals import * # import all variables needed

# server script
def main():
	host_ip = '127.0.0.1' # loop-back address
	port = 5004  # pick an arbitrary port, outide range 1024 (the reserved space) 
	# and does not clash with any other programs

	# socket(socket_family, socket_type)
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET-> ipv4 & SOCK_STREAM->TCP
	server_sock.bind((host_ip, port))  # bind our socket to this machine - pass tuple for (host,port)

	server_sock.listen(1) #listen for 1 connections at a time
	print("Server listening for connections...")

	# now we need to accept the connection
	client_sock, client_addr = server_sock.accept()  # accepting connection from the server socket gives us both the client's socket 
	# and the source address of the socket recieved
	print("Connection from %s" % str(client_addr))
	
	# north = 1, south = 2, east = 3, west = 4
	#direction = random.randint(1,4) # randomly generate initial direction for now
	
	while True:
		data = client_sock.recv(1024).decode('utf-8')
		'''
		1024 - buffer size (data to recv from client socket at a time)
		We also had to decode it since data is encoded over a network into bytestrings
		We decode the bytestring recieved into text string with utf-8 encoding.
		'''
		if not data:
			print("No command received from %s." % str(client_addr))
			break

		print(data)
		bodylist1 = "30 40,20 10,30 90"
	
		client_sock.send(bodylist1.encode('utf-8')) # send data in a packet to a the clients socket

	client_sock.close()

if __name__ == '__main__':
	main()
