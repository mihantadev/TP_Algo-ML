import random
import pygame

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)

def shuffle_puzzle(size=3):
    """
    Mélange les pièces d'un puzzle de taille donnée.
    Retourne un tableau 2D mélangé.
    """
    numbers = list(range(size * size))  # Liste des nombres de 0 à size*size-1
    random.shuffle(numbers)  # Mélange aléatoire
    return [numbers[i:i + size] for i in range(0, len(numbers), size)]


def find_empty_space(puzzle):
    """
    Trouve les coordonnées de l'espace vide (valeur 0) dans le puzzle.
    """
    for i, row in enumerate(puzzle):
        for j, val in enumerate(row):
            if val == 0:
                return i, j


def move(puzzle, direction):
    """
    Déplace une pièce vers une direction (haut, bas, gauche, droite).
    """
    x, y = find_empty_space(puzzle)
    if direction == "up" and x > 0:
        puzzle[x][y], puzzle[x - 1][y] = puzzle[x - 1][y], puzzle[x][y]
    elif direction == "down" and x < len(puzzle) - 1:
        puzzle[x][y], puzzle[x + 1][y] = puzzle[x + 1][y], puzzle[x][y]
    elif direction == "left" and y > 0:
        puzzle[x][y], puzzle[x][y - 1] = puzzle[x][y - 1], puzzle[x][y]
    elif direction == "right" and y < len(puzzle[0]) - 1:
        puzzle[x][y], puzzle[x][y + 1] = puzzle[x][y + 1], puzzle[x][y]


def swap_pieces(puzzle, pos1, pos2):
    """
    Effectue un échange entre deux positions dans le puzzle.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    puzzle[x1][y1], puzzle[x2][y2] = puzzle[x2][y2], puzzle[x1][y1]


def draw_puzzle(screen, puzzle, FONT):
    """
    Dessine le puzzle sur l'écran en utilisant Pygame.
    Utilise la police FONT passée en argument.
    """
    screen.fill(WHITE)
    for i, row in enumerate(puzzle):
        for j, val in enumerate(row):
            if val != 0:
                pygame.draw.rect(screen, BLUE, (j * 100, i * 100, 100, 100))
                text = FONT.render(str(val), True, WHITE)  # Utilisation de la police
                screen.blit(text, (j * 100 + 30, i * 100 + 30))
