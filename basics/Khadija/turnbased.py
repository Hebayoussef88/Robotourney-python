import pygame

# Init
pygame.init()

# Grid settings
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
TILE_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Strategy Game")

# Colors
WHITE = (240, 240, 240)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
SELECTED = (255, 255, 0)

# Units: list of [row, col, team]
units = [
    [0, 0, "red"],
    [0, 1, "red"],
    [7, 7, "blue"],
    [7, 6, "blue"]
]

selected = None
current_turn = "red"

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw units
    for unit in units:
        x, y = unit[1] * TILE_SIZE, unit[0] * TILE_SIZE
        color = RED if unit[2] == "red" else BLUE
        pygame.draw.circle(screen, color, (x + TILE_SIZE//2, y + TILE_SIZE//2), TILE_SIZE//3)

    # Draw selected highlight
    if selected:
        row, col = selected
        pygame.draw.rect(screen, SELECTED, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // TILE_SIZE
            row = mouse_y // TILE_SIZE

            if selected:
                # Try to move
                for u in units:
                    if u[0] == selected[0] and u[1] == selected[1]:
                        # Check for enemy at target
                        for enemy in units[:]:
                            if enemy[0] == row and enemy[1] == col and enemy[2] != current_turn:
                                units.remove(enemy)
                        # Check tile is empty or enemy
                        occupied = any(u[0] == row and u[1] == col and u[2] == current_turn for u in units)
                        if not occupied:
                            u[0], u[1] = row, col
                            selected = None
                            current_turn = "blue" if current_turn == "red" else "red"
                        break
            else:
                # Select own unit
                for u in units:
                    if u[0] == row and u[1] == col and u[2] == current_turn:
                        selected = (row, col)

    # Win check
    red_units = any(u[2] == "red" for u in units)
    blue_units = any(u[2] == "blue" for u in units)
    if not red_units:
        print("Blue wins!")
        pygame.time.wait(1000)
        running = False
    elif not blue_units:
        print("Red wins!")
        pygame.time.wait(1000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
