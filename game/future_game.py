import pygame
import os
import subprocess
import sys
from pytmx import load_pygame
import random
import time

from pygame.display import get_window_size
from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,KEYDOWN,QUIT,K_z, KSCAN_ESCAPE)

pygame.init()

screen_height = 672
screen_width  = 1200
mute_state = True
fullscreen = False
main_menu = True
return_to_main_menu = False
running10 = False
options_clickable = True

screen = pygame.display.set_mode((screen_width, screen_height))

tmx_data = load_pygame("tilemap.tmx")

# Function to render the map

clock = pygame.time.Clock()

def intro():
    import pygame
    import os
    import sys
    import cv2

    from pygame.display import get_window_size
    from pygame.locals import (K_w, K_s, K_d, K_a, K_ESCAPE, K_SPACE, KEYDOWN, QUIT,)

    global screen, mute_state

    pygame.init()

    window_size = (1200, 672)

    sprite_sheet = pygame.image.load('adam_walk_1-sheet.png')

    intro = "intro video.mp4"
    cap = cv2.VideoCapture(intro)

    pygame.display.set_caption("chronochills")
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
                pygame.quit()
                sys.exit()

        # Draw and display frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay)

    # Add this after the video loop
    cap.release()  # Release the video file

intro()



def load_tilemap(map_file):
    """Load and draw the tilemap."""
    tmx_data = load_pygame(map_file)
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):  # Check if the layer contains tiles
            for x, y, tile in layer.tiles():
                screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

def options():
    global screen, mute_state, fullscreen, running10
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
                break
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

