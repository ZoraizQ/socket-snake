import mysql.connector
import socket
import pygame
import random
import sys
from pygame.locals import *  # import all variables needed
from login import login
width = 800
height = 608
gridfactor = 16
part_graphics_list = ['graphics/part1.png', 'graphics/part2.png',
                      'graphics/part3.png', 'graphics/part4.png']

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="name_of_database"
)
mycursor = mydb.cursor()


def bounce_down(wind, textsurf, bg):  # comment
    grav = 6
    pace = 20
    x = int(width/2)-gridfactor*12
    y = int(height/2)-gridfactor*2
    bounce = width/(gridfactor/2)
    maxim_list = [y, y-bounce, y, y-bounce/4, y]
    minim = 0

    for m in maxim_list:
        maxim = int(m)
        g = grav  # down by default
        if minim > maxim:  # up
            g = -grav
        for i in range(minim, maxim, g):  # down
            wind.blit(bg, (0, 0))
            wind.blit(textsurf, (x, i))
            pygame.display.update()
            pygame.time.delay(pace)
        minim = maxim


def isStrListEmpty(given_list):
    empty = True
    for s in given_list:
        if s != "":
            empty = False

    return empty


def recv_packet(c_sock):
    testdata = c_sock.recv(1)
    if not testdata:
        return ""
    # pick the first 1 byte (normal size of chars)
    packet_size = testdata.decode('utf-8')
    # print(packet_size)
    while "%" not in packet_size:
        # recieve 1 byte every time
        packet_size += c_sock.recv(1).decode('utf-8')
        # print(packet_size)

    packet_size = int(packet_size[:-1])
    packet = c_sock.recv(packet_size).decode('utf-8')
    return packet


class Snake_Printer():  # Snake_Printer class
    def __init__(self):
        # universal part image for this snake
        self.part_image = pygame.image.load(
            'graphics/part1.png').convert_alpha()
        # universal food image for this snake
        self.food_image = pygame.image.load(
            'graphics/food.png').convert_alpha()
        self.ms = gridfactor  # movespeed

    def blit_body(self, new_body_str, wind):
        new_body = []
        for pair in new_body_str.split('|'):
            new_body.append([int(coord) for coord in pair.split(',')])
        #e.g. new_body = [['30', '40'], ['20', '10'], ['30', '90']]
        # rect = rectangular coordinates = ((x,y),(width,height))
        head_rect = self.part_image.get_rect()
        # gets the rect object from the surface
        head_rect.x = new_body[0][0]
        head_rect.y = new_body[0][1]

        wind.blit(self.part_image, head_rect)
        # blitting parts
        for i in range(1, len(new_body)):
            part_rect = self.part_image.get_rect()
            part_rect.x = new_body[i][0]
            part_rect.y = new_body[i][1]
            wind.blit(self.part_image, part_rect)
            # to blit the snake itself onto the window provided

    def blit_foodlist_str(self, foodlist_str, wind):  # comment
        foodlist = []
        for pair in foodlist_str.split('|'):
            foodlist.append(pair.split(','))

        for food in foodlist:
            food_rect = self.food_image.get_rect()
            food_rect.x = int(food[0])
            food_rect.y = int(food[1])
            wind.blit(self.food_image, food_rect)

    # setter to edit images for the sprites for head and part any time
    def edit_graphics(self, new_part_img):
        self.part_image = pygame.image.load(new_part_img).convert_alpha()


