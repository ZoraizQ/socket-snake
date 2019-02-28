import random
import curses  # https://docs.python.org/2/library/curses.html

scrn = curses.initscr()  # intialise screen
curses.curs_set(0)  # set cursor to 0 so it does not show up on the screen

# get max y and x (height and width)
screenheight, screenwidth = scrn.getmaxyx()

# create a new window using the height and width we got,
# starting from the top left corner of the screen (0, 0)
wind = curses.newwin(screenheight, screenwidth, 0, 0)

wind.keypad(True)  # so it accepts keypad input

wind.timeout(100)  # screen refresh rate = timeout every 100 ms

snk_x = screenwidth / 4  # snake part x coordinates
snk_y = screenheight / 2  # snake part y coordinates - beside the screen by 2

'''
create initial snake body parts, as part of a 2d matrix 
(list of coordinate lists for every parts), where [0] is the head coordinates, 
and last part is the tail.
'''
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# food place at the center (sh/2, sw/2)
food = [int(screenheight/2), int(screenwidth/2)]
print (food)
# add food to screen using window function addch(y coordinate, x coordinate, )
wind.addch(food[0], food[1], curses.ACS_PI)  # ACS_PI = alternate character set - letter PI

# initially the key pressed is right-arrow so our snake goes right
key = curses.KEY_RIGHT

while True:  # GAME LOOP - INFINITE
    next_key = wind.getch()  # get next character input from user
    if next_key == -1:  # -1? nothing pressed, key remains same
        key = key
    else:  # some key pressed, make current key the key pressed
        key = next_key

    '''
    note snake[0][0] is the head x and [0][1] is the head y,
    now if the head x or y reaches the borders
    (0, screenwidth) or (screenheight, 0) OR when head coordinates intersect/become
    the same as any other part coordinates snake[1:]
    then it is game over = kill/end window, quit
    '''
    if (snake[0][1] in [0, screenwidth]) or (snake[0][0] in [screenheight, 0]) or (snake[0] in snake[1:]):
        curses.endwin()
        quit()

    # new head of the snake = the old head will be our starting point
    new_head = [snake[0][0], snake[0][1]]

    '''
    calculate new head coordinates by incrementing respective coordinates to the
    old head's starting position
    if the snake was headed in the south/down direction then move new_head up by 1 
    unit by incrementing its y coordinate
    '''
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # since snake is a list, we insert at its start 0, our new head using .insert(position, value)
    snake.insert(0, new_head)

    # if the snake head snake[0] has the same coordinates as food
    if snake[0] == food:
        food = None  # food removed, time to select new food position randomly
        while food is None:
            # random coordinates within screen borders generated for the new food
            new_food = [
                random.randint(1, screenheight - 1),
                # in the range 1 (since 0 is the upper horizontal border coord y)
                # to screenheight-1 (since screenheight is the lower horizontal border y coord)
                random.randint(1, screenwidth - 1)
            ]
            # we also have to ensure the new food is not generated at the coordinates of
            # any of the snake's body parts, if it is we make food = None again, so the loop executes again
            # to generate a new random position for the food
            if new_food not in snake:  # unique, valid random position calculated
                food = new_food
            else:
                food = None
        # add alternate character set char - pi to y,x coordinates of food
        wind.addch(food[0], food[1], curses.ACS_PI)
    else:  # snake head did not encounter food
        # pop last element (part coordinates) from the snake list to get the tail
        tail = snake.pop()
        # tail part is removed from the list, and now we even remove the tail character
        # from the window by replacing it with space ' '
        wind.addch(int(tail[0]), int(tail[1]), ' ')

    wind.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)



