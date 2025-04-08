import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 100, 100)

# Maze layout (1 = wall, 0 = path, 2 = goal)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,1]
]

# Player position
player_pos = [1, 1]

# Game loop setup
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # Draw maze
    for row in range(ROWS):
        for col in range(COLS):
            tile = maze[row][col]
            color = WHITE if tile == 1 else BLACK
            if tile == 2:
                color = GREEN
            pygame.draw.rect(screen, color, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_pos[1]*TILE_SIZE, player_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]: dy = -1
    if keys[pygame.K_RIGHT]: dy = 1
    if keys[pygame.K_UP]: dx = -1
    if keys[pygame.K_DOWN]: dx = 1

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < ROWS and 0 <= new_y < COLS:
        if maze[new_x][new_y] != 1:
            player_pos = [new_x, new_y]

    # Win condition
    if maze[player_pos[0]][player_pos[1]] == 2:
        print("You win!")
        pygame.time.wait(1000)
        running = False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

