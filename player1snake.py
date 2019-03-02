'''
Python Player 1 Snake
'''
import pygame
import random

# initialise all functions
pygame.init()


win_dimensions = (500, 500) # tuple 500 pixels x 500 pixels
# pygame.display.setmode((width,height))
window = pygame.display.set_mode(win_dimensions)

# set caption "snake"
pygame.display.set_caption("snake")

# game variables
#pygame coordinate sys - topleft (0,0) and bottomright (width, height)
x = random.randint(-1,490) #lower bound exlusive, upper bound inclusive (0-490)
y = random.randint(-1,490)
width = 10
height = 10
run = True
vel = 10
player_image = pygame.image.load('hamza.jpg')
bg = pygame.image.load('download.jpg')
'''
north = 1, south = 2, east = 3, west = 4
'''
direction = random.randint(0,4) # randomly generate initial direction for now

while run:
 # alternative in time library - time.sleep(100)
    pygame.time.delay(100) # 100 miliseconds
 
 # pygame.event.get(), returns a list of all current I/O events occuring
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # every event has a type, and also event.key == pygame.K_ESCAPE so event has key pressed if I/O event
        # event checking if the red button X is pressed/clicked 
            run = False # loop breaks
     

    '''
    up = -vel, down = +vel
    left = -vel, right = +vel
    '''
    keys_dict = pygame.key.get_pressed()  # gets current dictonary of keyboard presses where each key e.g. pygame.K_LEFT has a value of 1 or 0 (pressed/not pressed)

     
    if keys_dict[pygame.K_ESCAPE] == True:
        run = False
        continue
    elif keys_dict[pygame.K_LEFT] == True:
        direction = 4
    elif keys_dict[pygame.K_UP] == True:
        direction = 1      
    elif keys_dict[pygame.K_DOWN] == True:        
        direction = 2   
    elif keys_dict[pygame.K_RIGHT] == True:
        direction = 3
        
    if direction == 4:
         x = x - vel
    elif direction == 1:
         y = y - vel
    elif direction == 2:
         y = y + vel
    elif direction == 3:
         x = x + vel
          
    '''
    rect_color = (255,0,0) # R,G,B
    rect = (x, y, width, height) #x coordinate, y coordinate, width, height  
    pygame.draw.rect(window, rect_color, rect)
    # draw a rectangle on window with color and rect dimensions
    '''
    window.blit(player_image, (x, y))
    pygame.display.update()  # update screen
    #window.fill((0,0,0))
    window.blit(bg, (0, 0))
    
    
    
pygame.quit() # terminates game  

#window.fill((0,0,0))




