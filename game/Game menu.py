import pygame
import os
import subprocess
import sys

from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init()

screen_height = 672
screen_width  = 1200
mute_state = True

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

def options():
    global screen, mute_state
    running10 = True
  # Initialize mute state (True means muted)

    while running10:
        # Background and options title
        back_op = pygame.image.load("pixil-frame-0.png")
        back_op = pygame.transform.scale(back_op, (screen_width, screen_height))
        screen.blit(back_op, (0, 0))

        options_title = pygame.image.load("options title.png")
        options_title = pygame.transform.scale(options_title, (300, 175))
        screen.blit(options_title, (25, -5))

        # Buttons
        fullscreen_button = pygame.image.load("fullscreen.png")
        fullscreen_button = pygame.transform.scale(fullscreen_button, (350, 100))
        exit_fullscreen_button = pygame.image.load("exit fullscreen.png")
        exit_fullscreen_button = pygame.transform.scale(exit_fullscreen_button, (350, 100))

        # Load mute/unmute button based on state
        if mute_state:
            mute_button = pygame.image.load("unmute.png")
        else:
            mute_button = pygame.image.load("mute.png")
        mute_button = pygame.transform.scale(mute_button, (150, 150))

        # Button positions and hitboxes
        button_pos = (8, 125)  # Same position for fullscreen/exit button
        fullscreen_rect = pygame.Rect(button_pos, fullscreen_button.get_size())
        exit_fullscreen_rect = pygame.Rect(button_pos, exit_fullscreen_button.get_size())
        mute_pos = (20, 200)
        mute_rect = pygame.Rect(mute_pos, mute_button.get_size())

        # Draw mute and fullscreen buttons
        screen.blit(mute_button, mute_pos)
        if screen.get_flags() & pygame.FULLSCREEN:
            screen.blit(exit_fullscreen_button, button_pos)
        else:
            screen.blit(fullscreen_button, button_pos)

        # Reset cursor if not over buttons
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running10 = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect single click
                if mute_rect.collidepoint(event.pos):  # Check if mute button is clicked
                    mute_state = not mute_state  # Toggle mute state
                elif fullscreen_rect.collidepoint(event.pos) and not screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                elif exit_fullscreen_rect.collidepoint(event.pos) and screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    pygame.display.update()

        back = pygame.image.load("back.png")
        screen.blit(back, (-50, 400))
        back_pos = (-50, 400)
        back_rect = pygame.Rect(back_pos, back.get_size())
        if back_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(hand)
            if pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_cursor(hand)
                running10 = False
            else:
                pygame.mouse.set_cursor()


        # Update the display
        pygame.display.flip()

def display_idle():
    global screen  # Ensure screen is accessible
    # Load the spritesheet
    try:
        sprite_sheet = pygame.image.load('adam_idle-sheet.png').convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return

    # Define the size of each frame
    frame_width1 = 420
    frame_height1 = 998
    num_frames = sprite_sheet.get_width() // frame_width1

    # Extract each frame
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface((i * frame_width1, 0, frame_width1, frame_height1))
        frames.append(frame)

    # Animation loop
    clock = pygame.time.Clock()
    frame_index = 0
    running1 = True

    while running1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:  # Exit on ESC
                running1 = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Display the current frame
        screen.blit(frames[frame_index],
                    (screen.get_width() // 2 - frame_width1 // 2,
                     screen.get_height() // 2 - frame_height1 // 2))
        frame_index = (frame_index + 1) % num_frames  # Cycle through frames

        keys1 = pygame.key.get_pressed()
        if keys1[pygame.K_d]:
            display_walk()
        
        if keys1[pygame.K_w]:
            display_jump()

        # Update the display
        pygame.display.update()
        clock.tick(10)  # Set the frame rate (e.g., 10 FPS)



    pygame.quit()

def display_walk():
    global screen  # Ensure screen is accessible
    # Load the spritesheet
    try:
        sprite_sheet = pygame.image.load('adam_walk_1-sheet.png').convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return

    # Define the size of each frame
    frame_width = 410
    frame_height = 998
    num_frames = sprite_sheet.get_width() // frame_width

    # Extract each frame
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)

    # Animation loop
    clock = pygame.time.Clock()
    frame_index = 0
    running1 = True

    while running1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:  # Exit on ESC
                running1 = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Display the current frame
        screen.blit(frames[frame_index],
                    (screen.get_width() // 2 - frame_width // 2,
                     screen.get_height() // 2 - frame_height // 2))
        frame_index = (frame_index + 1) % num_frames  # Cycle through frames

        # Update the display
        pygame.display.update()
        clock.tick(10)  # Set the frame rate (e.g., 10 FPS)



    pygame.quit()

def display_jump():
    global screen  # Ensure screen is accessible
    # Load the spritesheet
    try:
        sprite_sheet = pygame.image.load('adam_jump-sheet.png').convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return

    # Define the size of each frame
    frame_width = 416
    frame_height = 892
    num_frames = sprite_sheet.get_width() // frame_width

    # Extract each frame
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)

    # Animation loop
    clock = pygame.time.Clock()
    frame_index = 0
    running1 = True

    while running1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:  # Exit on ESC
                running1 = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Display the current frame
        screen.blit(frames[frame_index],
                    (screen.get_width() // 2 - frame_width // 2,
                     screen.get_height() // 2 - frame_height // 2))
        frame_index = (frame_index + 1) % num_frames  # Cycle through frames

        # Update the display
        pygame.display.update()
        clock.tick(10)  # Set the frame rate (e.g., 10 FPS)



    pygame.quit()

def play():
    import pygame
    import os
    import sys
    import cv2

    from pygame.display import get_window_size
    from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,K_SPACE,KEYDOWN,QUIT,)

    global screen, mute_state

    pygame.init()

    window_size = (1200, 672)

    sprite_sheet = pygame.image.load('adam_walk_1-sheet.png')


    intro = "chronochills intro video.mp4"
    audio_path = "chronochills intro.mp3"
    cap = cv2.VideoCapture(intro)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    if mute_state:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)
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
        ret, frame = cap.read()
        if not ret:  # Exit the loop if the video ends
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            break

        # Frame processing
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate frame
        frame = cv2.flip(frame, 0)  # Flip vertically
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.scale(frame_surface, window_size)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:  # Close window
                cap.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
  # Exit the loop

        # Draw and display frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay)



    # Add this after the video loop
    pygame.mixer.music.stop()  # Stop the audio
    cap.release()# Release the video file
    display_idle()
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
    

running5 = True

mouse_pressed = pygame.mouse.get_pressed()


while running5:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

            clock.tick(60)
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect single click
                if mute_rect.collidepoint(event.pos):  # Check if the mute button is clicked
                    mute_state = not mute_state  # Toggle mute state
            if mute_state:
                # Display the mute button
                screen.blit(mute, mute_pos)
            else:
                # Display the unmute button
                screen.blit(unmute, mute_pos)

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
