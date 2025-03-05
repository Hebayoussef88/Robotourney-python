import pygame
import os
from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init()

screen_height = 672
screen_width  = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("future chronochills")
screen1 = pygame.image.load("hack1 .jpg")
scale = pygame.transform.scale(screen1, (800, 1200))
Font1 = pygame.font.Font('Double Pixel-7 400.ttf', 135)

running = True


while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    my_text = Font1.render("Future chronochills", True, (255, 255, 255))

    screen.blit(screen1, (0,0))
    screen.blit(my_text, (180, 50))
    pygame.display.update()

pygame.quit()
