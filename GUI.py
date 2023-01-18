import pygame

WIDTH, HEIGHT = 630, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku Solver')

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

FPS = 60
BUFFER = 3

def draw_sudoku_grid():
    block_size = 70 # Set the size of the grid block
    for x in range(0, WIDTH, block_size):
        for y in range(0, HEIGHT, block_size):
            rectangle = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(WIN, WHITE, rectangle, 1)
    pygame.draw.lines(WIN, WHITE, True, [(0,0), (0, HEIGHT - BUFFER), (WIDTH - BUFFER, HEIGHT - BUFFER), (WIDTH - BUFFER, 0)], 6)
    pygame.draw.line(WIN, WHITE, (210,0), (210,630), 6)
    pygame.draw.line(WIN, WHITE, (420,0), (420,630), 6)
    pygame.draw.line(WIN, WHITE, (0,210), (630,210), 6)
    pygame.draw.line(WIN, WHITE, (0,420), (630,420), 6)


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_sudoku_grid()
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()