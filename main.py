import pygame
import random
import heapq
import time

# Dimensions du puzzle
DIMENSIONS = {3: (3, 3), 4: (4, 4)}


class Puzzle:
    def __init__(self, n):
        self.n = n  # Taille du puzzle (3 pour 8-puzzle, 4 pour 15-puzzle)
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
                    pygame.draw.rect(screen, (20, 205, 80), (x, y, block_size, block_size))
                    font = pygame.font.Font(None, 50)
                    text = font.render(str(num), True, (0, 0, 0))
                    screen.blit(text, (x + block_size // 3, y + block_size // 3))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, block_size, block_size), 2)


class PuzzleSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.goal_state = self.get_goal_state()
        self.start_state = tuple(self.puzzle.board)

    def get_goal_state(self):
        """Retourner l'état cible du puzzle."""
        return tuple(range(self.puzzle.n * self.puzzle.n))

    def get_heuristic(self, state):
        """Calculer la distance de Manhattan."""
        distance = 0
        for i, val in enumerate(state):
            if val != 0:
                target_pos = self.goal_state.index(val)
                target_row, target_col = divmod(target_pos, self.puzzle.n)
                current_row, current_col = divmod(i, self.puzzle.n)
                distance += abs(target_row - current_row) + abs(target_col - current_col)
        return distance

    def get_neighbors(self, state):
        """Retourner les voisins (états voisins)."""
        neighbors = []
        empty_pos = state.index(0)
        row, col = divmod(empty_pos, self.puzzle.n)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.puzzle.n and 0 <= new_col < self.puzzle.n:
                new_pos = new_row * self.puzzle.n + new_col
                new_state = list(state)
                new_state[empty_pos], new_state[new_pos] = new_state[new_pos], new_state[empty_pos]
                neighbors.append(tuple(new_state))

        return neighbors

    def solve(self):
        """Résoudre le puzzle avec l'algorithme A*."""
        open_list = []
        heapq.heappush(open_list, (self.get_heuristic(self.start_state), 0, self.start_state, []))
        closed_list = set()

        while open_list:
            _, cost, current_state, path = heapq.heappop(open_list)

            if current_state == self.goal_state:
                return path  # Retourner le chemin

            closed_list.add(current_state)

            for neighbor in self.get_neighbors(current_state):
                if neighbor not in closed_list:
                    new_cost = cost + 1
                    new_heuristic = new_cost + self.get_heuristic(neighbor)
                    heapq.heappush(open_list, (new_heuristic, new_cost, neighbor, path + [neighbor]))

        return None  # Aucun chemin trouvé


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

        pygame.draw.rect(screen, (20, 205, 80), button_3x3)
        pygame.draw.rect(screen, (20, 205, 80), button_4x4)

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


def main():
    # Sélection de la taille du puzzle
    n = select_puzzle_size()
    if not n:
        return

    puzzle = Puzzle(n)

    pygame.init()
    screen_size = 800
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Puzzle à glissements")

    # Bouton de résolution
    solve_button = pygame.Rect(550, 450, 120, 40)

    running = True
    solving = False
    solution = []

    while running:
        screen.fill((255, 255, 255))  # Fond blanc
        puzzle.draw(screen)

        pygame.draw.rect(screen, (20, 205 , 80), solve_button)
        font = pygame.font.Font(None, 30)
        solve_text = font.render("Résoudre", True, (0, 0, 0))
        screen.blit(solve_text, (solve_button.x + 30, solve_button.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not solving:
                if event.key == pygame.K_UP:
                    puzzle.move('up')
                elif event.key == pygame.K_DOWN:
                    puzzle.move('down')
                elif event.key == pygame.K_LEFT:
                    puzzle.move('left')
                elif event.key == pygame.K_RIGHT:
                    puzzle.move('right')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solve_button.collidepoint(event.pos) and n == 3:
                    solving = True
                    solver = PuzzleSolver(puzzle)
                    solution = solver.solve()

        # Résolution automatique
        if solving and solution:
            time.sleep(0.8)
            next_move = solution.pop(0)
            puzzle.board = list(next_move)
            puzzle.empty_pos = puzzle.board.index(0)
            if not solution:
                solving = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
