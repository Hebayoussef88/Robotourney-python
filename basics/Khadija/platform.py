import pygame

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
PLAYER_COLOR = (50, 150, 255)
PLATFORM_COLOR = (100, 100, 100)
GOAL_COLOR = (0, 255, 0)

# Player setup
player = pygame.Rect(100, 500, 40, 40)
vel_y = 0
gravity = 0.8
jump_power = -15
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),         # ground
    pygame.Rect(200, 500, 100, 20),
    pygame.Rect(400, 450, 100, 20),
    pygame.Rect(600, 380, 120, 20),
]

# Goal (flag)
goal = pygame.Rect(700, 340, 30, 40)

# Game loop
running = True
while running:
    screen.fill(SKY)

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_power

    # Apply gravity
    vel_y += gravity
    player.y += vel_y

    # Check collision with platforms
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and vel_y > 0:
            player.bottom = plat.top
            vel_y = 0
            on_ground = True

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, plat)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # Draw goal
    pygame.draw.rect(screen, GOAL_COLOR, goal)

    # Win condition
    if player.colliderect(goal):
        print("YOU WIN!")
        pygame.time.wait(1000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
