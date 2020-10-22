import pygame
import random
import sys
import os


pygame.display.init(), pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1276, 704))


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


black, white = (25, 25, 25), (255, 255, 255)
font80 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 80)
font21 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 21)


def draw(path, x, y):
    screen.blit(pygame.transform.flip(pygame.image.load(path).convert_alpha(), False, False), (x, y))


def centerprint(variable, x, y, sizeX, sizeY, color=(65, 65, 65), font=font80):
    text = font.render(str(variable), True, color)
    rect = pygame.Rect((x, y, sizeX, sizeY))
    text_rect = text.get_rect()
    text_rect.center = rect.center
    screen.blit(text, text_rect)


class Snake:
    def __init__(self, start_pos):
        self.body = []
        self.body.append(start_pos)
        self.body.append((start_pos[0]+1, start_pos[1]))
        self.alive = True

    def move(self, x, y):
        pos = 0, 0
        for i in range(len(self.body)):
            if i == 0:
                xx, yy = self.body[i]
                pos = xx, yy
                xx += x; yy += y
                self.body[i] = xx, yy
            else:
                xx, yy = pos
                pos = self.body[i]
                self.body[i] = xx, yy

    def deaded(self, rows, columns):
        if self.body[0][0] > columns - 1 or self.body[0][1] > rows - 1 or self.body[0][0] < 0 or self.body[0][1] < 0:
            self.alive = False
        elif self.body[0] in self.body[1:]: self.alive = False

    def grow(self):
        self.body.append((self.body[-1][0], self.body[-1][1]))

    def show(self, width):
        for i in range(len(self.body)):
            if i == 0: draw(resource_path("./Layout/Snake Head.png"), self.body[i][0] * width, self.body[i][1] * width)
            else: draw(resource_path("./Layout/Snake Body.png"), self.body[i][0] * width, self.body[i][1] * width)


def Menu(score=0):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            elif event.type == pygame.KEYDOWN: return event.key

        if score == 0:
            centerprint("Pressione qualquer tecla para iniciar", 628, 330, 25, 25, font=font21)
        else:
            centerprint(score - 2, 628, 280, 25, 25)
            centerprint("Pressione qualquer tecla para reiniciar", 628, 330, 25, 25, font=font21)

        pygame.display.update(); clock.tick(15)


def Snakegame():
    rows, columns, width, start = 32, 58, 22, True

    up, down, right, left = False, False, True, False
    snake = Snake((columns // 2, rows // 2))

    f1, f2 = random.randint(0, columns-1), random.randint(0, rows-1)

    while True:

        if up: snake.move(0, -1)
        if down: snake.move(0, 1)
        if right: snake.move(1, 0)
        if left: snake.move(-1, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not up:
                    up, down, right, left = False, True, False, False
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and not down:
                    up, down, right, left = True, False, False, False
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not left:
                    up, down, right, left = False, False, True, False
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not right:
                    up, down, right, left = False, False, False, True

        screen.fill(black)

        draw(resource_path("./Layout/Snake Food.png"), f1 * width, f2 * width)

        if f1 == snake.body[0][0] and f2 == snake.body[0][1]:
            while True:
                newf1, newf2 = random.randint(0, columns - 1), random.randint(0, rows - 1)
                if newf1 != f1 and newf2 != f2 and (newf1, newf2) not in snake.body: break
            f1, f2 = newf1, newf2

            snake.grow()

        snake.show(width)
        snake.deaded(rows, columns)

        if not snake.alive:
            Menu(len(snake.body))

            snake = Snake((columns // 2, rows // 2))
            f1, f2 = random.randint(0, columns - 1), random.randint(0, rows - 1)

        if start:
            key = Menu()
            if (key == pygame.K_DOWN or key == pygame.K_s) and not up:
                up, down, right, left = False, True, False, False
            elif (key == pygame.K_UP or key == pygame.K_w) and not down:
                up, down, right, left = True, False, False, False
            elif (key == pygame.K_RIGHT or key == pygame.K_d) and not left:
                up, down, right, left = False, False, True, False
            elif (key == pygame.K_LEFT or key == pygame.K_a) and not right:
                up, down, right, left = False, False, False, True
            start = False

        pygame.display.update(); clock.tick(15)


Snakegame()