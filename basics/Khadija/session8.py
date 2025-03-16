import turtle
import pygame
import random

# Draw background with Turtle
def draw_planet(x, y, color, size):
    turtle.penup()
    turtle.goto(x, y - size)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    turtle.circle(size)
    turtle.end_fill()

def draw_rocket():
    turtle.penup()
    turtle.goto(-200, -100)
    turtle.pendown()
    turtle.color("gray")
    turtle.begin_fill()
    turtle.goto(-180, -50)
    turtle.goto(-220, -50)
    turtle.goto(-200, -100)
    turtle.end_fill()
    turtle.hideturtle()

# Turtle setup
screen = turtle.Screen()
screen.bgcolor("black")
turtle.speed(0)
draw_rocket()
draw_planet(200, 150, "blue", 40)
draw_planet(-150, 200, "red", 50)
turtle.done()

# --- Pygame Part ---
pygame.init()
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Adventure")

# Load spaceship image
spaceship = pygame.image.load("spaceship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceship_x, spaceship_y = 50, HEIGHT // 2

# Load planet image
planet = pygame.image.load("planet.png")
planet = pygame.transform.scale(planet, (50, 50))
planet_x, planet_y = WIDTH - 70, HEIGHT // 2

# Asteroids setup
asteroids = [(random.randint(200, WIDTH - 50), random.randint(0, HEIGHT - 50)) for _ in range(5)]
ast_speed = 2

# Game loop
running = True
while running:
    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_x -= 5
    if keys[pygame.K_RIGHT]:
        spaceship_x += 5
    if keys[pygame.K_UP]:
        spaceship_y -= 5
    if keys[pygame.K_DOWN]:
        spaceship_y += 5

    # Move asteroids
    asteroids = [(x - ast_speed, y) if x > 0 else (WIDTH, random.randint(0, HEIGHT - 50)) for x, y in asteroids]

    # Collision check
    for ax, ay in asteroids:
        if abs(spaceship_x - ax) < 40 and abs(spaceship_y - ay) < 40:
            print("Game Over!")
            running = False

    # Win check
    if abs(spaceship_x - planet_x) < 40 and abs(spaceship_y - planet_y) < 40:
        print("You Win!")
        running = False

    # Draw everything
    win.fill((0, 0, 0))
    win.blit(spaceship, (spaceship_x, spaceship_y))
    win.blit(planet, (planet_x, planet_y))
    for ax, ay in asteroids:
        pygame.draw.circle(win, (255, 0, 0), (ax, ay), 20)

    pygame.display.update()

pygame.quit()
