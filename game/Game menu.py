import pygame
import os
import subprocess

from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)


pygame.init()


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
            try:
                process = subprocess.Popen(['python', 'level 1.py'])
                process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                print("Timeout reached. Process terminated.")
                exit()
        
    
    elif button_rect1.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(hand)
        screen.blit(options_clicked, (button_x2, button_y2))
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
