import pygame
import random
import time

# Dimensions du puzzle
DIMENSIONS = {3: (3, 3), 4: (4, 4)}

class Puzzle:
    def __init__(self, n, k):
        self.n = n  # Taille du puzzle (3 pour 8-puzzle, 4 pour 15-puzzle)
        self.k = k  # Nombre de déplacements avant swap
        self.size = DIMENSIONS[n]  # Dimensions du puzzle
        self.board = self.generate_board()  # Initialiser le plateau
        self.empty_pos = self.board.index(0)  # Position de la case vide

    def generate_board(self):
        """Générer un puzzle mélangé."""
        numbers = list(range(self.n * self.n))  # Liste de 0 à n*n-1
        random.shuffle(numbers)
        while not self.is_solvable(numbers):
            random.shuffle(numbers)
        return numbers

    def is_solvable(self, board):
        """Vérifier si le puzzle est résolvable."""
        inversions = 0
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if board[i] != 0 and board[j] != 0 and board[i] > board[j]:
                    inversions += 1
        return inversions % 2 == 0

    def swap(self, i, j):
        """Échanger deux cases du puzzle."""
        self.board[i], self.board[j] = self.board[j], self.board[i]

    def move(self, direction):
        """Déplacer une case vide dans la direction spécifiée."""
        empty = self.empty_pos
        row, col = divmod(empty, self.n)

        if direction == 'up' and row > 0:
            new_pos = empty - self.n
        elif direction == 'down' and row < self.n - 1:
            new_pos = empty + self.n
        elif direction == 'left' and col > 0:
            new_pos = empty - 1
        elif direction == 'right' and col < self.n - 1:
            new_pos = empty + 1
        else:
            return  # Mouvement invalide

        self.swap(empty, new_pos)
        self.empty_pos = new_pos

    def draw(self, screen, size=500):
        """Dessiner le puzzle avec Pygame."""
        block_size = size // self.n
        for i in range(self.n):
            for j in range(self.n):
                num = self.board[i * self.n + j]
                x, y = j * block_size, i * block_size
                if num != 0:
                    pygame.draw.rect(screen, (20, 205, 80), (x, y, block_size, block_size), border_radius=10)
                    font = pygame.font.Font(None, 50)
                    text = font.render(str(num), True, (0, 0, 0))
                    screen.blit(text, (x + block_size // 3, y + block_size // 3))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, block_size, block_size), 3, border_radius=10)

    def is_solved(self):
        """Vérifier si le puzzle est résolu."""
        return self.board == list(range(self.n * self.n))

    def solve(self):
        """Résoudre automatiquement le puzzle en remettant les cases dans l'ordre."""
        self.board = list(range(self.n * self.n))  # Réinitialiser le tableau à la solution
        self.empty_pos = self.board.index(0)
        time.sleep(0.8)


def select_puzzle_size():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Sélectionnez la taille du puzzle")

    font = pygame.font.Font(None, 40)
    large_text = font.render("Choisissez la taille:", True, (0, 0, 0))

    button_3x3 = pygame.Rect(100, 100, 200, 50)
    button_4x4 = pygame.Rect(100, 200, 200, 50)

    running = True
    while running:
        screen.fill((255, 255, 255))
        screen.blit(large_text, (100, 50))

        pygame.draw.rect(screen, (20, 205, 80), button_3x3, border_radius=10)
        pygame.draw.rect(screen, (20, 205, 80), button_4x4, border_radius=10)

        text_3x3 = font.render("3x3", True, (255, 255, 255))
        text_4x4 = font.render("4x4", True, (255, 255, 255))

        screen.blit(text_3x3, (160, 115))
        screen.blit(text_4x4, (160, 215))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_3x3.collidepoint(event.pos):
                    return 3
                if button_4x4.collidepoint(event.pos):
                    return 4

        pygame.display.flip()

    pygame.quit()


def select_k_value():
    pygame.init()
    screen = pygame.display.set_mode((420, 250))
    pygame.display.set_caption("Choisir le nombre de déplacements k")

    font = pygame.font.Font(None, 25)
    text = font.render("Entrez nombre déplacements k:", True, (0, 0, 0))
    input_box = pygame.Rect(100, 100, 200, 50)

    k_value = ""
    running = True
    while running:
        screen.fill((255, 255, 255))
        screen.blit(text, (50, 50))

        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        font_input = pygame.font.Font(None, 40)
        txt_surface = font_input.render(k_value, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if k_value.isdigit():
                        return int(k_value)
                    else:
                        k_value = ""  # Efface l'entrée si elle est invalide
                elif event.key == pygame.K_BACKSPACE:
                    k_value = k_value[:-1]
                else:
                    k_value += event.unicode

        pygame.display.flip()

    pygame.quit()
    return 3  # Valeur par défaut si l'utilisateur ferme la fenêtre


def main():
    while True:  # Boucle principale pour revenir à la sélection de la taille
        # Sélection de la taille du puzzle
        n = select_puzzle_size()
        if not n:
            return

        # Sélection du nombre k de déplacements avant swap
        k = select_k_value()

        puzzle = Puzzle(n, k)

        pygame.init()
        screen_size = 650
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Puzzle à glissements")

        # Définition des boutons
        button_back = pygame.Rect(500, 390, 100, 50)
        button_solve = pygame.Rect(500, 450, 150, 50)
        font = pygame.font.Font(None, 40)

        running = True
        while running:
            screen.fill((255, 255, 255))  # Fond blanc
            puzzle.draw(screen)

            # Dessiner les boutons
            pygame.draw.rect(screen, (20, 205, 80), button_back, border_radius=10)
            pygame.draw.rect(screen, (20, 205, 80), button_solve, border_radius=10)
            text_back = font.render("Retour", True, (255, 255, 255))
            text_solve = font.render("Résoudre", True, (255, 255, 255))

            screen.blit(text_back, (button_back.x + 10, button_back.y + 10))
            screen.blit(text_solve, (button_solve.x + 10, button_solve.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.collidepoint(event.pos):
                        running = False  # Fermer cette boucle et revenir à la sélection de la taille
                        break  # Quitter la boucle intérieure pour revenir à l'écran principal
                    if button_solve.collidepoint(event.pos):
                        puzzle.solve()  # Résoudre automatiquement le puzzle

                # Ajouter les contrôles de clavier pour déplacer la case vide
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Touche fléchée haut
                        puzzle.move('up')
                    elif event.key == pygame.K_DOWN:  # Touche fléchée bas
                        puzzle.move('down')
                    elif event.key == pygame.K_LEFT:  # Touche fléchée gauche
                        puzzle.move('left')
                    elif event.key == pygame.K_RIGHT:  # Touche fléchée droite
                        puzzle.move('right')
                        
            pygame.display.flip()

        # Si l'utilisateur quitte ou clique sur "Retour", revenir à la page de sélection
        if not running:
            continue  # Recommencer la boucle et retourner à la sélection de la taille du puzzle

    pygame.quit()



if __name__ == "__main__":
    main()
