import random

def shuffle_puzzle(size=3):
    """
    Mélange les pièces d'un puzzle de taille donnée.
    Retourne un tableau 2D mélangé.
    """
    numbers = list(range(size * size))  # Liste des nombres de 0 à size*size-1
    random.shuffle(numbers)  # Mélange aléatoire
    return [numbers[i:i + size] for i in range(0, len(numbers), size)]


def is_solvable(puzzle):
    """
    Vérifie si un puzzle est solvable.
    Basé sur le nombre d'inversions.
    """
    # Transformer le puzzle en une liste plate
    flat_puzzle = [num for row in puzzle for num in row if num != 0]

    # Compter les inversions
    inversions = 0
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1

    # Si la taille du puzzle est impaire, le nombre d'inversions doit être pair
    if len(puzzle) % 2 != 0:
        return inversions % 2 == 0

    # Si la taille du puzzle est paire, prenez en compte la ligne de l'espace vide
    else:
        empty_row = next(i for i, row in enumerate(puzzle) if 0 in row)
        if empty_row % 2 == 0:  # Ligne paire
            return inversions % 2 != 0
        else:  # Ligne impaire
            return inversions % 2 == 0


def find_empty_space(puzzle):
    """
    Trouve les coordonnées de l'espace vide (valeur 0) dans le puzzle.
    """
    for i, row in enumerate(puzzle):
        for j, val in enumerate(row):
            if val == 0:
                return i, j


def is_puzzle_solved(puzzle):
    """
    Vérifie si le puzzle est résolu.
    Les pièces doivent être en ordre croissant, avec 0 en dernière position.
    """
    size = len(puzzle)
    flat_puzzle = [num for row in puzzle for num in row]
    return flat_puzzle == list(range(1, size * size)) + [0]