def level2():
    global screen
    pygame.init()

    font = pygame.font.Font('Double Pixel-7 400.ttf', 120)
    coming_soon = font.render("Level 2 is coming soon!", True, (255, 0, 0))

    running100 = True
    while running100:
        screen.fill((0, 0, 0))
        screen.blit(coming_soon, (screen_width // 2 - coming_soon.get_width() // 2, screen_height // 3))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running100 = False  # Exit the loop when ESC is pressed

        pygame.display.flip()




class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction
        self.width = 30
        self.height = 15
        self.color = (0, 255, 255)  # Blue color

    def move(self):
        self.x += self.speed * self.direction

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4.7
        self.direction = random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])
        self.image = pygame.image.load("monster.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.health = 3
        
        # Keep the monster within the screen bounds
        self.x = max(0, min(screen_width - 250, self.x))
        self.y = max(0, min(screen_height - 250, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def hit(self):
        self.health -= 1


def show_losing_page():
    """Display the losing page."""
    global screen

    pygame.init()

    # Load losing text
    font = pygame.font.Font('Double Pixel-7 400.ttf', 160)
    losing_text = font.render("You Lost!", True, (255, 0, 0))

    reset = pygame.image.load("reset.png")
    reset = pygame.transform.scale(reset, (200, 100))  # Adjust size as needed

    # Button position and hitbox
    button_pos100 = (screen_width // 2 - reset.get_width() // 2, screen_height // 2)
    button_rect100 = pygame.Rect(button_pos, reset.get_size())

    running100 = True
    while running100:
        screen.fill((0, 0, 0))
        screen.blit(losing_text, (screen_width // 2 - losing_text.get_width() // 2, screen_height // 4))
        screen.blit(reset, button_pos100)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    player()
                    running100 = False

        pygame.display.flip()

def show_winning_page():
    """Display the winning page."""
    global screen

    # Load winning text
    font1 = pygame.font.Font('Double Pixel-7 400.ttf', 160)
    winning_text = font1.render("You won!", True, (0, 255, 0))

    next_level_button = pygame.image.load("next_level.png")
    next_level_button = pygame.transform.scale(next_level_button, (200, 100))  # Adjust size as needed

    # Button position and hitbox
    button_pos = (screen_width // 2 - next_level_button.get_width() // 2, screen_height // 2)
    button_rect = pygame.Rect(button_pos, next_level_button.get_size())

    running100 = True
    while running100:
        screen.fill((0, 0, 0))
        screen.blit(winning_text, (screen_width // 2 - winning_text.get_width() // 2, screen_height // 4))
        screen.blit(next_level_button, button_pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    level2()
                    running100 = False  # Exit the loop after transitioning to the next level

        pygame.display.flip()


def pause_menu():
    """Display the pause menu and handle events."""
    global screen, main_menu, return_to_main_menu

    # Load pause menu text
    font = pygame.font.Font('Double Pixel-7 400.ttf', 80)
    pause_text = font.render("Paused", True, (255, 255, 255))

    # Load resume button image
    resume_button = pygame.image.load("resume.png")
    resume_button = pygame.transform.scale(resume_button, (200, 100))  # Adjust size as needed

    # Load back to menu button image
    back_to_menu_button = pygame.image.load("back_to_menu.png")
    back_to_menu_button = pygame.transform.scale(back_to_menu_button, (200, 100))  # Adjust size as needed

    # Button positions and hitboxes
    resume_button_pos = (screen_width // 2 - resume_button.get_width() // 2, screen_height // 2)
    resume_button_rect = pygame.Rect(resume_button_pos, resume_button.get_size())

    back_to_menu_button_pos = (screen_width // 2 - back_to_menu_button.get_width() // 2, screen_height // 2 + resume_button.get_height() + 65)
    back_to_menu_button_rect = pygame.Rect(back_to_menu_button_pos, back_to_menu_button.get_size())

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 4))
        screen.blit(resume_button, resume_button_pos)
        screen.blit(back_to_menu_button, back_to_menu_button_pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Exit the pause menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    running = False  # Exit the pause menu
                elif back_to_menu_button_rect.collidepoint(event.pos):
                    running = False  # Exit the pause menu and go back to the main menu
                    main_menu = True
                    return_to_main_menu = True
                    options_clicked = False
                    music = "hard-hitting-techno-track-for-intense-vibes-266980.mp3"


        pygame.display.flip()
        pygame.time.wait(10)



    

import math

def player():
    """Main game loop handling animations, movement, and events, including double jumping."""
    global screen, fullscreen, return_to_main_menu

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
    hit_frames = load_animation('adam_hit_sheet.png', 870, 986, scale_factor=0.15)
    hidden = load_animation('lose play.png', 870, 986)

    map_file = "tilemap.tmx"

    music = "hard-hitting-techno-track-for-intense-vibes-266980.mp3"

    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    if mute_state:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)

    # Offset to move spritesheets down
    OFFSET_Y = 140

    # Player position and movement settings
    player_x = screen_width // 2
    player_y = screen_height // 2 + OFFSET_Y
    player_speed = 7
    jump_velocity = -30  # Increased jump velocity for faster jump
    gravity = 2  # Increased gravity for faster fall
    is_jumping = False
    jump_count = 0  # Tracks the number of jumps
    max_jumps = 2  # Limit to double jump
    facing_right = True  # Tracks sprite direction

    # Initial state
    current_frames = idle_frames
    current_state = "idle"
    frame_index = 0
    frame_timer = 0
    hit_frame_timer = 0
    hit_animation_playing = False
    hit_animation_done = False

    # Load background and icon
    logo = pygame.image.load("chronochills logo.png")
    logo = pygame.transform.scale(logo, (550, 300))
    pygame.display.set_icon(logo)

    background_image = pygame.image.load("level1_bg.png")

    health = 350  # Initialize health

    monster_num = 1
    max_num = 6
    min_distance = 200  # Minimum distance between player and monster

    total_spawned_monsters = 2  # Start with 2 monsters
    defeated_monsters = 0
   
    
    # Function to generate a valid monster position
    def generate_monster_position():
        while True:
            x = random.randint(0, screen_width - 150)
            y = random.randint(0, screen_height - 150)
            distance = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
            if distance >= min_distance:
                return x, y

    # Create "monster_num" monsters at valid positions
    monsters = [Monster(*generate_monster_position()) for _ in range(2)]

    # Load tilemap and collidable tiles
    tilemap = load_pygame(map_file)
    collidable_tiles = []
    for layer in tilemap.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, tile in layer.tiles():
                if hasattr(tile, "properties") and "collidable" in tile.properties:
                    collidable_tiles.append(pygame.Rect(x * tilemap.tilewidth, y * tilemap.tileheight, tilemap.tilewidth, tilemap.tileheight))

    # Load gun image
    gun_image = pygame.image.load("gun.png")
    gun_image = pygame.transform.scale(gun_image, (70, 90))  # Adjust the size as needed

    bullets = []
    max_bullets = 10  # Limit the number of bullets

    # Main loop
    while True:
        if return_to_main_menu:
            return_to_main_menu = False
            break
        screen.blit(background_image, (0, 0))
        load_tilemap(map_file)

        for monster in monsters:
            monster.draw()
            dx = player_x - monster.x
            dy = player_y - monster.y
            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            monster.x += monster.speed * dx / dist
            monster.y += monster.speed * dy / dist

        keys = pygame.key.get_pressed()

        # Draw health bar
        pygame.draw.rect(screen, "red", (20, 20, 350, 50))
        pygame.draw.rect(screen, "green", (20, 20, health, 50))

        if keys[pygame.K_ESCAPE]:
            pause_menu()
        
        # Movement logic
        player_dx = 0
        player_dy = 0
        if keys[pygame.K_d] and not hit_animation_playing:  # Move right
            current_state = "walking"
            current_frames = walk_frames
            frame_index %= len(current_frames)
            player_dx = player_speed
            facing_right = True
        elif keys[pygame.K_a] and not hit_animation_playing:  # Move left
            current_state = "walking"
            current_frames = walk_frames
            frame_index %= len(current_frames)
            player_dx = -player_speed
            facing_right = False
        elif not is_jumping and not hit_animation_playing:  # Idle state
            current_state = "idle"
            current_frames = idle_frames
            frame_index %= len(current_frames)

        # Jump logic with double jump
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not hit_animation_playing:
                if event.key == pygame.K_w and jump_count < max_jumps:
                    is_jumping = True
                    jump_count += 1
                    if jump_count == 2:  # Use double jump animation for the second jump
                        current_state = "double_jumping"
                        current_frames = double_jump_frames
                    else:
                        current_state = "jumping"
                        current_frames = jump_frames
                    frame_index = 0
                    jump_velocity = -30  # Reset velocity for the jump
                if event.key == pygame.K_SPACE and len(bullets) < max_bullets:  # Limit the number of bullets
                    # Calculate the gun's tip position
                    gun_x = player_x + (frame.get_width() // 2 if facing_right else -frame.get_width() // 2) - (gun_image.get_width() // 2)
                    gun_y = player_y - frame.get_height() // 6
                    bullet_x = gun_x + (gun_image.get_width() if facing_right else 0)
                    bullet_y = gun_y + gun_image.get_height() // 2.5
                    direction = 1 if facing_right else -1
                    bullets.append(Bullet(bullet_x, bullet_y, direction))

        if is_jumping:
            player_dy += jump_velocity
            jump_velocity += gravity
            if player_y + player_dy >= screen_height // 2 + OFFSET_Y:  # Reset when hitting the ground
                player_y = screen_height // 2 + OFFSET_Y
                is_jumping = False
                jump_count = 0
                jump_velocity = -30
                player_dy = 0

        # Create hitboxes for player and monsters
        player_rect = pygame.Rect(player_x - idle_frames[0].get_width() // 2, player_y - idle_frames[0].get_height() // 2, idle_frames[0].get_width(), idle_frames[0].get_height())
        monster_rects = [pygame.Rect(monster.x, monster.y, monster.image.get_width(), monster.image.get_height()) for monster in monsters]

        # Check for collision with collidable tiles
        player_rect.x += player_dx
        player_rect.y += player_dy
        for tile_rect in collidable_tiles:
            if player_rect.colliderect(tile_rect):
                if player_dx > 0:  # Moving right
                    player_rect.right = tile_rect.left
                elif player_dx < 0:  # Moving left
                    player_rect.left = tile_rect.right
                if player_dy > 0:  # Moving down
                    player_rect.bottom = tile_rect.top
                    is_jumping = False
                    jump_count = 0
                    jump_velocity = -30
                elif player_dy < 0:  # Moving up
                    player_rect.top = tile_rect.bottom
                player_dx = 0
                player_dy = 0

            for monster_rect in monster_rects:
                if monster_rect.colliderect(tile_rect):
                    # Reverse monster direction on collision
                    monster = monsters[monster_rects.index(monster_rect)]
                    monster.direction = (-monster.direction[0], -monster.direction[1])

        # Update player position
        player_x = player_rect.centerx
        player_y = player_rect.centery

        # Check for collision with monsters
        # Check for collision with monsters
        # Check for collision with monsters
        for monster_rect in monster_rects:
            if player_rect.colliderect(monster_rect):  # Only apply pushback if there is a collision
                # Reduce health
                health -= 2
                current_state = "hit"
                current_frames = hit_frames
                frame_index = 0  # Reset frame index for hit animation
                hit_animation_playing = True
                hit_animation_done = False

                # Get the monster causing the collision
                monster = monsters[monster_rects.index(monster_rect)]

                # Calculate pushback direction
                pushback_x = player_x - monster.x
                pushback_y = player_y - monster.y
                pushback_distance = 50  # Distance to push the player back
                pushback_magnitude = max(1, (pushback_x ** 2 + pushback_y ** 2) ** 0.5)
                pushback_x = (pushback_x / pushback_magnitude) * pushback_distance
                pushback_y = (pushback_y / pushback_magnitude) * pushback_distance

                # Apply pushback
                player_x += pushback_x
                player_y += pushback_y

                # Clamp player position to screen boundaries
                player_x = max(0, min(player_x, screen_width - idle_frames[0].get_width()))
                player_y = max(0, min(player_y, screen_height - idle_frames[0].get_height()))

                # Ensure health doesn't go below 0
                if health < 0:
                    health = 0
                    if health == 0:
                        current_state = "hidden"
                        current_frames = hidden
                        show_losing_page()



        if health < 0:
            health = 0  # Ensure health doesn't go below 0
            if health == 0:
                current_state = "hidden"
                current_frames = hidden
                show_losing_page()

        last_hit_time = 0  # Initialize a variable to track the last hit time
        hit_cooldown = 1  # Cooldown in seconds

# Inside the collision handling logic
        current_time = time.time()
        if current_time - last_hit_time > hit_cooldown:
            last_hit_time = current_time
    # Apply pushback and reduce health


        # Move and draw bullets ------------------------------------------------------------------------------------------------------------
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.x < 0 or bullet.x > screen_width:
                bullets.remove(bullet)
            else:
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                for monster in monsters:
                    monster_rect = pygame.Rect(monster.x, monster.y, monster.image.get_width(), monster.image.get_height())
                    if bullet_rect.colliderect(monster_rect):
                        monster.hit()
                        try:
                            bullets.remove(bullet)
                        except ValueError:
                            pass

                        if monster.health <= 0:
                           monsters.remove(monster)
                           defeated_monsters += 1

                           # Check if all six monsters have been defeated
                           if defeated_monsters == 14:
                               show_winning_page()

                           # Spawn two more monsters if less than six have been spawned
                           if len(monsters) == 0 and total_spawned_monsters < 14:
                               monsters.extend([Monster(*generate_monster_position()) for _ in range(2)])
                               total_spawned_monsters += 2
   
        # -----------------------------------------------------------------------------------------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Animation frame update
        frame_timer += 1
        hit_frame_timer += 1
        if hit_animation_playing:
            if hit_frame_timer >= 2:  # Change hit frame every 3 ticks (faster)
                frame_index = (frame_index + 1) % len(current_frames)
                hit_frame_timer = 0
        else:
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

            # Calculate gun position
            gun_x = player_x + (frame.get_width() // 2 if facing_right else -frame.get_width() // 2) - (gun_image.get_width() // 2)
            gun_y = player_y - frame.get_height() // 6

            # Flip gun image if facing left
            gun_to_blit = gun_image if facing_right else pygame.transform.flip(gun_image, True, False)

            # Blit gun image
            screen.blit(gun_to_blit, (gun_x, gun_y))

                 # Check if hit animation is done
        if hit_animation_playing and frame_index == len(hit_frames) - 1:
            hit_animation_playing = False
            hit_animation_done = True

        # Move player back after hit animation is done
        

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

    music = "hard-hitting-techno-track-for-intense-vibes-266980.mp3"

    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0)


    
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
            main_menu = False
            
            
        
    
    elif options_clickable and button_rect1.collidepoint(pygame.mouse.get_pos()):
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
