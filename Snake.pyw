import pygame
import random
import sys
from enum import Enum
from Functions import BLACK2, GRAY, resource_path, draw, centerPrint


pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1276, 704))
pygame.display.set_caption("Snake")
font80 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 80)
font21 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 21)


class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    RIGHT = 1, 0
    LEFT = -1, 0


class Snake:
    def __init__(self, startPos):
        self.body = [startPos, (startPos[0] + 1, startPos[1])]

    def move(self, direction):
        prev, self.body[0] = self.body[0], tuple(map(sum, zip(self.body[0], direction.value)))

        for i in range(1, len(self.body)):
            pos = prev
            prev, self.body[i] = self.body[i], pos

    def isAlive(self, rows, columns):
        return all(0 <= i < j for i, j in zip(self.body[0], (columns, rows))) and self.body[0] not in self.body[1:]

    def eat(self, food):
        return self.body.append(self.body[-1]) if food == self.body[0] else ...

    def show(self, width):
        draw(screen, resource_path("./Layout/Snake Head.png"), self.body[0][0] * width, self.body[0][1] * width)
        for x in self.body[1:]:
            draw(screen, resource_path("./Layout/Snake Body.png"), x[0] * width, x[1] * width)


def SnakeGame():
    rows, columns, width, start, direction, keyboard, alive = 32, 58, 22, True, None, True, True

    snake = Snake((columns // 2, rows // 2))
    food = random.randint(0, columns-1), random.randint(0, rows-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and keyboard:
                if event.key in [pygame.K_DOWN, pygame.K_s] and direction != Direction.UP:
                    direction = Direction.DOWN
                elif event.key in [pygame.K_UP, pygame.K_w] and direction != Direction.DOWN:
                    direction = Direction.UP
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != Direction.LEFT:
                    direction = Direction.RIGHT
                elif event.key in [pygame.K_LEFT, pygame.K_a] and direction != Direction.RIGHT:
                    direction = Direction.LEFT

                if not alive:
                    snake = Snake((columns // 2, rows // 2))
                keyboard, start = False, False

        screen.fill(BLACK2)
        draw(screen, resource_path("./Layout/Snake Food.png"), food[0] * width, food[1] * width)
        snake.show(width)

        if snake.eat(food):
            while food in snake.body and len(snake.body) != rows * columns:
                food = random.randint(0, columns-1), random.randint(0, rows-1)

        if not (alive := snake.isAlive(rows, columns)) or start:
            centerPrint(screen, "Pressione qualquer tecla para iniciar", 628, 330, 25, 25, GRAY, font21)
            if not alive:
                centerPrint(screen, len(snake.body[2:]), 628, 280, 25, 25, GRAY, font80)
                direction = None
        else:
            snake.move(direction)

        keyboard = True
        pygame.display.update()
        clock.tick(15)


SnakeGame()
