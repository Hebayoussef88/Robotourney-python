import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
px,py,is_jump,jump_force,gravity,pj=100,500,False,-10,0.5,0
run=True
while run:
    screen.fill((100,100,0))
    platform = [pygame.draw.rect(screen,(0,0,0),(100,550,150,10)),
    pygame.draw.rect(screen,(0,0,0),(250,450,150,10)),
    pygame.draw.rect(screen,(0,0,0),(400,350,150,10)),
    pygame.draw.rect(screen,(0,0,0),(550,250,150,10)),
    pygame.draw.rect(screen,(0,0,0),(700,150,150,10))]
    goal = pygame.draw.rect(screen,(0,200,0),(750,20,50,50))
    player = pygame.draw.rect(screen,(200,0,0),(px,py,50,50))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and is_jump == True:
        pj = jump_force
        is_jump = False
    
    if keys[pygame.K_LEFT]:
        px -= 1
    if keys[pygame.K_RIGHT]:
        px += 1
    
    pj +=gravity
    py += pj
    is_jump = False
    for p in platform:
        if pygame.Rect(px,py,50,50).colliderect(p) and pj>0:
            py = p.top - 50
            pj=0
            is_jump = True
    if pygame.Rect(px,py,50,50).colliderect(goal):
        print("You win")
        run=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    pygame.time.delay(10)
screen.fill((0.255,0))
pygame.time.delay(500)
