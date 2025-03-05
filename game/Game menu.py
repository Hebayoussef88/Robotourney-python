import pygame
import os
from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init

screen_height = 672
screen_width  = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("future chronochills")
screen1 = pygame.image.load("hack1 .jpg")
scale = pygame.transform.scale(screen1, (800, 1200))

running = True


while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.blit(screen1, (0,0))
    pygame.display.update()

pygame.quit()
