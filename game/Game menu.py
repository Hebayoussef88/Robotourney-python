def main_menu1():
    global main_menu
    while main_menu:
        pygame.init()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

                clock.tick(60)
                if event.type == pygame.MOUSEBUTTONDOWN:  # Detect single click
                    if mute_rect.collidepoint(event.pos):  # Check if the mute button is clicked
                        mute_state = not mute_state  # Toggle mute state
                if mute_state:
                    # Display the mute button
                    screen.blit(mute, mute_pos)
                else:
                    # Display the unmute button
                    screen.blit(unmute, mute_pos)

        my_text = Font1.render("chronochills", True, (255, 255, 255))
        button_pos = (520, 300)
        button_pos1 = (520, 425)
        button_pos2 = (520, 550)
        button_rect = pygame.Rect(button_pos, play_unclicked.get_size())
        button_rect1 = pygame.Rect(button_pos1, options_unclicked.get_size())
        button_rect2 = pygame.Rect(button_pos2, quit_unclicked.get_size())


    
        screen.blit(screen1, (0,0))
        screen.blit(logo, (318, 1))
        screen.blit(play_unclicked, (button_x1, button_y1))
        screen.blit(options_unclicked, (button_x2, button_y2))
        screen.blit(quit_unclicked, (button_x3, button_y3))
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(hand)
            screen.blit(play_clicked, (button_x1, button_y1))
            if pygame.mouse.get_pressed()[0]:
                main_menu = False
            
            
        
    
        elif button_rect1.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(hand)
            screen.blit(options_clicked, (button_x2, button_y2))
            if pygame.mouse.get_pressed()[0]:
                options()
        elif button_rect2.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(hand)
            screen.blit(quit_clicked, (button_x3, button_y3))
            if pygame.mouse.get_pressed()[0]:
                quit()


        else:
            pygame.mouse.set_cursor()
            screen.blit(play_unclicked, (button_x1, button_y1))
            screen.blit(options_unclicked, (button_x2, button_y2))
            screen.blit(quit_unclicked, (button_x3, button_y3))


        pygame.display.update()

main_menu1()
