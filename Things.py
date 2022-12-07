import sys
import os
import pygame
import pygame.freetype
import time

pygame.font.init(), pygame.freetype.init()
images = {}


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


Fonts = {
    "myriad21": pygame.font.Font(resource_path("./Fonts/myriad-pro-8.otf"), 21),
    "myriad40": pygame.font.Font(resource_path("./Fonts/myriad-pro-8.otf"), 40),
    "myriad36": pygame.font.Font(resource_path("./Fonts/myriad-pro-8.otf"), 36),
    "bigJohn21": pygame.font.Font(resource_path("./Fonts/BIG JOHN.otf"), 21),
    "bigJohn36": pygame.font.Font(resource_path("./Fonts/BIG JOHN.otf"), 36),
    "bigJohn70": pygame.font.Font(resource_path("./Fonts/BIG JOHN.otf"), 70),
    "demiBold21": pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 21),
    "demiBold80": pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 80),
    "seguiEmj50": pygame.freetype.Font(resource_path("./Fonts/seguiemj.ttf"), 50),
    "seguisym18": pygame.font.Font(resource_path("./Fonts/seguisym.ttf"), 18),
    "seguisym21": pygame.font.Font(resource_path("./Fonts/seguisym.ttf"), 21),
    "seguisym81": pygame.font.Font(resource_path("./Fonts/seguisym.ttf"), 81),
}

Colors = {
    "black": (0, 0, 0), "black2": (25, 25, 25),
    "darkgreen": (0, 175, 69), "green": (0, 146, 69), "lightgreen": (72, 181, 89),
    "darkred": (141, 39, 45), "red": (193, 39, 45), "lightred": (254, 92, 92), "lightcoral": (254, 132, 132),
    "orange": (247, 107, 30), "lightorange": (247, 127, 45),
    "darkblue": (0, 75, 188), "blue": (0, 113, 188),
    "darkgray": (51, 51, 51), "gray": (70, 70, 70), "lightgray": (138, 138, 138), "lightgray2": (153, 153, 153),
    "lightgray4": (214, 214, 214), "lightgray3": (230, 230, 230), "white": (255, 255, 255),
}


class TimePiece:
    def __init__(self):
        self.__startTime, self.__seconds, self.__minutes, self.__hours = time.time(), 0, 0, 0

    def update(self, bl=True):
        if bl:
            self.__seconds = int(time.time() - self.__startTime)
            if self.__seconds > 59:
                self.__startTime = time.time()
                self.__minutes += 1
            if self.__minutes > 59:
                self.__minutes = 0
                self.__hours += 1
        else:
            self.__startTime = time.time()

    def __repr__(self):
        if self.__hours > 0:
            return f"{self.__hours:02d}:{self.__minutes:02d}:{self.__seconds:02d}"
        return f"{self.__minutes:02d}:{self.__seconds:02d}"

    @property
    def seconds(self):
        return self.__seconds

    def reset(self):
        self.__init__()


class AbstractButton:
    def __init__(self, text, pos, size):
        self.text = text
        self.rect = pygame.Rect(pos, size)

    def under(self, mouse):
        return self.rect.x + self.rect.w > mouse[0] > self.rect.x and self.rect.y + self.rect.h > mouse[1] > self.rect.y

    def click(self, event, enabled=True):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and enabled:
            return self.rect.collidepoint(event.pos)


def isImageLoaded(f):
    def helper(screen, path, *args):
        if path not in images:
            images.update({path: pygame.image.load(resource_path(path))})
        return f(screen, path, *args)
    return helper


@isImageLoaded
def draw(screen, path, pos, mirror=False):
    if mirror:
        screen.blit(pygame.transform.flip(images[path], True, False), pos)
    else:
        screen.blit(images[path].convert_alpha(), pos)


def centerPrint(screen, variable, pos, size, color=Colors["black"], font=Fonts["demiBold21"]):
    text = font.render(str(variable), True, color)
    rect = pygame.Rect(pos + size)
    text_rect = text.get_rect()
    text_rect.center = rect.center
    screen.blit(text, text_rect)


def centerPrintFreeType(screen, variable, pos, size, color, font):
    text = font.render(str(variable), color[:-1])
    text_rect = text[0].get_rect()
    text_rect.center = pygame.Rect(pos + size).center
    screen.blit(text[0], text_rect)
