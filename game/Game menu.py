import pygame
import os
from pygame.locals import (K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init

screen_height = 800
screen_width  = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("future chronochills")
screen1 = pygame.image.load("c:\Users\og126\Downloads\hack1.jpg")

running = True


while running:
    
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
        
            if event.key == K_ESCAPE:
                running = False

        
        elif event.type == QUIT:
            running = False


