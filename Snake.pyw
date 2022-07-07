import pygame as pg
import random
from Things import Colors, Fonts, draw, centerPrint


class Snake:
    def __init__(self, startPos):
        self.body = [startPos, (startPos[0] + 1, startPos[1])]

    def move(self, direction):
        prev, self.body[0] = self.body[0], tuple(map(sum, zip(self.body[0], direction)))
        for i in range(1, len(self.body)):
            pos = prev
            prev, self.body[i] = self.body[i], pos

    def isAlive(self, rows, columns):
        return all(0 <= i < j for i, j in zip(self.body[0], (columns, rows))) and self.body[0] not in self.body[1:]


def SnakeGame():
    rows, columns, w, start, direction, keyboard, alive = 32, 58, 22, True, (0, 0), True, True
    snake, food = Snake((columns // 2, rows // 2)), (random.randint(0, columns - 1), random.randint(0, rows - 1))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.KEYDOWN and event.key in [pg.K_DOWN, pg.K_s, pg.K_UP, pg.K_w, pg.K_RIGHT, pg.K_d, pg.K_LEFT, pg.K_a] and keyboard:
                for key, dir in [((pg.K_DOWN, pg.K_s), (0, 1)), ((pg.K_UP, pg.K_w), (0, -1)), ((pg.K_RIGHT, pg.K_d), (1, 0)), ((pg.K_LEFT, pg.K_a), (-1, 0))]:
                    if event.key in key and (direction != tuple(x * -1 for x in dir) or not alive):
                        direction = dir
                if not alive:
                    snake = Snake((columns // 2, rows // 2))
                keyboard, start = False, False

        screen.fill(Colors["black2"])
        draw(screen, "Assets/Snake Food.png", (food[0] * w, food[1] * w))
        [draw(screen, f"Assets/Snake {'Body' if i != 0 else 'Head'}.png", (body[0] * w, body[1] * w)) for i, body in enumerate(snake.body)]

        if food == snake.body[0]:
            snake.body.append(snake.body[-1])
            while food in snake.body and len(snake.body) != rows * columns:
                food = random.randint(0, columns - 1), random.randint(0, rows - 1)

        if not (alive := snake.isAlive(rows, columns)) or start:
            centerPrint(screen, "Pressione qualquer tecla para iniciar", (628, 330), (25, 25), Colors["gray"])
            if not alive:
                centerPrint(screen, len(snake.body[2:]), (628, 280), (25, 25), Colors["gray"], Fonts["demiBold80"])
        else:
            snake.move(direction)

        keyboard = True, pg.display.update(), pg.time.Clock().tick(15)


if __name__ == "__main__":
    screen = pg.display.set_mode((1276, 704))
    pg.display.set_caption("Snake")
    SnakeGame()