def main(argv, name):
    # host server's ip and server's port
    server_ip, server_port = argv[0], int(argv[1])
    if server_ip == "":
        server_ip = "127.0.0.1"

    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting to connect to %s on port %i." %
              (server_ip, server_port))
        # TCP - from the client side, we CONNECT to the given host and port
        client_sock.connect((server_ip, server_port))
        # our client's port is decided arbitrarily by our computer e.g. 5192
    except socket.error:  # comment
        print("Unable to connect to the server.")
        quit()

    # initially the direction is recieved from the server
    direction = 0
    try:
        client_sock.send(name.encode("utf-8"))
        directionbstr = client_sock.recv(1)
        if not directionbstr:
            print(
                "Sorry, there may already be a game in progress. \nExiting in 3 seconds.")
            client_sock.shutdown(2)
            client_sock.close()
            pygame.time.wait(3000)
            quit()
    except:
        print("Unable to connect to the server.")
        client_sock.shutdown(2)
        client_sock.close()
        quit()

    print("Initializing the game.")
    pygame.init()
    #pygame.font.SysFont(name, size, bold=False, italic=False)
    font1 = pygame.font.SysFont('calibri', 18, True)  # font object created

    # surface created for main window, with dimensions globally stated
    window = pygame.display.set_mode((width, height))

    # set main display's caption to "snake1"
    pygame.display.set_caption("snake")

    bg = pygame.image.load('graphics/bg.png').convert()
    overlay = pygame.image.load('graphics/bg_overlay.png').convert_alpha()
    # render/blit background image on window
    # block information transfer, render surface onto another surface
    window.blit(bg, (0, 0))

    # bytestring from client buffer decoded to utf-8 string then to int
    direction = int(directionbstr.decode('utf-8'))
    snake = Snake_Printer()  # object of snake_printer() class

    running = True
    packet_score = ""
    packet_segments = []
    while running:
        pygame.time.delay(80)  # delay in miliseconds

        # pygame.event.get(), returns a list of all current I/O events occuring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # every event has a type, and also event.key == pygame.K_ESCAPE so event has key pressed if I/O event
                # event checking if the red button X is pressed/clicked
                print("Forced disconnect. Exiting in 1 second.")
                pygame.time.wait(1000)
                client_sock.shutdown(2)
                client_sock.close()  # close connection if user quitted
                pygame.quit()
                quit()

        # gets current dictonary of keyboard presses where each key e.g. pygame.K_LEFT has a value of 1 or 0 (pressed/not pressed)
        keys_dict = pygame.key.get_pressed()

        # reverse direction is not allowed, if the snake1 is going east (3), then direction cannot be changed to west (4)
        if keys_dict[pygame.K_LEFT] == True and direction != 3:
            direction = 4
        elif keys_dict[pygame.K_UP] == True and direction != 2:
            direction = 1
        elif keys_dict[pygame.K_DOWN] == True and direction != 1:
            direction = 2
        elif keys_dict[pygame.K_RIGHT] == True and direction != 4:
            direction = 3

        client_sock.sendall(str(direction).encode('utf-8'))  # direction sent

        window.blit(bg, (0, 0))

        try:
            # client's socket recieves data from the server script running on the server it connected to
            packet = recv_packet(client_sock)
            if packet == "":
                break
        except socket.error:
            print("Failed to recieve packet.")
            client_sock.shutdown(2)
            client_sock.close()
            quit()

        packet_segments = packet.split('%')
        #print (packet_segments)

        updated_body_lists = packet_segments[1].split('-')  # "1,2|3,3|4,3-"

        if packet_segments[0] != "":
            snake.blit_foodlist_str(packet_segments[0], window)

        for i in range(len(updated_body_lists)):
            if updated_body_lists[i] != "":
                # different color every time until 4 players, the 5th player is assigned the same color as player 1 (index 0 by mod)
                snake.edit_graphics(part_graphics_list[i % 4])
                snake.blit_body(updated_body_lists[i], window)  # comment

        window.blit(overlay, (0, 0))

        if packet_segments[2] != packet_score:  # score updated, only then render it
            packet_score = packet_segments[2]
            # font.render(text, antialias, color, background=None) -> Surface
            text_surface = font1.render(
                'Score: ' + packet_score, True, (255, 255, 255))
        window.blit(text_surface, (8, 8))

        pygame.display.update()  # update screen

        if len(packet_segments) > 3:
            print("Final packet recieved. All snakes are dead.")
            mycursor.execute(
                "INSERT INTO records(name,score) VALUES('"+name+"', '"+packet_score+"');")
            mydb.commit()
            running = False

    if len(packet_segments) <= 3:
        client_sock.send("ACK".encode('utf-8'))
        client_sock.shutdown(2)
        client_sock.close()
        quit()

    winner = packet_segments[3]
    displaystr = 'WINNER: PLAYER ' + winner
    if winner == "-1":
        displaystr = 'THERE IS NO WINNER'

    print(displaystr)
    font2 = pygame.font.SysFont('calibri', gridfactor*3, True)
    text_surface = font2.render(displaystr, True, (255, 255, 255))
    bounce_down(window, text_surface, bg)
    pygame.time.delay(500)
    final_scores = packet_segments[4].split('|')

    window.blit(bg, (0, 0))
    text_surface = font1.render('SCORE LIST', True, (255, 69, 0))
    window.blit(text_surface, (350, 208))
    for i in range(len(final_scores)):
        scorestr = 'Player ' + str(i+1) + ": " + final_scores[i]
        print(scorestr)
        text_surface = font1.render(scorestr, True, (255, 255, 255))
        window.blit(text_surface, (350, 200+(i+1)*(gridfactor*2)))

    pygame.display.update()  # update screen
    client_sock.send("ACK".encode('utf-8'))
    print("Game over. Exiting in 3 seconds.")
    pygame.time.wait(3000)
    client_sock.shutdown(2)  # SHUT_RD, SHUT_WR, SHUT_RDWR --- value 0, 1, 2
    client_sock.close()  # close connection if user quitted
    pygame.quit()


if __name__ == '__main__':
    user_name = login()
    main(sys.argv[1:], user_name)
