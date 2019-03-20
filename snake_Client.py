import socket
import pygame
import random
from pygame.locals import * # import all variables needed

class Snake(pygame.sprite.Sprite): # Snake is extended class of Sprite
    def __init__(self):
        super(Snake, self).__init__() # comment needed
        self.head_image = pygame.image.load('graphics/head.png').convert() # load method returns surface object from given path, convert creates a copy that will render quicker
        self.part_image = pygame.image.load('graphics/part.png').convert() # universal part image for this snake   

        self.ms = 10 # movespeed
        self.id = 0 # player ID, should be either 1/2/3/4, 0 by default -- not set

    def blit_body(self, new_body_str, wind):
        new_body = []
        for pair in new_body_str.split('|'):
            new_body.append(pair.split(','))
        print(new_body)
        #e.g. new_body = [['30', '40'], ['20', '10'], ['30', '90']]
        # rect = rectangular coordinates = ((x,y),(width,height))
        head_rect = self.head_image.get_rect()               
        # gets the rect object from the surface
        head_rect.x = int(new_body[0][0])            
        head_rect.y = int(new_body[0][1])

        # checking for head going out of bounds, to change graphic color
        if head_rect.x <= 0 or (head_rect.x+10) > 500 or head_rect.y <= 0 or (head_rect.y+10) > 500 or new_body[0] in new_body[1:]:
            self.edit_graphics('graphics/part2.png','graphics/part2.png')
            
        wind.blit(self.head_image, head_rect)
        # blitting parts
        for i in range(1, len(new_body)):
            part_rect = self.part_image.get_rect()
            part_rect.x = int(new_body[i][0])
            part_rect.y = int(new_body[i][1])
            wind.blit(self.part_image, part_rect)
            # to blit the snake itself onto the window provided

           
    # setter, getters for id
    def set_id(self, new_id):
        self.id = new_id

    
    def get_id(self):
        return self.id


    def edit_graphics(self, new_head_img, new_part_img): # setter to edit images for the sprites for head and part any time
        self.head_image = pygame.image.load(new_head_img).convert()
        self.part_image = pygame.image.load(new_part_img).convert()



def main():
    pygame.init()
    
    win_dimensions = (500, 500) # tuple 500 pixels x 500 pixels (width, height)
    window = pygame.display.set_mode(win_dimensions) # surface created for main window
    
    pygame.display.set_caption("snake") # set main display's caption to "snake1"

    bg = pygame.image.load('graphics/bg.png')
    # render/blit background image on window
    window.blit(bg, (0, 0)) # block information transfer, render surface onto another surface
    
    server_ip = "127.0.0.1"  # host server's ip
    server_port = 5004  # server's port

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_ip, server_port))  # TCP - from the client side, we CONNECT to the given host and port
    # our client's port is decided arbitrarily by our computer e.g. 5192
    
    client_id = int(client_sock.recv(1024).decode('utf-8')) # recv from server

    snake = Snake()
    snake.set_id(client_id)
    

    direction = 3
    running = True
    while running:
        pygame.time.delay(400) # 100 miliseconds

        # pygame.event.get(), returns a list of all current I/O events occuring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # every event has a type, and also event.key == pygame.K_ESCAPE so event has key pressed if I/O event
            # event checking if the red button X is pressed/clicked 
                running = False # loop breaks
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys_dict = pygame.key.get_pressed()  # gets current dictonary of keyboard presses where each key e.g. pygame.K_LEFT has a value of 1 or 0 (pressed/not pressed)

        # reverse direction is not allowed, if the snake1 is going east (3), then direction cannot be changed to west (4)    
        if keys_dict[pygame.K_LEFT] == True and direction != 3:
            direction = 4
        elif keys_dict[pygame.K_UP] == True and direction != 2:
            direction = 1      
        elif keys_dict[pygame.K_DOWN] == True and direction != 1:
            direction = 2  
        elif keys_dict[pygame.K_RIGHT] == True and direction != 4:
            direction = 3


        client_sock.send(str(direction).encode('utf-8')) # direction sent

        list_of_bodystr = client_sock.recv(1024).decode('utf-8')  # client's socket recieves data from the server script running on the server it connected to


        updated_body_lists = list_of_bodystr.split('-') #"1,2|3,3|4,3-"

        print("Recieved data from server: ", updated_body_lists)

        window.blit(bg, (0, 0))
        for i in range(len(updated_body_lists)):
            if updated_body_lists[i] != "":
                snake.blit_body(updated_body_lists[i], window)

        pygame.display.update()  # update screen

    client_sock.close()  # close connection if user quitted
    pygame.quit()

if __name__ == '__main__':
    main()
