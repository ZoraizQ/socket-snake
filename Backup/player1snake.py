import pygame
import random
from pygame.locals import * # import all variables needed

'''
Python Player 1 Snake

- Snake Position (List) / Sprite Group, tail simulated
- Handle collisions with other sprites
- Apply threads so that n snakes can play
- libpng warning: bKGD: invalid
'''

class Snake(pygame.sprite.Sprite): # Snake is extended class of Sprite
    def __init__(self):
        super(Snake, self).__init__() # comment needed
        self.head_image = pygame.image.load('graphics/head.png').convert() # load method returns surface object from given path, convert creates a copy that will render quicker
        self.part_image = pygame.image.load('graphics/part.png').convert() # universal part image for this snake
        
        # initially randomise the sprite rect's x,y coordinates  
        head_rect = self.head_image.get_rect() # gets the rect object from the surface
        head_rect.x = random.randint(3,49)*10 #lower bound inclusive, upper bound inclusive (0-490) in multiples of 10 (cell size)
        head_rect.y = random.randint(3,49)*10
        
        part1_rect = self.part_image.get_rect()
        part1_rect.x = head_rect.x - 10
        part1_rect.y = head_rect.y

        part2_rect = self.part_image.get_rect()
        part2_rect.x = head_rect.x - 20
        part2_rect.y = head_rect.y

        self.body = [head_rect, part1_rect, part2_rect] # initially length of snake is 3

        self.ms = 10 # movespeed
        self.id = 0 # player ID, should be either 1/2/3/4, 0 by default -- not set
        self.length = 3


    # bool return type, false if updating was not possible (snake1 head killed)
    def update_rect(self, direction):
        '''
        #pygame coordinate sys - topleft (0,0) and bottomright (width, height)
        up = -vel, down = +vel, left = -vel, right = +vel
        '''
        prev_part_x = 0
        prev_part_y = 0
        # updating parts
        for i in range (1, len(self.body)):  # we could have also used self.length -- the member variable
            if i == 1:
                prev_part_x = self.body[i].x
                prev_part_y = self.body[i].y
                self.body[i].move_ip(self.body[0].x-self.body[i].x, self.body[0].y-self.body[i].y) # rect.move_ip(x initial - x_final, y_initial - y_final) #relatively
            else:
                self.body[i].move_ip(prev_part_x-self.body[i].x, prev_part_y-self.body[i].y)
        
        # updating head
        if direction == 4:
            self.body[0].move_ip(-self.ms, 0) # rect.move_ip(x relative, y relative)
            # move_ip() - because we want to move the existing Rect without making a copy.
        elif direction == 1:
            self.body[0].move_ip(0, -self.ms)
        elif direction == 2:
            self.body[0].move_ip(0, self.ms)
        elif direction == 3:
            self.body[0].move_ip(self.ms, 0)
        
        # checking for head going out of bounds of map
        if self.body[0].left <= 0 or self.body[0].right > 500 or self.body[0].top <= 0 or self.body[0].bottom > 500:
            self.kill() # kill sprite, remove pointer to it, so python's garbage collector removes it from memory
            return False
        
        return True

    # setter, getters for id
    def set_id(self, new_id):
        self.id = new_id

    
    def get_id(self):
        return self.id


    def edit_graphics(self, new_head_img, new_part_img): # setter to edit images for the sprites for head and part any time
        self.head_image = pygame.image.load(new_head_img).convert()
        self.part_image = pygame.image.load(new_part_img).convert()

    # to blit the snake itself onto the window provided
    def draw_self(self, win):
        win.blit(self.head_image, self.body[0])
        for i in range (1, len(self.body)):  # we could have also used self.length -- the member variable
            win.blit(self.part_image, self.body[i])


def main():
    # initialise all functions
    pygame.init()

    win_dimensions = (500, 500) # tuple 500 pixels x 500 pixels (width, height)
    window = pygame.display.set_mode(win_dimensions) # surface created for main window

    pygame.display.set_caption("snake1") # set main display's caption to "snake1"

    bg = pygame.image.load('graphics/bg.png')

    # north = 1, south = 2, east = 3, west = 4
    direction = random.randint(1,4) # randomly generate initial direction for now

    snake1 = Snake() # Snake object constructed
    snake1.set_id(1)

    print("Ready?")
    pygame.time.delay(500)
    print("Begin!")
    running = True

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

        # reverse direction is not allowed, if the snake1 is going east (3), then direction cannot be changed to west (4)    
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
        
        if snake1.update_rect(direction) == False:
            print("Snake %i has died." % snake1.get_id())
            snake1.edit_graphics('graphics/part2.png', 'graphics/part2.png')
            running = False

        # blit the snake1 head image at the snake1 head's rect
        snake1.draw_self(window)

        pygame.display.update()  # update screen
        
    print("Quitting the game.")
    pygame.quit() # terminates game  


if __name__ == '__main__': # execute main first
    main()