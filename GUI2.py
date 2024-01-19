import pygame
import time
from copy import deepcopy
from square import Square

BLACK = (20, 20, 20)
WHITE = (250, 250, 250)
BLUE = (30, 144, 255)
RED = (240, 20, 0)
GRAY = (200, 200, 200)

FPS = 60
BUFFER = 3
THICK_LINE = 4
FONT_SIZE = 32
SELECTED = [0, 0]
SOLVED_BOARD = solve(deepcopy(original_board))
game_active = True

WIDTH, HEIGHT = (Square.block_width * 9) + (2 * THICK_LINE), (Square.block_height * 9) + (2 * THICK_LINE)
WIN = pygame.display.set_mode((WIDTH, HEIGHT + 40))
pygame.display.set_caption('Sudoku')

class GUI:
    def __init__(self, solver) -> None:
        self.solver = solver

    def draw_sudoku_grid(self, grid, pos, changed, empty, time=None, val=0):
        WIN.fill(WHITE)

        # Checking if a new value has been added
        sq = grid[SELECTED[0]][SELECTED[1]]
        if val and not sq.value:
            if val == SOLVED_BOARD[SELECTED[0]][SELECTED[1]]:
                sq.value = val
                empty -= 1
            else:
                Square.strikes += 1

        # Check if selected grid spot has changed and make changes accordingly
        if changed:
            grid[SELECTED[0]][SELECTED[1]].selected = False
            x = pos[0] // 52
            y = pos[1] // 52
            grid[y][x].selected = True
            SELECTED[1] = x
            SELECTED[0] = y

        # Printing out the grid
        r_pos = 0
        c_pos = 0
        font = pygame.font.SysFont('Calibri', FONT_SIZE, bold=False)
        for x in range(len(grid)):
            if x % 3 == 0 and x < 8 and x > 0:
                r_pos += int(THICK_LINE / 2) - 1
                pygame.draw.line(WIN, BLACK, (0, r_pos), (WIDTH, r_pos), THICK_LINE)
                r_pos += int(THICK_LINE / 2) + 1
            c_pos = 0
            for y in range(len(grid[0])):
                sq = grid[x][y]
                if sq.rect is None:
                    sq.set_rect(c_pos, r_pos)
                if sq.selected:
                    WIN.fill(GRAY, sq.rect)
                else:
                    WIN.fill(WHITE, sq.rect)
                pygame.draw.rect(WIN, BLACK, sq.rect, 1)
                if sq.value:
                    if not original_board[x][y]:
                        color = BLUE
                    else:
                        color = BLACK
                    text = font.render(str(sq.value), True, color)
                    rect = text.get_rect(center=(sq.rect.x + int(Square.block_width / 2), sq.rect.y + int(Square.block_height / 2)))
                    WIN.blit(text, rect)
                c_pos += Square.block_height
                if (y + 1) % 3 == 0 and y < 8 and y > 0:
                    c_pos += int(THICK_LINE / 2) - 1
                    pygame.draw.line(WIN, BLACK, (c_pos, 0), (c_pos, HEIGHT), THICK_LINE)
                    c_pos += int(THICK_LINE / 2) + 1
            r_pos += Square.block_width

        is_solved = False
        if not empty:
            self.solved(time)
            is_solved = True

        # Handling Strikes
        if Square.strikes >= 0 and Square.strikes < 3:
            s = ''
            for _ in range(Square.strikes):
                s += 'X '
            text = font.render(s, True, RED)
            rect = text.get_rect(center=(20 + (Square.strikes * 14), HEIGHT + 20))
            WIN.blit(text, rect)
            
            # Printing Time
            if time and not is_solved:
                text = font.render('Time: ' + str(time) + 's', True, BLACK)
                rect = text.get_rect(center=(WIDTH * 0.75, HEIGHT + 20))
                WIN.blit(text, rect)

        elif Square.strikes >= 3:
            self.game_over()
            is_solved = True

        pygame.display.update() 

        return is_solved

    def game_over(self):
        game_active = False
        font = pygame.font.SysFont('Calibri', FONT_SIZE * 2, bold=True)
        text = font.render('Game Over', True, RED)
        rect = text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
        WIN.blit(text, rect)
        pygame.display.update()

    def solved(self, time=0):
        game_active = False
        font = pygame.font.SysFont('Calibri', int(FONT_SIZE * 1.5), bold=True)
        text = font.render('Solved in ' + str(time) + 's', True, BLUE)
        rect = text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
        WIN.blit(text, rect)
        pygame.display.update()
        
    def handle_inputs(self, event):
        if event.key == pygame.K_SPACE:
            self.solver.solve()

    

