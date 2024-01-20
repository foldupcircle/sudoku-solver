import pygame
import time
from square import Square

BLACK = (20, 20, 20)
WHITE = (250, 250, 250)
BLUE = (30, 144, 255)
RED = (240, 20, 0)
GRAY = (200, 200, 200)
GREEN = (50, 205, 50)

THICK_LINE = 4
FONT_SIZE = 32

WIDTH, HEIGHT = (Square.block_width * 9) + (2 * THICK_LINE), (Square.block_height * 9) + (2 * THICK_LINE)
WIN = pygame.display.set_mode((WIDTH, HEIGHT + 40))

class GUI:
    def __init__(self, solver=None) -> None:
        self.solver = solver
        self.game_active = True

    def draw_sudoku_grid(self, empty, time=None):
        WIN.fill(WHITE)

        pygame.display.set_caption('Sudoku')

        # Printing out the grid
        r_pos = 0
        c_pos = 0
        font = pygame.font.SysFont('Calibri', FONT_SIZE, bold=False) # Set Font

        for x in range(len(self.solver.board)):
            if x % 3 == 0 and x < 8 and x > 0:
                r_pos += int(THICK_LINE / 2) - 1
                pygame.draw.line(WIN, BLACK, (0, r_pos), (WIDTH, r_pos), THICK_LINE)
                r_pos += int(THICK_LINE / 2) + 1
            c_pos = 0
            for y in range(len(self.solver.board[0])):
                sq = self.solver.board[x][y]
                if sq.rect is None:
                    sq.set_rect(c_pos, r_pos)
                if sq.selected:
                    WIN.fill(GRAY, sq.rect)
                else:
                    WIN.fill(WHITE, sq.rect)
                pygame.draw.rect(WIN, BLACK, sq.rect, 1)
                if sq.value:
                    if not self.solver.original_board[x][y].value:
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
            
        # Printing Time
        if time and not is_solved:
            text = font.render('Time: ' + str(time) + 's', True, BLACK)
            rect = text.get_rect(center=(WIDTH * 0.75, HEIGHT + 20))
            WIN.blit(text, rect)

        pygame.display.update() 

        return is_solved

    def solved(self, time=0):
        self.game_active = False
        font = pygame.font.SysFont('Calibri', int(FONT_SIZE), bold=True)
        text = font.render('Solved in ' + str(time) + 's', True, GREEN)
        rect = text.get_rect(center=(WIDTH * 0.75, HEIGHT + 20))
        WIN.blit(text, rect)
        pygame.display.update()
        
    def handle_inputs(self, event):
        if event.key == pygame.K_SPACE:
            start_time = time.time()
            self.solver.solve()
            return time.time() - start_time
