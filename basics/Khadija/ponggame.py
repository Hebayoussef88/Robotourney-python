import pygame
pygame.init()
screen  = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ping Pong Game")
font= pygame.font.SysFont("Comic Sans MS", 30)
def showScore():
    text1 = font.render("Player 1 : "+str(p1point),False,(255,255,255))
    text_rext1 = text1.get_rect()
    text_rext1.center = (90,30)
    screen.blit(text1,text_rext1)
    text2 = font.render("Player 2 : "+str(p2point),False,(255,255,255))
    text_rext2 = text2.get_rect()
    text_rext2.center = (700,30)
    screen.blit(text2,text_rext2)
run = True
p1y,p2y,ball_x,ball_y,speed,dx,dy,p1point,p2point=200,200,400,300,0.1,1,1,0,0
while run:
    screen.fill((0,0,0))
    showScore()
    player1=pygame.draw.rect(screen,(255,255,255),[10,p1y,10,130])
    player2=pygame.draw.rect(screen,(255,255,255),[780,p2y,10,130])
    ball= pygame.draw.circle(screen,(255,255,255),[ball_x,ball_y],15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and p1y >0:
        p1y -= 0.2
    if keys[pygame.K_DOWN]and p1y <500:
        p1y += 0.2
    if keys[pygame.K_w]and p2y >0:
        p2y -= 0.2
    if keys[pygame.K_s]and p2y <500:
        p2y += 0.2
    ball_x += speed * dx
    ball_y += speed * dy
    if ball_x > 800:
        ball_x,ball_y =400,300
        dx = -1
        p1point +=1
    if ball_x < 0 :
        ball_x,ball_y =400,300
        dx = 1
        p2point+=1
    if ball_y > 500:
        dy = -1
    if ball_y < 0 :
        dy = 1
    if player1.colliderect(ball):
        dx=1
    if player2.colliderect(ball):
        dx=-1
    pygame.display.update()