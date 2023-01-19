import pygame
from solve import solve, original_board, board

WIDTH, HEIGHT = 630, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku Solver')

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

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    bo = original_board
    pos = 0
    changed = False
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
                changed = False
        draw_sudoku_grid(bo, pos, changed)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()