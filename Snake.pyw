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
        self.alive = True

    def move(self, direction):
        prev = self.body[0]
        self.body[0] = tuple(map(sum, zip(self.body[0], direction.value)))

        for i in range(1, len(self.body)):
            pos = prev
            prev, self.body[i] = self.body[i], pos

    def deaded(self, rows, columns):
        if self.body[0][0] > columns - 1 or self.body[0][1] > rows - 1 or self.body[0][0] < 0 or self.body[0][1] < 0:
            self.alive = False
        elif self.body[0] in self.body[1:]:
            self.alive = False

    def eat(self, food):
        if food == self.body[0]:
            self.body.append((self.body[-1][0], self.body[-1][1]))
            return True

    def show(self, width):
        draw(screen, resource_path("./Layout/Snake Head.png"), self.body[0][0] * width, self.body[0][1] * width)
        for i in range(1, len(self.body)):
            draw(screen, resource_path("./Layout/Snake Body.png"), self.body[i][0] * width, self.body[i][1] * width)


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
            centerPrint(screen, "Pressione qualquer tecla para iniciar", 628, 330, 25, 25, GRAY, font21)
        else:
            centerPrint(screen, score - 2, 628, 280, 25, 25, GRAY, font80)
            centerPrint(screen, "Pressione qualquer tecla para reiniciar", 628, 330, 25, 25, GRAY, font21)

        pygame.display.update()
        clock.tick(15)


def SnakeGame():
    rows, columns, width, start, direction, keyboard = 32, 58, 22, True, Direction.RIGHT, True

    snake = Snake((columns // 2, rows // 2))
    food = random.randint(0, columns-1), random.randint(0, rows-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and keyboard:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != Direction.UP:
                    direction = Direction.DOWN
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != Direction.DOWN:
                    direction = Direction.UP
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != Direction.LEFT:
                    direction = Direction.RIGHT
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != Direction.RIGHT:
                    direction = Direction.LEFT
                keyboard = False

        screen.fill(BLACK2)
        draw(screen, resource_path("./Layout/Snake Food.png"), food[0] * width, food[1] * width)

        snake.show(width)
        snake.deaded(rows, columns)

        if snake.eat(food):
            while True:
                newFood = random.randint(0, columns - 1), random.randint(0, rows - 1)
                if newFood not in snake.body:
                    break
            food = newFood

        if not snake.alive:
            direction = Menu(len(snake.body))

            snake = Snake((columns // 2, rows // 2))
            food = random.randint(0, columns - 1), random.randint(0, rows - 1)

        if start:
            direction = Menu()
            start = False

        snake.move(direction)
        keyboard = True

        pygame.display.update()
        clock.tick(15)


SnakeGame()
