import socket

def main():
	host = '127.0.0.1'
	port = 5000

	# by default a socket is TCP so we need to change it to TCP
	# SOCK_DGRAM - type = UDP datagram, SOCK_STREAM for TCP
	# AF_INET as we will pass it a host,port tuple (IPv4 traffic)
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_sock.bind((host,port))

	# no need to listen and then accept a connection

	print("Server Started")
	while True:
		# UDP is connectionless, we need to store the data
		# and the source IP address where it came from
		data_recieved, data_source_addr = server_sock.recvfrom(1024)
		# UDP - RECVFROM(1024) used

		data_recieved = data_recieved.decode('utf-8')

		print("Message from %s" % str(data_source_addr))
		print("Data recieved from connect user: " + data_recieved)

		data_sent = data_recieved.upper()
		print("Sending: " + data_sent)
		# UDP - SENDTO(DATA, ADDR)
		server_sock.sendto(data_sent.encode('utf-8'), data_source_addr)
	server_sock.close()  # still have to close UDP connection

if __name__ == '__main__':
	main()
