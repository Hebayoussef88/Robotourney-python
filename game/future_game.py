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
level_2 = False
main_menu_active = True
underoos = False


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

class Boss:
    def __init__(self, x, y, screen):
        self.screen = screen
        self.x = x  # Image position
        self.y = y  # Image position
        self.rect_x = x  # Rect position
        self.rect_y = y  # Rect position
        self.speed = 20
        self.boss_image = pygame.image.load("boss.png")
        self.original_image = pygame.transform.scale(self.boss_image, (280, 300))  # Store the original image
        self.boss_image = self.original_image.copy()  # Copy for transformations
        self.health = 90
        self.rolling = True
        self.direction = 1
        self.angle = 0
        self.on_ground = False
        self.rotated_rect = None
        self.Mask = None
        self.rect_scale_x = 1.0  # Default scaling factor for the rect
        self.mask_scale_x = 1.0  # Default scaling factor for the mask
        self.boss_bullets = []  # List to store boss bullets
        self.shoot_cooldown = 1000  # Cooldown in milliseconds
        self.shoot_cooldown1 = 370
        self.last_shot_time = 0 
        self.rotating = False
        self.rotation_speed = 5  # degrees per frame
        self.rotation_count = 0  # Tracks how many degrees we've rotated

        # Initialize rotated rect and mask
        self.update_rotated_rect_and_mask()

    def shoot(self, player_x, player_y):
        """Shoot a bullet towards the player."""
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_shot_time > self.shoot_cooldown:
            # Calculate direction towards the player
            dx = player_x - self.rect_x
            dy = player_y - self.rect_y
            distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            direction_x = dx / distance
            direction_y = dy / distance

            # Create a new BossBullet
            bullet = BossBullet(self.rect_x, self.rect_y, direction_x, direction_y)
            self.boss_bullets.append(bullet)  # Add the bullet to the list
            self.last_shot_time = current_time  # Update the last shot time

    def shoot1(self, player_x, player_y):
        """Shoot a bullet towards the player."""
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_shot_time > self.shoot_cooldown1:
            # Calculate direction towards the player
            dx = player_x - self.rect_x
            dy = player_y - self.rect_y
            distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            direction_x = dx / distance
            direction_y = dy / distance

            # Create a new BossBullet
            bullet = BossBullet1(self.rect_x, self.rect_y, direction_x, direction_y)
            self.boss_bullets.append(bullet)  # Add the bullet to the list
            self.last_shot_time = current_time  # Update the last shot time

    
    def update_bullets(self):
        """Update and draw bullets fired by the boss."""
        for bullet in self.boss_bullets[:]:
            bullet.move()  # Move the bullet
            bullet.draw()  # Draw the bullet on the screen
            # Remove bullets that go off-screen
            if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
                self.boss_bullets.remove(bullet)


    def update_rotated_rect_and_mask(self):
        """Update the rotated rect, mask, and image size."""
        # Scale the boss image to match the rect size
        scaled_width = int(self.original_image.get_width() * self.rect_scale_x)
        scaled_height = int(self.original_image.get_height() * self.rect_scale_x)
        self.boss_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

        # Rotate the boss image
        rotated_image = pygame.transform.rotate(self.boss_image, self.angle)

        # Update the rotated rect with scaling and offsets
        self.rotated_rect = rotated_image.get_rect(center=(self.rect_x, self.rect_y))

        # Update the mask with scaling
        self.Mask = pygame.mask.from_surface(rotated_image)

    def move_rect_and_mask(self, offset_x, offset_y):
        self.rect_x += offset_x
        self.rect_y += offset_y
        self.x = self.rect_x  # Synchronize image position with rect
        self.y = self.rect_y  # Synchronize image position with rect
        print(f"Rect position updated: rect_x={self.rect_x}, rect_y={self.rect_y}")  # Debug
        self.update_rotated_rect_and_mask()

    def phase1(self):
        """Handle the boss's movement and behavior in phase 1."""
        if not self.on_ground:
            ground_level = screen_height - self.boss_image.get_height() + 110  # Move boss closer to the ground
            self.rect_y += 10  # Move the rect down
            self.rect_x += 10  # Move the rect right
            if self.rect_y >= ground_level:
                self.rect_y = ground_level
                self.on_ground = True

        if self.on_ground and self.rolling:
            self.rect_x += self.speed * self.direction  # Move the rect horizontally

        # Reverse direction if the rect hits the screen boundaries
            if self.rotated_rect.left <= 0:
                self.rect_x = self.rotated_rect.width // 2
                self.direction *= -1
            elif self.rotated_rect.right >= screen_width:
                self.rect_x = screen_width - self.rotated_rect.width // 2
                self.direction *= -1

        # Rotate the boss only when rolling
            if self.rolling:
                self.angle += 10

        # Stop rolling if health is low
            if self.health <= 57:
                self.rolling = False

    # Update the rotated rect and mask after movement or rotation
        self.update_rotated_rect_and_mask()



    def phase2(self, player_x, player_y):
        """Handle the boss's behavior in phase 2."""
        # Move the boss back to the sky
        target_y = 100  # Target position near the top of the screen
        if self.rect_y > target_y:
            self.rect_y -= 5  # Move upward by 5 pixels per frame

        # Ensure the boss doesn't go above the target position
        if self.rect_y < target_y:
            self.rect_y = target_y
            
        left_edge = 50  # Left edge position
        right_edge = screen_width - self.rotated_rect.width - 50

        if not hasattr(self, "moving_right"):
            self.moving_right = True  # Initialize direction
        if not hasattr(self, "wait_timer"):
            self.wait_timer = 0  # Initialize the wait timer

        current_time = pygame.time.get_ticks()  # Get the current time

        if self.wait_timer > 0:
            # Boss is waiting; check if the wait time has passed
            if current_time - self.wait_timer >= 1500:  # 1.5 seconds
                self.wait_timer = 0  # Reset the timer
        else:
            if self.moving_right:
                # Move to the right edge
                if self.rect_x < right_edge:
                    self.rect_x += 5  # Move right by 5 pixels per frame
                else:
                    self.moving_right = False  # Switch direction
                    self.shoot(player_x, player_y)  # Shoot bullets
                    self.wait_timer = current_time  # Start the wait timer
            else:
                # Move to the left edge
                if self.rect_x > left_edge:
                    self.rect_x -= 5  # Move left by 5 pixels per frame
                else:
                    self.moving_right = True  # Switch direction

                    self.wait_timer = current_time  # Start the wait timer
        self.shoot(player_x, player_y)  # Shoot bullets
        self.update_bullets()  # Update and draw bullets
        self.update_rotated_rect_and_mask()  # Ensure the boss's rect and mask are updated

    

    def phase3(self, player_x, player_y):
        self.boss_image = pygame.image.load("anger_boss.png")
        self.boss_image = pygame.transform.scale(self.boss_image, (280, 300))  # Store the original image
        self.original_image = pygame.transform.scale(self.boss_image, (280, 300))  # Store the original image
        self.boss_image = self.original_image.copy()  # Copy for transformations

       
        target_y = 100  # Target position near the top of the screen
        if self.rect_y > target_y:
            self.rect_y -= 5  # Move upward by 5 pixels per frame

        # Ensure the boss doesn't go above the target position
        if self.rect_y < target_y:
            self.rect_y = target_y
            
        left_edge = 50  # Left edge position
        right_edge = screen_width - self.rotated_rect.width - 50

        if not hasattr(self, "moving_right"):
            self.moving_right = True  # Initialize direction
        if not hasattr(self, "wait_timer"):
            self.wait_timer = 0  # Initialize the wait timer

        current_time = pygame.time.get_ticks()  # Get the current time

        if self.wait_timer > 0:
            # Boss is waiting; check if the wait time has passed
            if current_time - self.wait_timer >= 1500:  # 1.5 seconds
                self.wait_timer = 0  # Reset the timer
        else:
            if self.moving_right:
                # Move to the right edge
                if self.rect_x < right_edge:
                    self.rect_x += 5  # Move right by 5 pixels per frame
                else:
                    self.moving_right = False  # Switch direction
                    self.shoot(player_x, player_y)  # Shoot bullets
                    self.wait_timer = current_time  # Start the wait timer
            else:
                # Move to the left edge
                if self.rect_x > left_edge:
                    self.rect_x -= 5  # Move left by 5 pixels per frame
                else:
                    self.moving_right = True  # Switch direction

                    self.wait_timer = current_time  # Start the wait timer
        self.shoot1(player_x, player_y)  # Shoot bullets
        self.update_bullets()  # Update and draw bullets
        self.update_rotated_rect_and_mask()  # Ensure the boss's rect and mask are

    def death(self):
        self.rect_y += 20
        for bullet in self.boss_bullets[:]:
            self.boss_bullets.remove(bullet)

            






    def draw(self):
        # Rotate the boss image
        rotated_image = pygame.transform.rotate(self.boss_image, self.angle)

        # Draw the rotated image on the screen
        self.screen.blit(rotated_image, self.rotated_rect.topleft)

        # Draw the rotated_rect as a red rectangle
        print(f"Drawing rect at: {self.rotated_rect.topleft}")  # Debug

        # Visualize the mask as a semi-transparent overlay
        mask_surface = self.Mask.to_surface(setcolor=(0, 0, 0, 0), unsetcolor=(0, 0, 0, 0))  # Green with transparency
        self.screen.blit(mask_surface, self.rotated_rect.topleft)

    def hit(self):
        self.health -= 8

