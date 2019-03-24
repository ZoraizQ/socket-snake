import socket
import random
from _thread import *
import threading
import sys, getopt
import copy
import time

width = 800
height = 608
gridfactor = 16 # cell size

status_all = "alive"
gameInProgress = False

list_of_bodylists = []
food_list = []
score_list = []

last_survivor = 0

#bodylist = [[33,11],[12,23],[34,12]]
#bodystr = "33,11|12,23|34,12"
def str_from_list(given_list):
    new_str = ""
    for pair in given_list:
        new_str += ("%i,%i|" % (pair[0],pair[1]))
    return new_str[:-1]

def survivorsCount():
    num = 0
    last = 0
    for i in range(len(list_of_bodylists)): #checking if the body list is empty
        if list_of_bodylists[i] != []:
            last = i+1
            num += 1

    if num == 1:
        global last_survivor
        last_survivor = last
    return num

class Snake_Tracker():
    def __init__(self, given_id): # range for random generation
        self.ms = gridfactor # movespeed
        self.id = given_id # player ID, should be either 1/2/3/4, 0 by default -- not set

         # range for spawning zones calculated according to width, height
        head_x = random.randint(int(96/gridfactor), int((width-96)/gridfactor))*gridfactor #lower bound inclusive, upper bound inclusive, in multiples of gridfactor (cell size)
        head_y = random.randint(int(96/gridfactor), int((height-96)/gridfactor))*gridfactor
        print("Snake %i's head spawned at coordinates (%i, %i)" % (self.id, head_x, head_y))

        self.body = [[head_x,head_y]]
        for i in range(2):
            self.body.append([head_x-gridfactor*i,head_y])
        
        
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
        
        # when snake head collides with one of the foods
        for i in range(len(food_list)):
            if self.body[0] == food_list[i]:
                new_tail = copy.deepcopy(self.body[len(self.body)-1]) 
                if direction == 3:
                    new_tail[0] -= self.ms
                elif direction == 4:
                    new_tail[0] += self.ms
                elif direction == 2:
                    new_tail[1] -= self.ms
                elif direction == 1:
                    new_tail[1] += self.ms
                self.body.append(new_tail)
                del food_list[i]
                score_list[self.id-1] += 15
                break

        # checking for head going out of bounds
        if self.body[0][0] < 0 or self.body[0][0] >= width or self.body[0][1] < 0 or self.body[0][1] >= height:
            return False
        elif self.body[0] in self.body[1:]: #your head collides with your own body part
            return False
            
        #or head in list_of_bodylists:
        for i in range(len(list_of_bodylists)):
            snakei_list = list_of_bodylists[i]
            if snakei_list == []: # ignore empty lists
                continue
            if self.body[0] == snakei_list[0]:
                print("Head-on collision")
                list_of_bodylists[i] = []
                global last_survivor
                last_survivor = 0
                return False
            elif self.body[0] in snakei_list[1:] and self.id != i+1:
                print("%i's head collided with %i's part" % (self.id, i+1))
                score_list[i] += 100
                return False
        
        return True

    # setter, getters for id
    def set_id(self, new_id):
        self.id = new_id

    def get_id(self):
        return self.id

    def get_body(self): #[[30,40],[20,10],[30,90]]
        return self.body


