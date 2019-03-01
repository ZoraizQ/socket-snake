import socket

def main():
	# in net code, one client pretends to be the server, this script will function the server
	host_ip = '127.0.0.1'  # loop-back address
	port = 5000  # pick an arbitrary port, outide range 1024 (the reserved space) 
	# and does not clash with any other programs

	# socket(socket_family, socket_type)
	server_sock = socket.socket()
	server_sock.bind((host_ip,port))  # bind our socket to this machine - pass tuple for (host,port)

	# listen(no. of connections at a time)
	server_sock.listen(1)  # listen for 1 connection at a time

	# now we need to accept the connection
	client_sock, client_addr = server_sock.accept()  # accepting connection from the server socket gives us both the client's socket and the source address of the socket recieved
	print("Connection from %s" % str(client_addr))

	# now that out server is running and we have a connection
	while True:  # let our server run indefinitely
		data = client_sock.recv(1024).decode('utf-8');  
		'''
		1024 - buffer size (data to recv from client socket at a time)
		We also had to decode it since data is encoded over a network into bytestrings
		We decode the bytestring recieved into text string with utf-8 encoding.
		'''
		if not data:  # if no data is recieved from our client
			break

		print("From connected user: " + data)
		data = data.upper()  # capitalise data recieved
		print("Sending: " + data)
		client_sock.send(data.encode('utf-8'))  # encode data into bytes and send it in a packet to the client's socket

	client_sock.close()  # if we recieved no data (while loop broken), then close connection to client socket

if __name__ == '__main__':
	main()