class BossBullet:
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y
        self.speed = 7.5
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.image = pygame.image.load("fireball.png")  
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect(center=(self.x, self.y))  

    def move(self):
        """Move the bullet in the specified direction."""
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y
        self.rect.center = (self.x, self.y)  
    def draw(self):
        """Draw the bullet on the screen."""
        screen.blit(self.image, self.rect.topleft)

class BossBullet1:
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y
        self.speed = 10
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.image = pygame.image.load("fireball.png")  
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect(center=(self.x, self.y))  

    def move(self):
        """Move the bullet in the specified direction."""
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y
        self.rect.center = (self.x, self.y)  
    def draw(self):
        """Draw the bullet on the screen."""
        screen.blit(self.image, self.rect.topleft)



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

def load_tilemap(map_file):
    """Load and draw the tilemap."""
    tmx_data = load_pygame(map_file)
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):  # Check if the layer contains tiles
            for x, y, tile in layer.tiles():
                screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))



def pause_menu():
    """Display the pause menu and handle events."""
    global screen, main_menu, return_to_main_menu, running2

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
                    # Set flags to return to the main menu
                    main_menu = True
                    return_to_main_menu = True
                    running = False  # Exit the pause menu loop

        pygame.display.flip()
        pygame.time.wait(10)

