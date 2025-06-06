import pygame
import os
import subprocess
import sys
import random
from pytmx import load_pygame


from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,)

pygame.init()

screen_height = 672
screen_width  = 1200
mute_state = True
fullscreen = False

screen = pygame.display.set_mode((screen_width, screen_height))

tmx_data = load_pygame("tilemap.tmx")

# Function to render the map

clock = pygame.time.Clock()

def load_tilemap(map_file):
    """Load and draw the tilemap."""
    tmx_data = load_pygame(map_file)
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):  # Check if the layer contains tiles
            for x, y, tile in layer.tiles():
                screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

def options():
    global screen, mute_state, fullscreen
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
                    fullscreen = True
                elif exit_fullscreen_rect.collidepoint(event.pos) and screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    fullscreen = False
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

def load_animation(sprite_sheet_path, frame_width, frame_height, scale_factor=0.2):
    """Load and scale frames from a spritesheet."""
    try:
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return []

    num_frames = sprite_sheet.get_width() // frame_width

    # Calculate scaled dimensions
    scaled_width = int(frame_width * scale_factor)
    scaled_height = int(frame_height * scale_factor)

    # Extract and scale each frame
    frames = [
        pygame.transform.scale(
            sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height)),
            (scaled_width, scaled_height)
        )
        for i in range(num_frames)
    ]
    return frames

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.direction = random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])
        self.image = pygame.image.load("monster.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

    def move(self):
        if random.randint(0, 50) == 0:  # Change direction randomly
            self.direction = random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])
        self.x += self.direction[0]
        self.y += self.direction[1]
        
        # Keep the monster within the screen bounds
        self.x = max(0, min(screen_width - 50, self.x))
        self.y = max(0, min(screen_height - 50, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    



def play():
    global screen, mute_state
    
    pygame.init()
    
    

        
    
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
    player()
    monster = Monster(600, 336)  # Create a monster in the middle of the screen
    
   
           
       
        
    monster.move()
    monster.draw()
def player():
    """Main game loop handling animations, movement, and events, including double jumping."""
    global screen, fullscreen

    # Screen settings
    screen_width, screen_height = 1200, 672
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("level 1")
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    # Load animations
    idle_frames = load_animation('adam_idle-sheet.png', 420, 998)
    walk_frames = load_animation('adam_walk_1-sheet.png', 410, 998)
    jump_frames = load_animation('adam_jump-sheet.png', 416, 892)
    double_jump_frames = load_animation('adam_double-sheet.png', 600, 797)

    map_file = "tilemap.tmx"

    # Offset to move spritesheets down
    OFFSET_Y = 140

    # Player position and movement settings
    player_x = screen_width // 2
    player_y = screen_height // 2 + OFFSET_Y
    player_speed = 7
    jump_velocity = -22
    gravity = 1
    is_jumping = False
    jump_count = 0  # Tracks the number of jumps
    max_jumps = 2   # Limit to double jump
    facing_right = True  # Tracks sprite direction

    # Initial state
    current_frames = idle_frames
    current_state = "idle"
    frame_index = 0
    frame_timer = 0

    # Load background and icon
    logo = pygame.image.load("chronochills logo.png")
    logo = pygame.transform.scale(logo, (550, 300))
    pygame.display.set_icon(logo)

    background_image = pygame.image.load("level1_bg.png")

    # Main loop
    while True:
        screen.blit(background_image, (0, 0))
        load_tilemap(map_file)

        keys = pygame.key.get_pressed()

        # Movement logic
        if keys[pygame.K_d]:  # Move right
            current_state = "walking"
            current_frames = walk_frames
            frame_index %= len(current_frames)
            player_x += player_speed
            facing_right = True
        elif keys[pygame.K_a]:  # Move left
            current_state = "walking"
            current_frames = walk_frames
            frame_index %= len(current_frames)
            player_x -= player_speed
            facing_right = False
        elif not is_jumping:  # Idle state
            current_state = "idle"
            current_frames = idle_frames
            frame_index %= len(current_frames)

        #        # Jump logic with double jump
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w and jump_count < max_jumps:
                is_jumping = True
                jump_count += 1
                if jump_count == 2:  # Use double jump animation for the second jump
                    current_state = "double_jumping"
                    current_frames = double_jump_frames
                else:
                    current_state = "jumping"
                    current_frames = jump_frames
                frame_index = 0
                jump_velocity = -22  # Reset velocity for the jump

        if is_jumping:
            player_y += jump_velocity
            jump_velocity += gravity
            if player_y >= screen_height // 2 + OFFSET_Y:  # Reset when hitting the ground
                player_y = screen_height // 2 + OFFSET_Y
                is_jumping = False
                jump_count = 0
                jump_velocity = -22


        if is_jumping:
            player_y += jump_velocity
            jump_velocity += gravity
            if player_y >= screen_height // 2 + OFFSET_Y:  # Reset when hitting the ground
                player_y = screen_height // 2 + OFFSET_Y
                is_jumping = False
                jump_count = 0
                jump_velocity = -22

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Animation frame update
        frame_timer += 1
        if frame_timer >= 5:  # Change frame every 5 ticks
            frame_index = (frame_index + 1) % len(current_frames)
            frame_timer = 0

        # Render the current animation frame
        if current_frames:
            frame = current_frames[frame_index]
            if not facing_right:  # Flip frame if facing left
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(
                frame,
                (player_x - frame.get_width() // 2, player_y - frame.get_height() // 2)
            )

        pygame.display.update()
        clock.tick(30)







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

screen = pygame.display.set_mode((1200, 672))


while running5:
    pygame.init()
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
