import pygame
import os
from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init()

screen_height = 672
screen_width  = 1200
button_x1 = 470
button_y1 = 200
button_x2 = 470
button_y2 = 350
button_x3 = 470
button_y3 = 500
button_width = 100
button_height = 200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("future chronochills")
screen1 = pygame.image.load("hack1 .jpg")
scale = pygame.transform.scale(screen1, (800, 1200))
Font1 = pygame.font.Font('Double Pixel-7 400.ttf', 135)
play_unclicked = pygame.image.load("play_unclicked.png").convert_alpha()
play_unclicked = pygame.transform.scale(play_unclicked, (250, 130))
options_unclicked = pygame.image.load("options_unclicked.png").convert_alpha()
options_unclicked = pygame.transform.scale(options_unclicked, (250, 130))
quit_unclicked = pygame.image.load("quit_unclicked.png").convert_alpha()
quit_unclicked = pygame.transform.scale(quit_unclicked, (250, 130))
play_clicked = pygame.image.load("play_clicked.png").convert_alpha()
options_clicked = pygame.image.load("options_clicked.png").convert_alpha()
quit_clicked = pygame.image.load("quit_clicked.png").convert_alpha()
hand = pygame.SYSTEM_CURSOR_HAND
    

running = True


while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    my_text = Font1.render("Future chronochills", True, (255, 255, 255))
    button_pos = (470, 200)
    button_rect = pygame.Rect(button_pos, play_unclicked.get_size())

    left, middle, right = pygame.mouse.get_pressed()

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        button_image = play_clicked
        pygame.mouse.set_cursor(hand)
    else:
        play_unclicked == pygame.image.load("play_unclicked.png").convert_alpha()
        pygame.mouse.set_cursor()
        

  

    screen.blit(screen1, (0,0))
    screen.blit(my_text, (180, 50))
    screen.blit(play_unclicked, (button_x1, button_y1))
    screen.blit(options_unclicked, (button_x2, button_y2))
    screen.blit(quit_unclicked, (button_x3, button_y3))
    pygame.display.update()

pygame.quit()
