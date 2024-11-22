import pygame

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50,105,6)

def show_menu(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    
    # Texte du menu
    text0 = font.render("Choisissez une dimension :", True, GREEN)
    text1 = font.render("1. 3x3 (8-puzzle)", True, BLACK)
    text2 = font.render("2. 4x4 (15-puzzle)", True, BLACK)
    
    # Positions des options
    screen.blit(text0, (50,100))
    screen.blit(text1, (100, 200))
    screen.blit(text2, (100, 300))
    pygame.display.flip()
    
    # Retourne les zones des options pour la détection des clics
    return {
        "3x3": pygame.Rect(50, 100, text1.get_width(), text1.get_height()),
        "4x4": pygame.Rect(50, 200, text2.get_width(), text2.get_height())
    }

def select_puzzle_size(screen):
    while True:
        # Affiche le menu et récupère les zones des options
        zones = show_menu(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Détection des clics de souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Position de la souris
                if zones["3x3"].collidepoint(mouse_pos):
                    return 3
                elif zones["4x4"].collidepoint(mouse_pos):
                    return 4
            
            # Détection des touches clavier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Choix 3x3
                    return 3
                elif event.key == pygame.K_2:  # Choix 4x4
                    return 4
                elif event.key == pygame.K_ESCAPE:  # Quitter le jeu
                    pygame.quit()
                    exit()
