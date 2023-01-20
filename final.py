from copy import deepcopy
import pygame
from square import Square
from typing import Optional

rows = {}
columns = {}
boxes = {}
board = [
    [5,0,0,0,1,6,2,0,0],
    [0,0,0,9,8,0,5,0,4],
    [0,3,0,0,0,0,0,0,9],
    [0,0,0,6,0,0,1,0,0],
    [9,0,6,0,0,0,0,0,2],
    [0,2,3,0,4,9,0,0,0],
    [0,4,0,0,0,0,0,8,1],
    [3,1,5,2,9,0,0,6,7],
    [8,0,9,4,7,1,0,2,5]
]

original_board = deepcopy(board)

def can_input(r, c, b, key, val):
    '''
    Return True if val can be placed at coordinate key(tuple), else False
    '''
    row = key[0]
    col = key[1]
    box = ((row // 3) * 3) + (col // 3)
    if val in r.get(row) or val in c.get(col) or val in b.get(box):
        return False
    return True

def parse(bo, rows, columns, boxes, avail={}):
    # Parse through the board, storing empty and existing values
    for r in range(len(bo)):
        rows[r] = []
        for c in range(len(bo[0])):
            if r == 0:
                columns[c] = []
            box = ((r // 3) * 3) + (c // 3)
            if r % 3 == 0 and c % 3 == 0:
                boxes[box] = []
            
            v = bo[r][c]
            if v:
                rows[r].append(v)
                columns[c].append(v)
                boxes[box].append(v)
            else:
                avail[(r, c)] = []
    
    # Store all empty values in avail
    for k in avail.keys():
        s = set()
        row = k[0]
        col = k[1]
        for r in rows.get(row):
            s.add(r)
        for c in columns.get(col):
            s.add(c)
        box = ((row // 3) * 3) + (col // 3)
        for b in boxes.get(box):
            s.add(b)
        for n in range(1, 10):
            if n not in s:
                avail[k].append(n)

def solve(bo, grid):
    '''
    Solving the given sudoku board b using the backtracking algorithm
    '''
    # Defining Hashmaps to store values while parsing
    rows = {}
    boxes = {}
    columns = {}
    avail = {}

    parse(bo, rows, columns, boxes, avail)

    avail_spaces = sorted(avail.keys())
    def place(k_index):
        '''
        Place the numbers in available spaces, backtracking when they don't fit
        '''
        if k_index == len(avail_spaces):
            return 0
        r = avail_spaces[k_index][0]
        c = avail_spaces[k_index][1]
        b = ((r // 3) * 3) + (c // 3)
        found = False
        for v in avail.get(avail_spaces[k_index]):
            if can_input(rows, columns, boxes, avail_spaces[k_index], v):
                rows[r].append(v)
                columns[c].append(v)
                boxes[b].append(v)
                bo[r][c] = v
                if grid:
                    print('hi')
                    grid[r][c].value = v
                    draw_sudoku_grid(grid, (0, 0), False, len(avail))
                res = place(k_index + 1)
                if res:
                    rows[r].pop()
                    columns[c].pop()
                    boxes[b].pop()
                    bo[r][c] = 0
                    if grid:
                        grid[r][c].value = 0
                        draw_sudoku_grid(grid, (0, 0), False, len(avail))
                else:
                    found = True
        if not found:
            return 1
        else:
            return 0
    place(0)
    return bo

def print_board(b):
    for i in b:
        print(i)
         
#########################################################################

# GUI

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
SOLVED_BOARD = solve(deepcopy(original_board), False)
game_active = True


WIDTH, HEIGHT = (Square.block_width * 9) + (2 * THICK_LINE), (Square.block_height * 9) + (2 * THICK_LINE)
WIN = pygame.display.set_mode((WIDTH, HEIGHT + 40))
pygame.display.set_caption('Sudoku')

def draw_sudoku_grid(grid, pos, changed, empty, val=0):
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

    if Square.strikes > 0 and Square.strikes < 3:
        s = ''
        for _ in range(Square.strikes):
            s += 'X '
        text = font.render(s, True, RED)
        rect = text.get_rect(center=(20 + (Square.strikes * 14), HEIGHT + 20))
        WIN.blit(text, rect)
    elif Square.strikes >= 3:
        game_over()

    pygame.display.update()

    return empty

def game_over():
    game_active = False
    font = pygame.font.SysFont('Calibri', FONT_SIZE * 2, bold=True)
    text = font.render('Game Over', True, RED)
    rect = text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
    WIN.blit(text, rect)
    pygame.display.update()

def solved():
    game_active = False
    font = pygame.font.SysFont('Calibri', FONT_SIZE * 2, bold=True)
    text = font.render('Solved!', True, BLUE)
    rect = text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
    WIN.blit(text, rect)
    pygame.display.update()
    
def handle_inputs(event, grid, bo):
    val = 0
    if event.key == pygame.K_1:
        val = 1
    if event.key == pygame.K_2:
        val = 2
    if event.key == pygame.K_3:
        val = 3
    if event.key == pygame.K_4:
        val = 4
    if event.key == pygame.K_5:
        val = 5
    if event.key == pygame.K_6:
        val = 6
    if event.key == pygame.K_7:
        val = 7
    if event.key == pygame.K_8:
        val = 8
    if event.key == pygame.K_9:
        val = 9
    if event.key == pygame.K_SPACE:
        print('hello')
        solve(grid, bo)
    return val

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    pos = 0
    changed = False
    grid = deepcopy(original_board)
    empty = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            grid[r][c] = Square(r, c, original_board[r][c])
            if not original_board[r][c]:
                empty += 1
    print_board(SOLVED_BOARD)
    while run:
        if game_active:
            clock.tick(FPS)
            changed = False
            val = 0
            keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    val = handle_inputs(event, grid, deepcopy(original_board))
                if event.type == pygame.MOUSEBUTTONDOWN and pos != pygame.mouse.get_pos():
                    pos = pygame.mouse.get_pos()
                    changed = True
                    
            empty = draw_sudoku_grid(grid, pos, changed, empty, val)
            if not empty:
                solved()
            pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()