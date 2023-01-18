import pygame
from solve import solve, original_board, board

WIDTH, HEIGHT = 630, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku Solver')

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BLUE = (70, 130, 180)

FPS = 60
BUFFER = 3
THINK_LINE = 10
FONT_SIZE = 40
BLOCK_SIZE = int(WIDTH / 9)
SELECTED = [0,0]

def draw_sudoku_grid(bo):
    WIN.fill(BLACK)
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
    pygame.draw.lines(WIN, WHITE, True, [(0,0), (0, HEIGHT - BUFFER), (WIDTH - BUFFER, HEIGHT - BUFFER), (WIDTH - BUFFER, 0)], THINK_LINE)
    pygame.draw.line(WIN, WHITE, (WIDTH / 3,0), (WIDTH / 3,HEIGHT), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (WIDTH * 2 / 3,0), (WIDTH * 2 / 3,HEIGHT), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (0,HEIGHT / 3), (WIDTH,HEIGHT / 3), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (0,HEIGHT * 2 / 3), (WIDTH,HEIGHT * 2 / 3), THINK_LINE)
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

def handle_selected(keys_pressed, position):
    row = SELECTED[0]
    col = SELECTED[1]
    if not position:
        pressed = False
        if keys_pressed[pygame.K_UP]:
            rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
            if SELECTED[0]:
                SELECTED[0] -= 1
            pressed = True
        elif keys_pressed[pygame.K_DOWN]:
            rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
            if SELECTED[0] != 8:
                SELECTED[0] += 1
            pressed = True
        elif keys_pressed[pygame.K_RIGHT]:
            rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
            if SELECTED[1] != 9:
                SELECTED[1] += 1
            pressed = True
        elif keys_pressed[pygame.K_LEFT]:
            rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
            if SELECTED[1]:
                SELECTED[1] -= 1 
            pressed = True
        if pressed:
            row = SELECTED[0]
            col = SELECTED[1]
            rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, BLUE, rectangle, 10)
        pygame.display.update()
    else:
        rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(WIN, WHITE, rectangle, 1)
        row = position[0] // BLOCK_SIZE
        col = position[1] // BLOCK_SIZE
        SELECTED[0] = row
        SELECTED[1] = col
        rectangle = pygame.Rect(row * 70, col * 70, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(WIN, BLUE, rectangle, 10)
    
def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    bo = original_board
    while run:
        clock.tick(FPS)
        pos = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = 0
        draw_sudoku_grid(bo)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            bo = solve(board)
        # handle_selected(keys_pressed, pos)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()