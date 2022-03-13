import sys
import os
import pygame


BLACK, BLACK2, WHITE = (0, 0, 0), (25, 25, 25), (255, 255, 255)
GRAY = (70, 70, 70)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def draw(screen, path, x, y):
    screen.blit(pygame.transform.flip(pygame.image.load(path).convert_alpha(), False, False), (x, y))


def centerPrint(screen, variable, x, y, sizeX, sizeY, color=BLACK, font=None):
    if font is None:
        font = pygame.font.SysFont("arial", 21)

    text = font.render(str(variable), True, color)
    rect = pygame.Rect((x, y, sizeX, sizeY))
    text_rect = text.get_rect()
    text_rect.center = rect.center
    screen.blit(text, text_rect)
