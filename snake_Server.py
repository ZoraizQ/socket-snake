import socket
import random
from _thread import *
import threading
import time
import copy

list_of_bodylists = []
#bodylist = [[33,11],[12,23],[34,12]]
#bodystr = "33,11|12,23|34,12"
food_list = []

def str_from_list(given_list):
    new_str = ""
    for pair in given_list:
        new_str += ("%i,%i|" % (pair[0],pair[1]))
    return new_str[:-1]


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
        
        for i in range(len(food_list)):
            if self.body[0] == food_list[i]:
                tail = self.body[len(self.body)-1] 
                new_tail = []  
                if direction == 3:
                    new_tail = [tail[0]-10, tail[1]]
                elif direction == 4:
                    new_tail = [tail[0]-10, tail[1]]
                elif direction == 2:
                    new_tail = [tail[0], tail[1]-10]
                elif direction == 1:
                    new_tail = [tail[0], tail[1]+10]
                self.body.append(new_tail)
                del food_list[i]
                break

        # checking for head going out of bounds
        if self.body[0][0] < 0 or (self.body[0][0]+10) > 500 or self.body[0][1] < 0 or (self.body[0][1]+10) > 500:
            return False
        elif self.body[0] in self.body[1:]: #your head collides with your own body part
            return False
        
        
        #or head in list_of_bodylists:
        for i in range(len(list_of_bodylists)):
            list_of_snakei = list_of_bodylists[i]
            if list_of_snakei == []:
                continue
            if self.body[0] == list_of_snakei[0]:
                #print("collideedd head on")
                list_of_bodylists[i] = ""
                return False
            elif self.body[0] in list_of_snakei[1:]:
                #print("collided with part")
                return False
        
        return True

    # setter, getters for id
    def set_id(self, new_id):
        self.id = new_id


    def get_id(self):
        return self.id

    def get_body(self): #30,40|20,10|30,90
        return self.body

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
            list_of_bodylists[snake_tracker.get_id()-1] = []
            running = False
        else:
            list_of_bodylists[client_id-1] = copy.deepcopy(snake_tracker.get_body()) # "30,40|20,10|30,90"
        
        print(list_of_bodylists)

        list_of_bodylists_str = ""
        for b in list_of_bodylists: #[[[30,70],[30,80],[30,90]], [[30,70],[30,80],[30,90]]]
            list_of_bodylists_str += str_from_list(b) + '-'
        list_of_bodylists_str = list_of_bodylists_str[:-1]

        packet = str_from_list(food_list) + "%" + list_of_bodylists_str
        print(packet)
        client_sock.send(packet.encode('utf-8')) # send list of body list strings in string form, encoded to bytestring

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

        list_of_bodylists.append([])

        foodx = random.randint(1,49)*10
        foody = random.randint(1,49)*10
        food_list.append([foodx,foody])
        #print_lock.acquire()

        # Start a new thread and return its identifier 
        start_new_thread(player_thread, (client_sock, client_id))
        client_id += 1
    server_sock.close()
   
if __name__ == '__main__':
    main()
