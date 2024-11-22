import pygame
from game_logic import shuffle_puzzle, move, swap_pieces, draw_puzzle
from menu import select_puzzle_size

# Initialisation de Pygame
pygame.init()

# Initialiser la police après pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Puzzle Game")
FONT = pygame.font.Font(None, 36)  # Initialisation correcte de la police

# Sélection de la taille du puzzle
puzzle_size = select_puzzle_size(screen)  # Exemple, vous pouvez permettre à l'utilisateur de sélectionner la taille
print(f"Puzzle choisi : {puzzle_size}x{puzzle_size}")
puzzle = shuffle_puzzle(size=puzzle_size)
moves = 0
k = 10  # Un swap tous les 10 déplacements

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(puzzle, "up")
                moves += 1
            elif event.key == pygame.K_DOWN:
                move(puzzle, "down")
                moves += 1
            elif event.key == pygame.K_LEFT:
                move(puzzle, "left")
                moves += 1
            elif event.key == pygame.K_RIGHT:
                move(puzzle, "right")
                moves += 1

            # Effectuer un swap tous les k déplacements
            if moves % k == 0:
                swap_pieces(puzzle, (0, 0), (1, 1))  # Exemple de positions à échanger

    # Dessiner le puzzle en passant FONT comme argument
    draw_puzzle(screen, puzzle, FONT)
    pygame.display.flip()

pygame.quit()