def player_thread(client_sock, client_id): 
    # north = 1, south = 2, east = 3, west = 4
    direction = random.randint(1,4) # randomly generate initial direction for now 
    client_sock.send(str(direction).encode('utf-8')) # STRING function .encode(format), BYTESTRING function .decode(format) 
    snake_tracker = Snake_Tracker(client_id)

    #snake_tracker.update_body(direction) # update list once
    list_of_bodylists[client_id-1] = copy.deepcopy(snake_tracker.get_body())

    snake_alive = True
    gamestep = 1
    global status_all
    global gameInProgress
    while status_all == "alive":
        if gameInProgress and gamestep % random.randint(30,60) == 0:
            foodx = random.randint(0,int(width/gridfactor))*gridfactor
            foody = random.randint(0,int(height/gridfactor))*gridfactor
            food_list.append([foodx,foody])
        
        directionbstr = client_sock.recv(4)
        if not directionbstr:
            list_of_bodylists[client_id-1] = []
            break
        
        direction = int(directionbstr.decode('utf-8'))
        ''' 4 - buffer size (data to recv from client socket at a time)
        We also had to decode it since data is encoded over a network into bytestrings
        We decode the bytestring recieved into text string with utf-8 encoding. '''

        if snake_alive and gameInProgress:
            if snake_tracker.update_body(direction) == False:
                print("Snake %i has collided and died." % snake_tracker.get_id())
                list_of_bodylists[client_id-1] = []
                snake_alive = False
            else:
                list_of_bodylists[client_id-1] = copy.deepcopy(snake_tracker.get_body()) # [[30,40],[20,10],[30,90]]
        
        list_of_bodylists_str = ""
        for b in list_of_bodylists: #[[[30,70],[30,80],[30,90]], [[30,70],[30,80],[30,90]]]
            list_of_bodylists_str += str_from_list(b) + '-'
        list_of_bodylists_str = list_of_bodylists_str[:-1]

        packet = str_from_list(food_list) + "%" + list_of_bodylists_str + "%" + str(score_list[client_id-1])
        
        if survivorsCount() == 0 and gameInProgress:
            status_all = "dead" #if list_of_bodylists is empty (survivorsCount), status_all changed from "alive" to "dead"
            winner = -1
            global last_survivor
            if last_survivor == 0:
                print("No one wins.")
            else:
                #score_list[last_survivor-1] += 250 # last survivor gets a bonus of 250
                winner = last_survivor

            #highest_score = score_list.index(max(score_list)) + 1
            packet += "%"+str(winner)

            final_scores_str = ""
            for s in score_list:
                final_scores_str += str(s) + '|'
            packet += "%" + final_scores_str[:-1]
            packet = str(sys.getsizeof(packet)) + "%" + packet
            client_sock.sendall(packet.encode('utf-8')) # send list of body list strings in string form, encoded to bytestring
            break
        

        packet = str(sys.getsizeof(packet)) + "%" + packet
        client_sock.send(packet.encode('utf-8')) # send list of body list strings in string form, encoded to bytestring
        
        gamestep += 1
        time.sleep(0.02) #delay on server end

    print("Client %i is disconnecting." % client_id)
    client_sock.close()

# server script
def main(argv):
    host_ip, port = argv[0], int(argv[1]) # use all available IP addresses (both localhost and any public addresses configured)
    # pick an arbitrary port, outide range 1024 (the reserved space) and does not clash with any other programs

    # socket(socket_family, socket_type)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET-> ipv4 & SOCK_STREAM->TCP
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # comment needed here
    server_sock.bind((host_ip, port))  # bind our socket to this machine - pass tuple for (host,port)

    print ("Number of players that will be playing: " + argv[2])
    requiredPlayers = int(argv[2]) # listen for the required number of connections at a time
    print("Server listening for connections...")

    client_id = 1
    numPlayers = len(score_list)  # len(score_list) gives us total number of players currently (0 appended for each)

    threads = []
    global gameInProgress
    while True:
        try:
            server_sock.listen(requiredPlayers) # server will not start listening also until this parameter has been given
            client_sock, client_addr = server_sock.accept()  # accepting connection from the server socket gives us both the client's socket and the source address
            print("Connection from %s" % str(client_addr))

            score_list.append(0)
            numPlayers = len(score_list) # score list updated each time, since 0 added 
            
            if gameInProgress:
                score_list.pop()
                client_sock.close()
                continue

            list_of_bodylists.append([])
            print("Player %i has connected. Waiting for %i more player(s)." % (client_id, requiredPlayers-len(score_list)))
            if numPlayers == requiredPlayers:
                print("Player requirement met. Game beginning.")
                gameInProgress = True
            # Start a new thread and return its identifier 
            t = start_new_thread(player_thread, (client_sock, client_id))
            threads.append(t)
            client_id += 1
        except:
            print("Quitting server.")
            quit()

    for t in threads:
        t.join()
    print("Quitting server.")    
    server_sock.close()
   
if __name__ == '__main__':
    main(sys.argv[1:])
