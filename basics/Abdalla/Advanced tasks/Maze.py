import pygame

pygame.init()


size, width, height = 40, 600, 300
row, col = height // size, width // size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

font = pygame.font.SysFont(None, 60)

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,1,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,0,0,0,1,1,1,1,0,1,2,1],
    [1,1,1,1,0,1,1,1,1,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,1,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,1,1,0,1,1],
    [1,1,1,1,0,0,1,1,1,0,0,0,0,1,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,1,1]
]

px, py = 1, 1

run = True
won = False
while run:
    screen.fill((255, 255, 255))
    
    
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (c * size, r * size, size, size))
            elif maze[r][c] == 2:
                pygame.draw.rect(screen, (0, 255, 0), (c * size, r * size, size, size))
    
  
    pygame.draw.rect(screen, (255, 0, 0), (px * size, py * size, size, size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and not won:
            nx, ny = px, py
            if event.key == pygame.K_LEFT:
                nx -= 1
            elif event.key == pygame.K_RIGHT:
                nx += 1
            elif event.key == pygame.K_UP:
                ny -= 1
            elif event.key == pygame.K_DOWN:
                ny += 1
            if maze[ny][nx] != 1:
                px, py = nx, ny
            if maze[py][px] == 2:
                print("You Win!")
                won = True

    if won:
        win_text = font.render("You Won!", True, (255, 255, 255))
        screen.fill((0, 200, 0))
        screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))

    pygame.display.update()

    if won:
        pygame.time.wait(2000)
        run = False

pygame.quit()
