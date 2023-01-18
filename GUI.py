import pygame
from solve import solve, original_board, board

WIDTH, HEIGHT = 630, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku Solver')

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

FPS = 60
BUFFER = 3
THINK_LINE = 10
FONT_SIZE = 40

def draw_sudoku_grid(board):
    WIN.fill(BLACK)
    block_size = 70 # Set the size of the grid block
    for x in range(0, WIDTH, block_size):
        for y in range(0, HEIGHT, block_size):
            rectangle = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
    pygame.draw.lines(WIN, WHITE, True, [(0,0), (0, HEIGHT - BUFFER), (WIDTH - BUFFER, HEIGHT - BUFFER), (WIDTH - BUFFER, 0)], THINK_LINE)
    pygame.draw.line(WIN, WHITE, (WIDTH / 3,0), (WIDTH / 3,HEIGHT), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (WIDTH * 2 / 3,0), (WIDTH * 2 / 3,HEIGHT), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (0,HEIGHT / 3), (WIDTH,HEIGHT / 3), THINK_LINE)
    pygame.draw.line(WIN, WHITE, (0,HEIGHT * 2 / 3), (WIDTH,HEIGHT * 2 / 3), THINK_LINE)
    font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c]:
                text = font.render(str(board[r][c]), True, WHITE)
                rect = text.get_rect(center=(c * 70 + (block_size / 2), r * 70 + (block_size / 2)))
                WIN.blit(text, rect)
    pygame.display.update()

def solve_and_draw(bo):
    solve(bo)
    draw_sudoku_grid(bo)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    bo = original_board
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_sudoku_grid(bo)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            bo = solve(board)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()