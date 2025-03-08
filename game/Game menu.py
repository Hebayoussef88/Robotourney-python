import pygame
import os
import subprocess
import sys

from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init()

screen_height = 672
screen_width  = 1200

screen = pygame.display.set_mode((screen_width, screen_height))

def options():
    global screen
    running1 = True
    while running1:
        back_op = pygame.image.load("pixil-frame-0.png")
        back_op = pygame.transform.scale(back_op, (screen_width, screen_height))
        screen.blit(back_op, (0, 0))

        options_title = pygame.image.load("options title.png")
        screen.blit(options_title, (15, 5))

        fullscreen_button = pygame.image.load("Fullscreen.png")
        fullscreen_button = pygame.transform.scale(fullscreen_button, (350, 100))
        screen.blit(fullscreen_button, (8, 125))
        fullscreen_pos = (8, 125)
        fullscreen_rect = pygame.Rect(fullscreen_pos, fullscreen_button.get_size())
        if fullscreen_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(hand)
            if pygame.mouse.get_pressed()[0]:  
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        else:
            pygame.mouse.set_cursor()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running1 = False

        pygame.display.flip()


def play():
    import pygame
    import os
    import sys
    import cv2

    from pygame.display import get_window_size
    from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

    global screen

    pygame.init()

    window_size = (1200, 672)


    intro = "chronochills intro video.mp4"
    audio_path = "chronochills intro.mp3"
    cap = cv2.VideoCapture(intro)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    if not cap.isOpened():
        print("Error: Cannot open video file.")
        sys.exit()




    pygame.display.set_caption("level 1")
    logo = pygame.image.load("chronochills logo.png")
    logo = pygame.transform.scale(logo, (550, 300))
    pygame.display.set_icon(logo)

    running = True

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the video's FPS
    delay = int(1000 / fps)  # Calculate the frame delay

    while running:
        pygame.mouse.set_cursor()
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Or ROTATE_90_COUNTERCLOCKWISE if needed
        frame = cv2.flip(frame, 0)
    
        # Convert frame (BGR to RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Convert frame to Pygame Surface
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.scale(frame_surface, window_size)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                cap.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        pygame.time.delay(delay)

    pygame.mixer.music.stop()
    cap.release()
    pygame.quit()

screen_height = 672
screen_width  = 1200
button_x1 = 520
button_y1 = 300
button_x2 = 520
button_y2 = 425
button_x3 = 520
button_y3 = 550
button_width = 100
button_height = 200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("chronochills")
logo = pygame.image.load("chronochills logo.png")
logo = pygame.transform.scale(logo, (550, 300))
pygame.display.set_icon(logo)
screen1 = pygame.image.load("hack1 .jpg")
scale = pygame.transform.scale(screen1, (800, 1200))
Font1 = pygame.font.Font('Double Pixel-7 400.ttf', 160)
play_unclicked = pygame.image.load("play_unclicked.png")
play_unclicked = pygame.transform.scale(play_unclicked, (150, 90))
options_unclicked = pygame.image.load("options_unclicked.png")
options_unclicked = pygame.transform.scale(options_unclicked, (150, 90))
quit_unclicked = pygame.image.load("quit_unclicked.png")
quit_unclicked = pygame.transform.scale(quit_unclicked, (150, 90))
play_clicked = pygame.image.load("play_clicked.png")
play_clicked = pygame.transform.scale(play_clicked, (150, 90))
options_clicked = pygame.image.load("options_clicked.png")
options_clicked = pygame.transform.scale(options_clicked, (150, 90))
quit_clicked = pygame.image.load("quit_clicked.png")
quit_clicked = pygame.transform.scale(quit_clicked, (150, 90))
hand = pygame.SYSTEM_CURSOR_HAND
    

running = True

mouse_pressed = pygame.mouse.get_pressed()


while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    my_text = Font1.render("chronochills", True, (255, 255, 255))
    button_pos = (520, 300)
    button_pos1 = (520, 425)
    button_pos2 = (520, 550)
    button_rect = pygame.Rect(button_pos, play_unclicked.get_size())
    button_rect1 = pygame.Rect(button_pos1, options_unclicked.get_size())
    button_rect2 = pygame.Rect(button_pos2, quit_unclicked.get_size())


    
    screen.blit(screen1, (0,0))
    screen.blit(logo, (318, 1))
    screen.blit(play_unclicked, (button_x1, button_y1))
    screen.blit(options_unclicked, (button_x2, button_y2))
    screen.blit(quit_unclicked, (button_x3, button_y3))
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(hand)
        screen.blit(play_clicked, (button_x1, button_y1))
        if pygame.mouse.get_pressed()[0]:
            play()
            
            
        
    
    elif button_rect1.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(hand)
        screen.blit(options_clicked, (button_x2, button_y2))
        if pygame.mouse.get_pressed()[0]:
            options()
    elif button_rect2.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(hand)
        screen.blit(quit_clicked, (button_x3, button_y3))
        if pygame.mouse.get_pressed()[0]:
            quit()


    else:
        pygame.mouse.set_cursor()
        screen.blit(play_unclicked, (button_x1, button_y1))
        screen.blit(options_unclicked, (button_x2, button_y2))
        screen.blit(quit_unclicked, (button_x3, button_y3))


    pygame.display.update()

pygame.quit()
