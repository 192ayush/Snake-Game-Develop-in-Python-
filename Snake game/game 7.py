import pygame
import time
import random

pygame.init()
pygame.font.init()  # Initialize font module

# Load background music
pygame.mixer.music.load("D:\Subway_Surfers_Theme_V2-646327.mp3")
pygame.mixer.music.play(-1)

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)  # Reverting snake color back to its original color
green = (0, 255, 0)
blue = (50, 153, 213)
orange = (255, 165, 0)
purple = (128, 0, 128)
pink = (255, 192, 203)  # Changing background color from pink to green
bg_color = (0, 128, 0)  # New background color (green)
blink_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255)]

# Display
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Load wallpapers
start_wallpaper = pygame.image.load("D:\close-up-snake-natural-habitat.jpg")
end_wallpaper = pygame.image.load("D:\cobra-snake-game-character-vbu0895huxqiek5p.jpg")
start_wallpaper = pygame.transform.scale(start_wallpaper, (dis_width, dis_height))
end_wallpaper = pygame.transform.scale(end_wallpaper, (dis_width, dis_height))

# Clock
clock = pygame.time.Clock()

# Snake and food size
snake_block = 20
snake_speed = 10

# Font Style
font_style = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 20)
script_font = pygame.font.Font(pygame.font.match_font('calibri'), 20)

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def message(msg, color, y_displace=0, x_pos=None, y_pos=None):
    mesg = font_style.render(msg, True, color)
    if x_pos is None or y_pos is None:
        dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])
    else:
        dis.blit(mesg, [x_pos - mesg.get_width() / 2, y_pos - mesg.get_height() / 2 + y_displace])

def pause_game():
    paused = True
    message("Paused. Press C to continue or Q to quit.", white, 10)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))

    small_text = pygame.font.SysFont(None, 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    dis.blit(text_surf, text_rect)

def start_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False

        dis.blit(start_wallpaper, (0, 0))
        message("Welcome to My Snake Game Everyone ", green, -100)
        message("Press Enter to start the game", red, 300)
        pygame.display.update()

def end_screen(score, high_score):
    outro = True
    while outro:
        dis.blit(end_wallpaper, (0,0))
        message("You lost! Press C to play again or Q to quit.", red)
        message("Your Score: " + str(score), black, 30, dis_width / 2, dis_height / 2 + 50)
        message("High Score: " + str(high_score), black, 60, dis_width / 2, dis_height / 2 + 100)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    return True  # Return True to restart the game loop

    return False

def gameLoop():
    start_screen()

    while True:  # Loop until the game is exited
        game_over = False
        game_close = False

        # Initial snake position
        x1 = dis_width / 2
        y1 = dis_height / 2

        # Movement changes
        x1_change = 0
        y1_change = 0

        # Snake body
        snake_List = []
        Length_of_snake = 1

        # Food position
        foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
        foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
        blink = False
        blink_count = 0

        # Score
        score = 0
        high_score = 0  # Initialize high score

        while not game_over:

            while game_close:
                # If the end screen returns True, restart the game loop
                if end_screen(score, high_score):
                    gameLoop()  # Restart the game loop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = snake_block
                        x1_change = 0
                    elif event.key == pygame.K_p:
                        pause_game()

            # Border crossing
            if x1 >= dis_width:
                x1 = 0
            elif x1 < 0:
                x1 = dis_width - snake_block
            elif y1 >= dis_height:
                y1 = 0
            elif y1 < 0:
                y1 = dis_height - snake_block

            x1 += x1_change
            y1 += y1_change
            dis.fill(bg_color)

            if blink:
                pygame.draw.circle(dis, random.choice(blink_colors), (int(foodx + snake_block / 2), int(foody + snake_block / 2)), int(snake_block / 2))
                blink_count += 1
                if blink_count == 5:
                    blink = False
                    blink_count = 0
            else:
                pygame.draw.circle(dis, green, (int(foodx + snake_block / 2), int(foody + snake_block / 2)), int(snake_block / 2))

            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_List.append(snake_head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_head:
                    game_close = True

            # Snake drawing
            for idx, segment in enumerate(snake_List):
                color = black if idx % 2 == 0 else purple
                pygame.draw.rect(dis, color, [segment[0], segment[1], snake_block, snake_block])

            # Score display
            score_text = script_font.render("Score: " + str(score), True, black)
            dis.blit(score_text, [10, 10])

            # AYUSH font style
            ayush_text = script_font.render("Developed by AYUSH", True, white)
            dis.blit(ayush_text, [dis_width - 200, dis_height - 30])

            pygame.display.update()

            # Update high score
            if score > high_score:
                high_score = score

            # Food eating
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
                foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
                Length_of_snake += 1
                score += 10  # Increment score when food is eaten
                blink = True

            clock.tick(snake_speed)

        # Display end screen after game over
        if not end_screen(score, high_score):
            break  # Exit the game loop if the player chooses to quit

    pygame.quit()
    quit()

gameLoop()
