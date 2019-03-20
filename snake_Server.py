import socket
import pygame
import random
from pygame.locals import * # import all variables needed


class Snake_Tracker():
    def __init__(self):
        super(Snake_Tracker, self).__init__() # comment needed        
        head_x = random.randint(6,49)*10 #lower bound inclusive, upper bound inclusive (0-490) in multiples of 10 (cell size)
        head_y = random.randint(6,49)*10
        
        self.body = []
        self.body.append([head_x,head_y])

        for i in range(1,5):
            self.body.append([head_x-10*i,head_y])
        
        self.ms = 10 # movespeed
        self.id = 0 # player ID, should be either 1/2/3/4, 0 by default -- not set
        #self.length = 3


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
        if self.body[0][0] <= 0 or (self.body[0][0]+10) > 500 or self.body[0][1] <= 0 or (self.body[0][1]+10) > 500:
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
        new_str = ""
        for pair in self.body:
            new_str += ("%i,%i|" % (pair[0],pair[1]))
        return new_str[:-1]

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
    direction = random.randint(1,4) # randomly generate initial direction for now 
    snake_tracker1 = Snake_Tracker()
    snake_tracker1.set_id(1)

    running = True
    while running:
        direction = int(client_sock.recv(1024).decode('utf-8')) #converting string into int

        if snake_tracker1.update_body(direction) == False:
            print("Snake %i has collided." % snake_tracker1.get_id())
            running = False
        '''
        1024 - buffer size (data to recv from client socket at a time)
        We also had to decode it since data is encoded over a network into bytestrings
        We decode the bytestring recieved into text string with utf-8 encoding.
        '''
        bodylist1 = snake_tracker1.get_body_str() # "30,40|20,10|30,90"

        client_sock.send(bodylist1.encode('utf-8')) # send data in a packet to a the clients socket

    client_sock.close()

if __name__ == '__main__':
    main()
