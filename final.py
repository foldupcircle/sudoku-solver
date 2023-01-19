from copy import deepcopy
import pygame
from square import Square

rows_or = {}
columns_or = {}
boxes_or = {}
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

def solve(bo):
    '''
    Solving the given sudoku board b using the backtracking algorithm
    '''
    # Defining Hashmaps to store values while parsing
    rows = {}
    boxes = {}
    columns = {}
    avail = {}

    parse(bo, rows, columns, boxes, avail)

    rows_or = deepcopy(rows)
    columns_or = deepcopy(columns)
    boxes_or = deepcopy(boxes)

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
                res = place(k_index + 1)
                if res:
                    rows[r].pop()
                    columns[c].pop()
                    boxes[b].pop()
                    bo[r][c] = 0
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

WIDTH, HEIGHT = 470, 470
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BLUE = (70, 130, 180)
RED = (255, 87, 51)
GRAY = (128,128,128)

FPS = 60
BUFFER = 3
THICK_LINE = 10
FONT_SIZE = 40
BLOCK_SIZE = int(WIDTH / 9)
SELECTED = [0, 0]



def draw_sudoku_grid(grid, pos, changed):
    WIN.fill(BLACK)
    r_pos = 0
    c_pos = 0
    for x in range(len(grid)):
        if x % 3 == 0 and x < 8 and x > 0:
            r_pos += int(THICK_LINE / 2) - 1
            pygame.draw.line(WIN, WHITE, (0, r_pos), (WIDTH, r_pos), THICK_LINE)
            r_pos += int(THICK_LINE / 2) + 1
        c_pos = 0
        for y in range(len(grid[0])):
            sq = grid[x][y]
            if not sq.rect:
                sq.set_rect(c_pos, r_pos)
            pygame.draw.rect(WIN, WHITE, sq.rect, 1)
            c_pos += 50
            if (y + 1) % 3 == 0 and y < 8:
                c_pos += int(THICK_LINE / 2) - 1
                pygame.draw.line(WIN, WHITE, (c_pos, 0), (c_pos, HEIGHT), THICK_LINE)
                c_pos += int(THICK_LINE / 2) + 1
        r_pos += 50

    '''
    if changed:
        SELECTED[0] = pos[0] // 70
        SELECTED[1] = pos[1] // 70
    x = SELECTED[0] * 70
    y = SELECTED[1] * 70
    rectangle = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    WIN.fill(GRAY, rect=rectangle)
    pygame.draw.rect(WIN, WHITE, rectangle, 1)

    
    font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
    for r in range(len(bo)):
        for c in range(len(bo[0])):
            if bo[r][c] and original_board[r][c]:
                text = font.render(str(bo[r][c]), True, WHITE)
                rect = text.get_rect(center=(c * 70 + (BLOCK_SIZE / 2), r * 70 + (BLOCK_SIZE / 2)))
                WIN.blit(text, rect)
            elif bo[r][c] and not original_board[r][c]:
                text = font.render(str(bo[r][c]), True, BLUE)
                rect = text.get_rect(center=(c * 70 + (BLOCK_SIZE / 2), r * 70 + (BLOCK_SIZE / 2)))
                WIN.blit(text, rect)
    '''

    pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    pos = 0
    changed = False
    bo = original_board
    grid = deepcopy(original_board)
    print(grid)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            grid[r][c] = Square(r, c, original_board[r][c])
    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            bo = solve(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_sudoku_grid(grid, pos, changed)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()