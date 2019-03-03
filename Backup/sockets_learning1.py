'''
server has generally port 80 open, used to transfer data between websites on the server/clients
lower number ports - specific ports
higher number - general purpose (security issues though)
'''
import socket  # part of your standard library
import os
import time

# get socket function in socket module, socket.AF_INET for IPv4 traffic, SOCK_STREAM for TCP connection, SOCK_DGRAM for UDP connection 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# <socket.socket fd=400, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
# <socket address, address family, type of socket, proto>
# print(s)

# generally to communicate with a server use a socket
server = "pythonprogramming.net"  # domain name, but IP address can also be used

# resolve DN to IP address for host server
server_ip = socket.gethostbyname(server)

# what port do you want to communicate with your server
port = 80  # HTTP, act like a browser

# HTTP get request string
request = "GET / HTTP/1.1\nHost: " + server + "\n\n"

s.connect((server, 80))  # connect to server of DN given at given port 
s.send(request.encode())  # python3 vs python2, encode string to byte-string in p3

result = s.recv(4096)  # 4096 - size of buffer, how much data we're gonna be downloading
# print(result)  # begins with b - bytecode request format, so when you recieve data you have to decode it and while sending encode it
'''
b'HTTP/1.1 301 Moved Permanently\r\n
Date: Sat, 23 Feb 2019 12:32:04 GMT\r\n
Server: Apache/2.4.10 (Ubuntu)\r\n
Location: https://pythonprogramming.net/\r\n
Content-Length: 325\r\n
Content-Type: text/html; charset=iso-8859-1\r\n\r\n
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n
<html><head>\n<title>301 Moved Permanently</title>\n</head>
<body>\n<h1>Moved Permanently</h1>\n<p>The document has moved <a href="https://pythonprogramming.net/">here</a>.</p>\n
<hr>\n<address>Apache/2.4.10 (Ubuntu) Server at pythonprogramming.net Port 80</address>\n</body></html>\n'
'''

# buffering in action, delay then pastes all data instantly
while (len(result) > 0): # while result has some bytes (its length > 0), data is being recieved
    print(result)
    result = s.recv(1024)

# LEARNING OS FUNCTIONS
curDir = os.getcwd()  # get current working directory
print(curDir)

os.mkdir('newDir')  # make directory of name 'newDir' in the script folder
time.sleep(2)  # delay 2 seconds

os.rename('newDir','newDir2')  # find folder in script directory of name 'newDir' and rename it to 'newDir2'
time.sleep(2)

os.rmdir('newDir2')  # find and delete folder called 'newDir2' in script directory