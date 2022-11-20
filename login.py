import pygame as pg


def login():
    pg.init()
    FONT = pg.font.Font(None, 42)
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    user_name = []

    done = False

    while not done:
        username_surface = FONT.render(
            "".join(user_name), True, (200, 200, 150))
        # Events regarding quit and keyboard
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    pg.quit()
                    return "".join(user_name)
                else:
                    # dlete character when the user clicks backspace
                    if event.key == pg.K_BACKSPACE:
                        user_name = user_name[:-1]
                        username_surface = FONT.render(
                            "".join(user_name), True, (200, 200, 150))
                        size = username_surface.get_size()
                        screen.fill(pg.Color("black"),
                                    (100+size[0], 50, 100, 30))
                    # Append space when the user clicks space
                    elif event.key == pg.K_SPACE:
                        user_name.append(" ")
                    else:
                        # Append the entered character
                        user_name.append(event.unicode)
        # Rendering enter my user name on screen
        my_font = pg.font.SysFont(None, 50)
        text_surface = my_font.render("enter user name", True, (255, 0, 0))
        screen.blit(text_surface, (0, 10))
        # Rendering the username enterd by user
        screen.blit(username_surface, (100, 50))

        pg.display.flip()
        clock.tick(30)
