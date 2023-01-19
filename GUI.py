import pygame
from solve import solve, original_board, board, rows_or, columns_or, boxes_or, can_input, parse

WIDTH, HEIGHT = 630, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BLUE = (70, 130, 180)
RED = (255, 87, 51)
GRAY = (128,128,128)

FPS = 60
BUFFER = 3
THINK_LINE = 10
FONT_SIZE = 40
BLOCK_SIZE = int(WIDTH / 9)
SELECTED = [0, 0]
bo = original_board

def draw_sudoku_grid(bo, pos, changed):
    WIN.fill(BLACK)
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
    pygame.draw.line(WIN, WHITE, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (WIDTH * 2 / 3, 0), (WIDTH * 2 / 3, HEIGHT), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (0, HEIGHT * 2 / 3), (WIDTH, HEIGHT * 2 / 3), THINK_LINE)

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

    pygame.display.update()

def handle_selected(keys_pressed):
    if keys_pressed[pygame.K_UP] and SELECTED[1] != 0:
        SELECTED[1] -= 1
    elif keys_pressed[pygame.K_DOWN] and SELECTED[1] != 8:
        SELECTED[1] += 1
    elif keys_pressed[pygame.K_LEFT] and SELECTED[0] != 0:
        SELECTED[0] -= 1
    elif keys_pressed[pygame.K_RIGHT] and SELECTED[0] != 8:
        SELECTED[0] += 1

def handle_inputs(keys_pressed):
    added = 0
    c = SELECTED[0]
    r = SELECTED[1]
    parse(bo, rows_or, columns_or, boxes_or)
    if keys_pressed[pygame.K_1] and can_input(rows_or, columns_or, boxes_or, (r, c), 1) and not bo[r][c]:
        bo[r][c] = 1
        added = 1
    elif keys_pressed[pygame.K_2] and can_input(rows_or, columns_or, boxes_or, (r, c), 2) and not bo[r][c]:
        bo[r][c] = 2
        added = 2
    elif keys_pressed[pygame.K_3] and can_input(rows_or, columns_or, boxes_or, (r, c), 3) and not bo[r][c]:
        bo[r][c] = 3
        added = 3
    elif keys_pressed[pygame.K_4] and can_input(rows_or, columns_or, boxes_or, (r, c), 4) and not bo[r][c]:
        bo[r][c] = 4
        added = 4
    elif keys_pressed[pygame.K_5] and can_input(rows_or, columns_or, boxes_or, (r, c), 5) and not bo[r][c]:
        bo[r][c] = 5
        added = 5
    elif keys_pressed[pygame.K_6] and can_input(rows_or, columns_or, boxes_or, (r, c), 6) and not bo[r][c]:
        bo[r][c] = 6
        added = 6
    elif keys_pressed[pygame.K_7] and can_input(rows_or, columns_or, boxes_or, (r, c), 7) and not bo[r][c]:
        bo[r][c] = 7
        added = 7
    elif keys_pressed[pygame.K_8] and can_input(rows_or, columns_or, boxes_or, (r, c), 8) and not bo[r][c]:
        bo[r][c] = 8
        added = 8
    elif keys_pressed[pygame.K_9] and can_input(rows_or, columns_or, boxes_or, (r, c), 9) and not bo[r][c]:
        bo[r][c] = 9
        added = 9
    
    if added:
        rows_or[r].append(added)
        columns_or[c].append(added)
        b = ((r // 3) * 3) + (c // 3)
        boxes_or[b].append(added)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    pos = 0
    changed = False
    bo = original_board
    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            bo = solve(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pos != pygame.mouse.get_pos():
                pos = pygame.mouse.get_pos()
                changed = True
            else:
                handle_selected(keys_pressed)
                handle_inputs(keys_pressed)
                changed = False
        draw_sudoku_grid(bo, pos, changed)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()