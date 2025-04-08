import pygame, pygame.midi, time, random, math

# Initialize
pygame.init()
pygame.midi.init()
pygame.font.init()
audio = pygame.midi.Output(0)
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Simon Say Game")
audio.set_instrument(4, 14)

# Colors and Sounds
colors = [(150, 0, 0), (0, 150, 0), (0, 0, 150), (150, 150, 0)]
sounds = [52, 57, 62, 64]

# Button Class
class Button:
    def __init__(self, i):
        self.x = 200 * (i % 2)
        self.y = 200 * (i // 2)
        self.color = colors[i]
        self.sound = sounds[i]
        self.rect = pygame.Rect((self.x, self.y), (200, 200))
        self.draw()

    def draw(self, lit=False, wait=0):
        bright = tuple(255 if i else 0 for i in self.color)
        color = bright if lit else self.color

        if lit:
            audio.note_on(self.sound, 127, 1)
        else:
            audio.note_off(self.sound, 127, 1)

        pygame.draw.rect(screen, color, self.rect)
        pygame.display.update()
        time.sleep(wait)

# Exit function
def end():
    audio.close()
    pygame.midi.quit()
    pygame.quit()
    quit()

# End Screen
def end_screen(streak, result='Won', fsize=40):
    texts = [f'You {result}!', f'Sequence: {streak}/8']
    font = pygame.font.SysFont('Arial', fsize)

    for i, text in enumerate(texts):
        surf = font.render(text, True, (0, 0, 0))
        screen.blit(surf, (100, 70 + 30 * i))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()

# Main Game Loop
def simon():
    player, wrong = False, False
    seq = []
    correct = 0
    tile = [Button(i) for i in range(len(colors))]

    while True:
        if player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for t in tile:
                        if t.rect.collidepoint(event.pos):
                            t.draw(lit=True)
                            if t == seq[correct]:
                                correct += 1
                            else:
                                wrong = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    [t.draw() for t in tile]
                    if wrong:
                        end_screen(correct, result="Lose")
                    else:
                        correct = 0
                        player = False
        else:
            chain = len(seq)
            p = math.exp(-0.1 * chain)
            if chain == 8:
                end_screen(chain)
            time.sleep(0.1 + p)
            seq.append(random.choice(tile))
            for t in seq:
                t.draw(lit=True, wait=p)
                t.draw(wait=0.1 * p)
            player = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()

        pygame.display.update()

# Start the game
simon()



