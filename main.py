import pygame
import time
from copy import deepcopy
from square import Square
from solve import Solver
from GUI2 import GUI

# Color RGBs
BLACK = (20, 20, 20)
WHITE = (250, 250, 250)
BLUE = (30, 144, 255)
RED = (240, 20, 0)
GRAY = (200, 200, 200)

# Global Variables
FPS = 60
BUFFER = 3
THICK_LINE = 4
FONT_SIZE = 32
SELECTED = [0, 0]
SOLVED_BOARD = solve(deepcopy(original_board))
game_active = True

# Pygame Display Settings
WIDTH, HEIGHT = (Square.block_width * 9) + (2 * THICK_LINE), (Square.block_height * 9) + (2 * THICK_LINE)
WIN = pygame.display.set_mode((WIDTH, HEIGHT + 40))
pygame.display.set_caption('Sudoku')

def main(gui, solver):
    pygame.init()
    run = True
    pos = 0
    changed = False
    start = time.time()
    global game_active
    grid = deepcopy(original_board)
    empty = 0
    is_solved = False
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            grid[r][c] = Square(r, c, original_board[r][c])
            if not original_board[r][c]:
                empty += 1

    while run:
        if game_active:
            if not is_solved:
                display_time = round(time.time() - start)
            changed = False
            val = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    val = handle_inputs(event, grid, deepcopy(original_board))
                if event.type == pygame.MOUSEBUTTONDOWN and pos != pygame.mouse.get_pos():
                    pos = pygame.mouse.get_pos()
                    changed = True
                    
            is_solved = draw_sudoku_grid(grid, pos, changed, empty, None, val)
            if is_solved:
                game_active = False
            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    gui = GUI()
    solver = Solver()
    main(gui, solver)