import pygame
import random
import sys
import os
from enum import Enum, auto


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1276, 704))
pygame.display.set_caption("Snake")

black, white = (25, 25, 25), (255, 255, 255)
font80 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 80)
font21 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 21)


def draw(path, x, y):
    screen.blit(pygame.transform.flip(pygame.image.load(path).convert_alpha(), False, False), (x, y))


def centerPrint(variable, x, y, sizeX, sizeY, color=(65, 65, 65), font=font80):
    text = font.render(str(variable), True, color)
    rect = pygame.Rect((x, y, sizeX, sizeY))
    text_rect = text.get_rect()
    text_rect.center = rect.center
    screen.blit(text, text_rect)


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class Snake:
    def __init__(self, startPos):
        self.body = []
        self.body.append(startPos)
        self.body.append((startPos[0] + 1, startPos[1]))
        self.alive = True

    @staticmethod
    def __direction(d):
        if d == Direction.UP:
            return 0, -1
        elif d == Direction.DOWN:
            return 0, 1
        elif d == Direction.RIGHT:
            return 1, 0
        elif d == Direction.LEFT:
            return -1, 0

    def move(self, Direction):
        x, y = self.__direction(Direction)
        pos = 0

        for i in range(len(self.body)):
            if i == 0:
                xx, yy = self.body[i]
                pos = xx, yy
                xx += x
                yy += y
                self.body[i] = xx, yy
            else:
                xx, yy = pos
                pos = self.body[i]
                self.body[i] = xx, yy

    def deaded(self, rows, columns):
        if self.body[0][0] > columns - 1 or self.body[0][1] > rows - 1 or self.body[0][0] < 0 or self.body[0][1] < 0:
            self.alive = False
        elif self.body[0] in self.body[1:]:
            self.alive = False

    def eat(self, food):
        if food == (self.body[0][0], self.body[0][1]):
            self.body.append((self.body[-1][0], self.body[-1][1]))
            return True

    def show(self, width):
        draw(resource_path("./Layout/Snake Head.png"), self.body[0][0] * width, self.body[0][1] * width)
        for i in range(1, len(self.body)):
            draw(resource_path("./Layout/Snake Body.png"), self.body[i][0] * width, self.body[i][1] * width)


def Menu(score=0):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    return Direction.DOWN
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    return Direction.UP
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    return Direction.RIGHT
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    return Direction.LEFT

        if score == 0:
            centerPrint("Pressione qualquer tecla para iniciar", 628, 330, 25, 25, font=font21)
        else:
            centerPrint(score - 2, 628, 280, 25, 25)
            centerPrint("Pressione qualquer tecla para reiniciar", 628, 330, 25, 25, font=font21)

        pygame.display.update()
        clock.tick(15)


def SnakeGame():
    rows, columns, width, start, direction = 32, 58, 22, True, Direction.RIGHT

    snake = Snake((columns // 2, rows // 2))
    food = random.randint(0, columns-1), random.randint(0, rows-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != Direction.UP:
                    direction = Direction.DOWN
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != Direction.DOWN:
                    direction = Direction.UP
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != Direction.LEFT:
                    direction = Direction.RIGHT
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != Direction.RIGHT:
                    direction = Direction.LEFT

        screen.fill(black)
        draw(resource_path("./Layout/Snake Food.png"), food[0] * width, food[1] * width)

        snake.show(width)
        snake.deaded(rows, columns)

        if snake.eat(food):
            while True:
                newFood = random.randint(0, columns - 1), random.randint(0, rows - 1)
                if newFood not in snake.body:
                    break
            food = newFood

        if not snake.alive:
            Menu(len(snake.body))

            snake = Snake((columns // 2, rows // 2))
            food = random.randint(0, columns - 1), random.randint(0, rows - 1)

        if start:
            direction = Menu()
            start = False

        snake.move(direction)

        pygame.display.update()
        clock.tick(15)


SnakeGame()
