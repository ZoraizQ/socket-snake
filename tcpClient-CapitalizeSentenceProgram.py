import socket

# client needs to be in a separate file so we can run both of them in the same time
def main():
	host_ip = '127.0.0.1'  # host server's ip
	port = 5000  # server's port

	client_sock = socket.socket()
	client_sock.connect((host_ip, port))  # TCP - from the client side, we CONNECT to the given host and port
	# our client's port is decided arbitrarily by our computer e.g. 5192

	message = input("-> ")
	while message != 'q':  # if user enters 'q' (for quit) key terminate the program by exiting the while
		# SENDTO(data, tuple) - from the client side
		client_sock.send(message.encode('utf-8')) 	# SEND(data)
		data_recieved = client_sock.recv(1024).decode('utf-8')  # client's socket recieves data from the server script running on the server it connected to

		print("Recieved from server " + data_recieved)
		message = input("-> ")

	client_sock.close()  # close connection if user quitted

if __name__ == '__main__':
	main()
