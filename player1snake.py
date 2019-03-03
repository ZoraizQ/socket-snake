'''
Python Player 1 Snake

- Snake Head, Sprite Class
- Snake Position (List) / Sprite Group
'''
import pygame
import random
from pygame.locals import *

# initialise all functions
pygame.init()

win_dimensions = (500, 500) # tuple 500 pixels x 500 pixels (width, height)
window = pygame.display.set_mode(win_dimensions) # surface created for main window

pygame.display.set_caption("snake") # set main display's caption to "snake"

class Snake_Head(pygame.sprite.Sprite): # Snake_Head is extended class of Sprite
    def __init__(self):
        super(Snake_Head, self).__init__() # c
        self.image = pygame.image.load('graphics/part1.png').convert() #load method returns surface object from given path, convert creates a copy that will render quicker
        #self.image.set_colorkey((255, 255, 255), RLEACCEL) # ignores white background (reduces transparency of white to 0) RLEACCEL mode makes modification slower but rendering faster
        self.rect = self.image.get_rect() # gets the rect object from the surface
        # initially randomise the sprite rect's x,y coordinates
        self.rect.x = random.randint(0,490) #lower bound inclusive, upper bound inclusive (0-490)
        self.rect.y = random.randint(0,490)
        self.ms = 10 # movespeed
         
    def update_rect(self, direction):
        '''
        #pygame coordinate sys - topleft (0,0) and bottomright (width, height)
        up = -vel, down = +vel, left = -vel, right = +vel
        '''
        if direction == 4:
            self.rect.move_ip(-self.ms, 0) # rect.move_ip(x relative, y relative)
            # move_ip() - because we want to move the existing Rect without making a copy.
        elif direction == 1:
            self.rect.move_ip(0, -self.ms)
        elif direction == 2:
            self.rect.move_ip(0, self.ms)
        elif direction == 3:
            self.rect.move_ip(self.ms, 0)

        if self.rect.left <= 0 or self.rect.right >= 500 or self.rect.top <= 0 or self.rect.bottom >= 500:
            print("You went out of bounds")
            self.kill()
            quit() # TEMPORARY - quit python program 


bg = pygame.image.load('graphics/bg.png')
running = True

# north = 1, south = 2, east = 3, west = 4
direction = random.randint(1,4) # randomly generate initial direction for now
print(direction)

snake = Snake_Head() # snake_head object constructed



while running:
 # alternative in time library - time.sleep(100)
    pygame.time.delay(100) # 100 miliseconds
 
 # pygame.event.get(), returns a list of all current I/O events occuring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        # every event has a type, and also event.key == pygame.K_ESCAPE so event has key pressed if I/O event
        # event checking if the red button X is pressed/clicked 
            run = False # loop breaks
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                break
            

    keys_dict = pygame.key.get_pressed()  # gets current dictonary of keyboard presses where each key e.g. pygame.K_LEFT has a value of 1 or 0 (pressed/not pressed)

    # reverse direction is not allowed, if the snake is going east (3), then direction cannot be changed to west (4)    
    if keys_dict[pygame.K_LEFT] == True and direction != 3:
        direction = 4
    elif keys_dict[pygame.K_UP] == True and direction != 2:
        direction = 1      
    elif keys_dict[pygame.K_DOWN] == True and direction != 1:        
        direction = 2   
    elif keys_dict[pygame.K_RIGHT] == True and direction != 4:
        direction = 3
    
    
    snake.update_rect(direction)
    
    '''
    rect_color = (255,0,0) # R,G,B
    rect = (x, y, width, height) #x coordinate, y coordinate, width, height  
    pygame.draw.rect(window, rect_color, rect) # draw a rectangle on window with color and rect dimensions
    window.fill((0,0,0))
    '''
    # render/blit background image 500x500 on window
    window.blit(bg, (0, 0))
    # blit the snake head image at the snake head's rect
    window.blit(snake.image, snake.rect) # block information transfer, render surface onto another surface
    pygame.display.update()  # update screen

    
    
pygame.quit() # terminates game  



