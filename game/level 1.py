import pygame
import os
import sys
import cv2

from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

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




screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("level 1")
logo = pygame.image.load("chronochills logo.png")
logo = pygame.transform.scale(logo, (550, 300))
pygame.display.set_icon(logo)

running = True

fps = cap.get(cv2.CAP_PROP_FPS)  # Get the video's FPS
delay = int(1000 / fps)  # Calculate the frame delay

while running:
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



        
