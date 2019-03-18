'''
Python Player 1 Snake

- Snake Head, Sprite Class
- Snake Position (List) / Sprite Group
'''
import pygame
import random
from pygame.locals import * # import all variables needed

# initialise all functions
pygame.init()

win_dimensions = (500, 500) # tuple 500 pixels x 500 pixels (width, height)
window = pygame.display.set_mode(win_dimensions) # surface created for main window

pygame.display.set_caption("snake") # set main display's caption to "snake"

class Snake_Head(pygame.sprite.Sprite): # Snake_Head is extended class of Sprite
    def __init__(self):
        super(Snake_Head, self).__init__() # c
        self.image_head = pygame.image.load('graphics/part.png').convert() #load method returns surface object from given path, convert creates a copy that will render quicker
        #self.image.set_colorkey((255, 255, 255), RLEACCEL) # ignores white background (reduces transparency of white to 0) RLEACCEL mode makes modification slower but rendering faster, but we do not need this since png sprites used
        self.rect = self.image_head.get_rect() # gets the rect object from the surface
        # initially randomise the sprite rect's x,y coordinates
        self.rect.x = random.randint(0,49)*10 #lower bound inclusive, upper bound inclusive (0-490) in multiples of 10 (cell size)
        self.rect.y = random.randint(0,49)*10
        self.ms = 10 # movespeed
        self.id = 0 # player ID, should be either 1/2/3/4

    # bool return type, false if updating was not possible (snake head killed)
    def update_rect(self, direction):
        '''
        #pygame coordinate sys - topleft (0,0) and bottomright (width, height)
        up = -vel, down = +vel, left = -vel, right = +vel
        '''
        prev_head_x = self.rect.x
        prev_head_y = self.rect.y
        #print("Previous head: (%i,%i)" % (prev_head_x, prev_head_y))
        if direction == 4:
            self.rect.move_ip(-self.ms, 0) # rect.move_ip(x relative, y relative)
            # move_ip() - because we want to move the existing Rect without making a copy.
        elif direction == 1:
            self.rect.move_ip(0, -self.ms)
        elif direction == 2:
            self.rect.move_ip(0, self.ms)
        elif direction == 3:
            self.rect.move_ip(self.ms, 0)
            
        if self.rect.left < 0 or self.rect.right > 500 or self.rect.top < 0 or self.rect.bottom > 500:
            self.kill()
            return False
        
        return True



bg = pygame.image.load('graphics/bg.png')
running = True

# north = 1, south = 2, east = 3, west = 4
direction = random.randint(1,4) # randomly generate initial direction for now

snake = Snake_Head() # snake_head object constructed

print("Ready?")
pygame.time.delay(500)
print(3)
pygame.time.delay(200)
print(2)
pygame.time.delay(200)
print(1)
pygame.time.delay(200)
print("Begin!")


while running:
 # alternative in time library - time.sleep(100)
    pygame.time.delay(100) # 100 miliseconds
 
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

    # reverse direction is not allowed, if the snake is going east (3), then direction cannot be changed to west (4)    
    if keys_dict[pygame.K_LEFT] == True and direction != 3:
        direction = 4
    elif keys_dict[pygame.K_UP] == True and direction != 2:
        direction = 1      
    elif keys_dict[pygame.K_DOWN] == True and direction != 1:        
        direction = 2   
    elif keys_dict[pygame.K_RIGHT] == True and direction != 4:
        direction = 3
    
    # render/blit background image on window
    window.blit(bg, (0, 0)) # block information transfer, render surface onto another surface
    
    if snake.update_rect(direction) == False:
        print("Snake %i has died." % snake.id)
        running = False

    # blit the snake head image at the snake head's rect
    window.blit(snake.image_head, snake.rect)
   
    pygame.display.update()  # update screen
    
print("Quitting the game.")
pygame.quit() # terminates game  



