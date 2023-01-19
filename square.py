import pygame

class Square:
    block_width = 50
    block_height = 50

    def __init__(self, x, y, val=0):
        self.selected = False
        self.xy = (x, y)
        self.value = val
        self.rect = None

    def set_rect(self, pixel_x, pixel_y):
        self.rect = pygame.Rect(pixel_x, pixel_y, self.block_width, self.block_height)
        self.pos = (pixel_x, pixel_y)
