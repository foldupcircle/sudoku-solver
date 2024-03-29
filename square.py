import pygame

class Square:
    block_width = 50
    block_height = 50
    strikes = 0

    def __init__(self, x, y, val=0):
        self.selected = False
        self.xy = (x, y)
        if val is not None:
            self.value = val
        else:
            self.value = 0
        self.rect = None

    def set_rect(self, pixel_x, pixel_y):
        self.rect = pygame.Rect(pixel_x, pixel_y, self.block_width, self.block_height)
        self.pos = (pixel_x, pixel_y)
