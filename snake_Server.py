import socket
import random
from _thread import *
import threading

list_of_bodystr = ["",""]

def str_from_bodylist(given_list):
    new_str = ""
    for pair in given_list:
        new_str += ("%i,%i|" % (pair[0],pair[1]))
    return new_str[:-1]

def list_from_bodystr(given_list):
    new_body = []
    for pair in new_body_str.split('|'):
        new_body.append(pair.split(','))
    return new_body

class Snake_Tracker():
    def __init__(self):
        super(Snake_Tracker, self).__init__() # comment needed        
        self.ms = 10 # movespeed
        self.id = 0 # player ID, should be either 1/2/3/4, 0 by default -- not set

        head_x = random.randint(6,49)*10 #lower bound inclusive, upper bound inclusive (0-490) in multiples of 10 (cell size)
        head_y = random.randint(6,49)*10
        
        self.body = [[head_x,head_y]]
        for i in range(4):
            self.body.append([head_x-10*i,head_y])
        
        
    # bool return type, false if updating was not possible (snake1 head killed)
    def update_body(self, direction):
        '''
        #pygame coordinate sys - topleft (0,0) and bottomright (width, height)
        up = -self.ms, down = +self.ms, left = -self.ms, right = +self.ms
        '''
        prev_head_x = self.body[0][0]
        prev_head_y = self.body[0][1]
        prev_part_x = 0
        prev_part_y = 0
        temp_x = 0
        temp_y = 0
       
        # updating parts
        for i in range (1, len(self.body)):  # we could have also used self.length -- the member variable
            if i == 1:
                prev_part_x = self.body[i][0]
                prev_part_y = self.body[i][1]
                self.body[i][0] = prev_head_x
                self.body[i][1] = prev_head_y
            else:
                temp_x = self.body[i][0]
                temp_y = self.body[i][1]
                self.body[i][0] = prev_part_x
                self.body[i][1] = prev_part_y
                prev_part_x = temp_x 
                prev_part_y = temp_y
                
        # updating head
        if direction == 4:
            self.body[0][0] -= self.ms
        elif direction == 1:
            self.body[0][1] -= self.ms
        elif direction == 2:
            self.body[0][1] += self.ms
        elif direction == 3:
            self.body[0][0] += self.ms
        
        # checking for head going out of bounds
        if self.body[0][0] < 0 or (self.body[0][0]+10) > 500 or self.body[0][1] < 0 or (self.body[0][1]+10) > 500:
            return False
        
        if self.body[0] in self.body[1:]: #your head collides with your own body part
            return False
        '''
        other_snake_body = [[30,40], [40,60], [50,20]]
        
        if self.body[0] == other_snake_body[0]: #your head collides with another head
            # both die
            return False
        elif self.body[0] in other_snake_body: #your head collides another snake's body part other than the head
            # my snake dies
            return False #COLLISION
        '''
        return True

    # setter, getters for id
    def set_id(self, new_id):
        self.id = new_id


    def get_id(self):
        return self.id


    def get_body_str(self): #30,40|20,10|30,90
        return str_from_bodylist(self.body)

def player_thread(client_sock, client_id): 
    # north = 1, south = 2, east = 3, west = 4
    direction = random.randint(1,4) # randomly generate initial direction for now 
    snake_tracker = Snake_Tracker()
    
    #client_sock.send(str(client_id).encode('utf-8'))
    snake_tracker.set_id(client_id)
    
    running = True
    while running:
        direction = int(client_sock.recv(1024).decode('utf-8')) #converting string into int
        ''' 1024 - buffer size (data to recv from client socket at a time)
        We also had to decode it since data is encoded over a network into bytestrings
        We decode the bytestring recieved into text string with utf-8 encoding. '''

        if snake_tracker.update_body(direction) == False:
            print("Snake %i has collided." % snake_tracker.get_id())
            list_of_bodystr[snake_tracker.get_id()-1] = ""
            running = False
        else:
            list_of_bodystr[client_id-1] = snake_tracker.get_body_str() # "30,40|20,10|30,90"
        
        print(list_of_bodystr)

        new_str = ""
        for b_str in list_of_bodystr: #["30,40|20,10|30,90", "30,40|20,10|30,90"]
            new_str += b_str + '-'
        new_str = new_str[:-1] 
     
        client_sock.send(new_str.encode('utf-8')) # send data in a packet to a the clients socket

    client_sock.close()

# server script
def main():
    host_ip = "127.0.0.1" # loop-back address
    port = 5004  # pick an arbitrary port, outide range 1024 (the reserved space) 
    # and does not clash with any other programs

    # socket(socket_family, socket_type)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET-> ipv4 & SOCK_STREAM->TCP
    server_sock.bind((host_ip, port))  # bind our socket to this machine - pass tuple for (host,port)

    maxPlayers = 2 #listen for 2 connections at a time
    server_sock.listen(maxPlayers) 
    print("Server listening for connections...")

    client_id = 1

    while True:
        # now we need to accept the connection
        client_sock, client_addr = server_sock.accept()  # accepting connection from the server socket gives us both the client's socket 
        # and the source address of the socket recieved
        print("Connection from %s" % str(client_addr))

        #print_lock.acquire()

        # Start a new thread and return its identifier 
        start_new_thread(player_thread, (client_sock, client_id))
        client_id += 1
    server_sock.close()
   
if __name__ == '__main__':
    main()
