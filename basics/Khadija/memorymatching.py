import pygame
import random
pygame.init()
screen = pygame.display.set_mode((500,600))
pygame.display.set_caption("Memory Match Game")
Card_size,margin,first_card,second_card,attempts,matched=100,20,None,None,0,0

def generate_position():
    position = []
    for i in range (4):
        for j in range(4):
            x = margin + j * (Card_size + margin)
            y = margin + i * (Card_size + margin)
            position.append((x,y))
    return position
def choose_pairs():
    symbols=list(range(8))*2
    random.shuffle(symbols)
    return symbols
class card:
    def __init__(self,symbol,position):
        self.symbol= symbol
        self.position = position
        self.rect =  pygame.Rect(position[0],position[1],Card_size,Card_size)
        self.revealed = False
        self.matched = False
    def draw(self,screen):
        if self.revealed or self.matched:
            pygame.draw.rect(screen,(255,255,255),self.rect)
            font = pygame.font.Font(None, 70)
            text = font.render(str(self.symbol),True,(0,0,0))
            screen.blit(text,(self.position[0]+35,self.position[1]+25))
        else:
            pygame.draw.rect(screen,(0,255,0),self.rect)

positions =generate_position()
pairs = choose_pairs()
cards = [card(pairs[i],positions[i]) for i in range(16)]


run=True
while run:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if first_card is None or (first_card and second_card is None):
                for c in cards:
                    if c.rect.collidepoint(event.pos) and not c.revealed and not c.matched:
                        c.revealed = True
                        if first_card is None:
                            first_card = c
                        elif second_card is None:
                            second_card = c
                            attempts +=1

    if first_card and second_card:
        if first_card.symbol == second_card.symbol:
            first_card.matched =True
            second_card.matched = True
            first_card = None
            second_card=None
            matched+=1
        else:
            first_card.revealed = False
            second_card.revealed=False
            first_card = None
            second_card=None
    for ca in cards:
        ca.draw(screen)
    font = pygame.font.Font(None, 35)
    text = font.render("Score : "+str(matched),True,(255,255,255))
    screen.blit(text,(40,550))
    if matched == 8:
        screen.fill((255,255,255))
        font = pygame.font.Font(None, 50)
        text = font.render("You Win",True,(0,0,0))
        screen.blit(text,(150,150))
    pygame.display.update()