import pygame
import random

pygame.init()

screen_width = 1860
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Turn Based Game")

meadow_backround = pygame.image.load("meadow.png")
grass_backround = pygame.image.load("grass layer.png")

player_x = 600
player_y = 600
enemy_x = 1700
enem_y = 450
player_speed = 3

grass_mask = pygame.mask.from_surface(grass_backround)

def battle():
    global screen
    BACKROUND = pygame.image.load("metal effect.png")
    turn = 1
    pc = 200
    ec = 370
    ph = 20
    eh = 20
    move = 0
    final_move = None
    final_move2 = None
    play = True
    turn_r = False
    damage_applied = False  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if play == True and turn == 1 and turn_r == False:
                if event.type == pygame.KEYDOWN:
                    if move < 2 and event.key == pygame.K_RIGHT:
                        pc += 450
                        move += 1
                    if move > 0 and event.key == pygame.K_LEFT:
                        pc -= 450
                        move -= 1
                    if event.key == pygame.K_y:
                        if move == 0:
                            final_move = "shield"
                        elif move == 1:
                            final_move = "attack"
                        elif move == 2:
                            final_move = "special attack"
                        play = False
                        turn = 2
                        turn_r = False
                        damage_applied = False 

        if play == False and turn == 2 and turn_r == False:
            choice = random.randint(1, 3)
            if choice == 1:
                ec = 370
                final_move2 = "shield"

            elif choice == 2:
                ec = 820
                final_move2 = "attack"
            elif choice == 3:
                ec = 1270
                final_move2 = "special attack"
            turn = 1
            turn_r = True 
            damage_applied = False

        if turn_r and not damage_applied:
            if final_move2 == "shield" and final_move in ["attack", "special attack", "shield"]:
                eh -= 0
                play = True        
                turn_r = False     
                move = 0           
                pc = 200           

            else:
                if final_move == "attack":
                    eh -= 5
                    play = True        
                    turn_r = False    
                    move = 0          
                    pc = 200           

                elif final_move == "special attack":
                    eh -= 10
                    play = True         
                    turn_r = False     
                    move = 0            
                    pc = 200           

            if final_move == "shield" and final_move2 in ["attack", "special attack", "shield"]:
                ph -= 0
                play = True         
                turn_r = False     
                move = 0           
                pc = 200           

            else:
                if final_move2 == "attack":
                    ph -= 5
                    play = True         
                    turn_r = False     
                    move = 0           
                    pc = 200           

                elif final_move2 == "special attack":
                    ph -= 10
                    play = True         
                    turn_r = False      
                    move = 0            
                    pc = 200            


            damage_applied = True 

            if ph < 0:
                print("you lose")
                quit()
            elif eh < 0:
                print("you win")
                quit()
            elif ph < 0 and eh < 0:
                print("draw")
                quit()


        screen.blit(BACKROUND, (0,0))
        player_choice = pygame.draw.rect(screen, (111, 111, 111), [pc, 825, 40, 40])
        enemy_choice = pygame.draw.rect(screen, (111, 111, 111), [ec, 140, 40, 40])
        player_red = pygame.draw.rect(screen, (200, 0, 0), [1100, 650, 400, 40])
        player_green = pygame.draw.rect(screen, (0, 200, 0), [1100, 650, ph*20, 40])
        enemy_red = pygame.draw.rect(screen, (200, 0, 0), [350, 300, 400, 40])
        enemy_green = pygame.draw.rect(screen, (0, 200, 0), [350, 300, eh*20, 40])

        pygame.display.update()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        keys = pygame.key.get_pressed()
        if grass_mask.get_at((player_x, player_y)):
            if keys[pygame.K_w]:
                player_y -= 5 * player_speed
            elif keys[pygame.K_s]:
                player_y += 5 * player_speed
            if keys[pygame.K_a]:
                player_x -= 5 * player_speed
            elif keys[pygame.K_d]:
                player_x += 5 * player_speed

            if player_y > 510:
                player_y -= 50
            if player_y < 445:
                player_y += 50
            if player_x < 240:
                player_x += 50

        
    screen.blit(meadow_backround, (0, 0))
    screen.blit(grass_backround, (0, 0))
    player = pygame.draw.rect(screen, (0, 200, 0), [player_x, player_y, 70, 70])
    enemy = pygame.draw.rect(screen, (200, 0, 0), [enemy_x, enem_y, 70, 70])
    pygame.display.update()

    if player.colliderect(enemy):
        battle()