def show_losing_page():
    """Display the losing page."""
    global screen, level_2

    pygame.init()

    # Load losing text
    font1 = pygame.font.Font('Double Pixel-7 400.ttf', 160)
    losing_text1 = font1.render("You Lost!", True, (255, 0, 0))

    reset1 = pygame.image.load("reset.png")
    reset1 = pygame.transform.scale(reset1, (200, 100))  # Adjust size as needed

    # Button position and hitbox
    button_pos1001 = (screen_width // 2 - reset1.get_width() // 2, screen_height // 2)
    button_rect1001 = pygame.Rect(button_pos1001, reset1.get_size())

    running100 = True
    while running100:
        screen.fill((0, 0, 0))
        screen.blit(losing_text1, (screen_width // 2 - losing_text1.get_width() // 2, screen_height // 4))
        screen.blit(reset1, button_pos1001)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect1001.collidepoint(event.pos):
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

def show_losing_page2():
    """Display the losing page."""
    global screen

    pygame.init()

    # Load losing text
    font = pygame.font.Font('Double Pixel-7 400.ttf', 160)
    losing_text = font.render("You Lost!", True, (255, 0, 0))

    reset = pygame.image.load("reset.png")
    reset = pygame.transform.scale(reset, (200, 100))  # Adjust size as needed

    # Button position and hitbox
    button_pos = (screen.get_width() // 2 - reset.get_width() // 2, screen.get_height() // 2)
    button_rect = pygame.Rect(button_pos, reset.get_size())

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(losing_text, (screen.get_width() // 2 - losing_text.get_width() // 2, screen.get_height() // 4))
        screen.blit(reset, button_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False  # Exit loop before restarting
                    level2_main()    # Restart level

        pygame.display.flip()

def finalle():
    import pygame
    import os
    import sys
    import cv2
    import numpy as np

    from pygame.display import get_window_size
    from pygame.locals import (K_w, K_s, K_d, K_a, K_ESCAPE, K_SPACE, KEYDOWN, QUIT,)

    global screen, mute_state, fullscreen

    pygame.init()

    window_size = (1200, 672)

    sprite_sheet = pygame.image.load('adam_walk_1-sheet.png')



    intro = "final.mp4"
    cap = cv2.VideoCapture(intro)



    pygame.display.set_caption("level 2")
    logo = pygame.image.load("chronochills logo.png")
    logo = pygame.transform.scale(logo, (550, 300))
    pygame.display.set_icon(logo)

    running = True

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the video's FPS
    delay = int(1000 / fps)  # Calculate the frame delay

    while running:
        ret, frame = cap.read()
        if not ret:  # Exit the loop if the video ends
            quit()

        # Frame processing
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate frame
        frame = cv2.flip(frame, 0)  # Flip vertically
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.scale(frame_surface, window_size)

        if fullscreen:
            screen = pygame.display.set_mode((window_size), pygame.FULLSCREEN)
            screen.blit(pygame.transform.scale(frame_surface, screen.get_size()), (20, 0))
        else:
            screen = pygame.display.set_mode((window_size))

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

boss = Boss(300, 0, screen)
# Scale the rect to 1.5x on the x-axis
boss.rect_scale_x = 0.8  # Increase size by 50%
# Scale the rectangle dynamically
boss.update_rotated_rect_and_mask()


def play():
    import pygame
    import os
    import sys
    import cv2

    from pygame.display import get_window_size
    from pygame.locals import (K_w,K_s,K_d,K_a,K_ESCAPE,K_SPACE,KEYDOWN,QUIT,)

    global screen, mute_state


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

    intro = "level 2 intro.mp4"
    cap = cv2.VideoCapture(intro)

    pygame.display.set_caption("level 2")
    logo = pygame.image.load("chronochills logo.png")
    logo = pygame.transform.scale(logo, (550, 300))
    pygame.display.set_icon(logo)

    pygame.mixer.music.load("level 2 intro.mp3")  # Replace with the actual audio file name
    pygame.mixer.music.play()
    if mute_state:
        pygame.mixer.music.set_volume(1)  # Set volume to full if not muted
    else:
        pygame.mixer.music.set_volume(0)  # Mute the audio if mute_state is True
   

    running = True

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the video's FPS
    delay = int(380 / fps)  # Calculate the frame delay

    while running:
        ret, frame = cap.read()
        if not ret:  # Exit the loop if the video ends
            level2_main()
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            level2_main()
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



import math

def player():
    """Main game loop handling animations, movement, and events, including double jumping."""
    global screen, fullscreen, return_to_main_menu, underoos

    underoos = False

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
            main_menu = True
            break
        if underoos:
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

        player_x = max(0, min(player_rect.centerx, screen_width - idle_frames[0].get_width()))

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
                               pygame.mixer.music.stop()
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

def level2_main():
    """Main game loop handling animations, movement, and events, including double jumping."""
    global screen, fullscreen, return_to_main_menu, boss, main_menu, main_menu_active, underoos

    boss_x = 1000
    boss_y = 450
    boss = Boss(boss_x, boss_y, screen)

    # Screen settings
    screen_width, screen_height = 1200, 672
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("level 2")
    background_image = pygame.image.load("level 2.png")
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        background_image = pygame.image.load("level 2.png")
        screen_width, screen_height = screen.get_size()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))
        background_image = pygame.image.load("level 2.png")

    clock = pygame.time.Clock()

    boss_x = 1000
    boss_y = 450
    boss = Boss(boss_x, boss_y, screen)

    # Load animations
    idle_frames = load_animation('adam_idle-sheet.png', 420, 998)
    walk_frames = load_animation('adam_walk_1-sheet.png', 410, 998)
    jump_frames = load_animation('adam_jump-sheet.png', 416, 892)
    double_jump_frames = load_animation('adam_double-sheet.png', 600, 797)
    hit_frames = load_animation('adam_hit_sheet.png', 870, 986, scale_factor=0.15)
    hidden = load_animation('lose play.png', 870, 986)


    music = "level 2.mp3"

    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    if mute_state:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)

    # Offset to move spritesheets down
    OFFSET_Y = 200

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



    health = 350  # Initialize health



    # Create "monster_num" monsters at v

    # Load tilemap and collidable tiles
   
    # Load gun image
    gun_image = pygame.image.load("gun.png")
    gun_image = pygame.transform.scale(gun_image, (70, 90))  # Adjust the size as needed

    bullets = []
    max_bullets = 1  # Limit the number of bullets

    frame = current_frames[frame_index]
    player_mask = pygame.mask.from_surface(frame)

    player_mask_surface = player_mask.to_surface()
    boss_mask_surface = boss.Mask.to_surface()
    
    # Load key images and scale
    key1 = pygame.image.load("key1.png")
    key1 = pygame.transform.scale(key1, (100, 100))
    key2 = pygame.image.load("key2.png")
    key2 = pygame.transform.scale(key2, (100, 100))
    key3 = pygame.image.load("key3.png")
    key3 = pygame.transform.scale(key3, (100, 100))

    # Set key positions
    key1_rect = key1.get_rect(topleft=(100, 500))
    key2_rect = key2.get_rect(topleft=(300, 500))
    key3_rect = key3.get_rect(topleft=(500, 500))

    # Track key collection
    key1_collected = False
    key2_collected = False
    key3_collected = False
    collected_keys = 0

    # Load and position the door
    door = pygame.image.load("door.png")
    door_rect = door.get_rect(topleft=(600, 200))
    door_unlocked = False  # NEW FLAG


    # Main loop
    while True:
        if return_to_main_menu:
            return_to_main_menu = False
            main_menu_active = True
            break
        if main_menu:
            main_menu = False
            running2 = True

        underoos = True

        screen.blit(background_image, (0, 0))

        if boss.health > 50:
            boss.phase1()
        elif boss.health > 30:
            boss.phase2(player_x, player_y)
        else:
            boss.phase3(player_x, player_y)

        if boss.health < 0:
            boss.death()

            # Update player rect each frame
            player_rect = pygame.Rect(
                player_x - idle_frames[0].get_width() // 2,
                player_y - idle_frames[0].get_height() // 2,
                idle_frames[0].get_width(),
                idle_frames[0].get_height()
            )

            # KEY COLLECTION CHECKS
            if not key1_collected and player_rect.colliderect(key1_rect):
                key1_collected = True
                collected_keys += 1

            if not key2_collected and player_rect.colliderect(key2_rect):
                key2_collected = True
                collected_keys += 1

            if not key3_collected and player_rect.colliderect(key3_rect):
                key3_collected = True
                collected_keys += 1

            # DOOR UNLOCK TRIGGER
            if collected_keys == 3:
                door_unlocked = True

            # DRAW UNCOLLECTED KEYS
            if not key1_collected:
                screen.blit(key1, key1_rect.topleft)
            if not key2_collected:
                screen.blit(key2, key2_rect.topleft)
            if not key3_collected:
                screen.blit(key3, key3_rect.topleft)

            # DRAW DOOR IF UNLOCKED
            if door_unlocked:
                screen.blit(door, door_rect.topleft)

                # DOOR COLLISION
                if player_rect.colliderect(door_rect):
                    finalle()


                

        



        player_rect = pygame.Rect(player_x - idle_frames[0].get_width() // 2, player_y - idle_frames[0].get_height() // 2, idle_frames[0].get_width(), idle_frames[0].get_height())        

        #  This part should always run, no matter the phase:
        for bullet in boss.boss_bullets[:]:
            bullet.move()
            bullet.draw()
            player_rect = pygame.Rect(player_x - idle_frames[0].get_width() // 2, player_y - idle_frames[0].get_height() // 2, idle_frames[0].get_width(), idle_frames[0].get_height())

            if player_rect.colliderect(bullet.rect):
                health -= 23
                boss.boss_bullets.remove(bullet)


        boss.draw()





        keys = pygame.key.get_pressed()

        # Draw health bar
        pygame.draw.rect(screen, "red", (20, 20, 350, 50))
        pygame.draw.rect(screen, "green", (20, 20, health, 50))

        pygame.draw.rect(screen, "red", (210, 130, 810, 10))
        pygame.draw.rect(screen, "green", (210, 130, boss.health * 9, 10))

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
            if player_y + player_dy >= screen_height // 2 + OFFSET_Y:  # Lower the player by 20 pixels
                player_y = screen_height // 2 + OFFSET_Y
                is_jumping = False
                jump_count = 0
                jump_velocity = -30
                player_dy = 0


        # Create hitboxes for player and monsters
        player_rect = pygame.Rect(player_x - idle_frames[0].get_width() // 2, player_y - idle_frames[0].get_height() // 2, idle_frames[0].get_width(), idle_frames[0].get_height())
       

        # Check for collision with collidable tiles
        player_rect.x += player_dx
        player_rect.y += player_dy


        # Update player position
        player_x = player_rect.centerx
        player_y = player_rect.centery

        player_x = max(0, min(player_rect.centerx, screen_width - idle_frames[0].get_width()))



        if health < 0:
            health = 0  # Ensure health doesn't go below 0
            if health == 0:
                current_state = "hidden"
                current_frames = hidden
                show_losing_page2()
                health = 350
                return

        last_hit_time = 0  # Initialize a variable to track the last hit time
        hit_cooldown = 1  # Cooldown in seconds

# Inside the collision handling logic
        current_time = time.time()
        if current_time - last_hit_time > hit_cooldown:
            last_hit_time = current_time

        if boss.Mask is None:
    # Initialize or assign a valid mask to boss.Mask
            boss.Mask = pygame.mask.from_surface(boss.rotated_rect)  # Example initialization

    
        offset1 = (
            int(player_rect.left - boss.rotated_rect.left),
            int(player_rect.top - boss.rotated_rect.top)
        )
        if player_mask.overlap(boss.Mask, offset1):
            # The error in the line `if player_mask.overlap(boss.Mask, offset1):` is that `player_mask` is not defined anywhere in the code.  
            # To fix this, you need to create a mask for the player sprite using `pygame.mask.from_surface()`.

            # Example Fix:
            # Assuming `frame` is the current player sprite being rendered:
            player_mask = pygame.mask.from_surface(frame)

            # Ensure this line is placed before the collision check:
            if player_mask.overlap(boss.Mask, offset1):
               health -= 3.5


        for bullet in bullets[:]:
            bullet.width = 70
            bullet.height = 70
            bullet.move()
            bullet.draw()
            if bullet.x < 0 or bullet.x > screen_width:
                bullets.remove(bullet)

            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)


            # Check for pixel-perfect collision
            offset = (int(bullet_rect.x - boss.rotated_rect.x), int(bullet_rect.y - boss.rotated_rect.y))
            if boss.Mask.overlap(pygame.mask.from_surface(pygame.Surface((bullet.width, bullet.height))), offset):
                boss.hit()
                if bullet in bullets:
                    bullets.remove(bullet)

            

   
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
            # Fix for the "integer modulo by 0" error in the animation frame update logic.
            if current_frames:  # Ensure current_frames is not empty
                if frame_timer >= 5:  # Change frame every 5 ticks
                    frame_index = (frame_index + 1) % len(current_frames)  # Safe modulo operation
                    frame_timer = 0
            else:
                print("Error: current_frames is empty. Cannot update animation frames.")

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

def main_menu():
    global hand
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

main_menu()



level = 1

while True:
    if main_menu_active:
        main_menu()
    elif level == 1:
        play()
        main_menu_active = False
        underoos = False
    elif level == 2:
        level2()























































    
















    













    


































