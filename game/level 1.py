import pygame
import os

from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init()

screen_height = 672
screen_width  = 1200

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("level 1")
logo = pygame.image.load("chronochills logo.png")
logo = pygame.transform.scale(logo, (550, 300))
pygame.display.set_icon(logo)

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False