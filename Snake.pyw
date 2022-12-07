import pygame as pg
import random
from Things import Colors, Fonts, draw, centerPrint

screen = pg.display.set_mode((1276, 704))
pg.display.set_caption("Snake")
rows, columns, w, start, direction, keyboard, alive = 32, 58, 22, True, (0, 0), True, True
startPos = (columns // 2, rows // 2)
snake, food = [startPos, (startPos[0] + 1, startPos[1])], (random.randint(0, columns - 1), random.randint(0, rows - 1))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN and event.key in [pg.K_DOWN, pg.K_s, pg.K_UP, pg.K_w, pg.K_RIGHT, pg.K_d, pg.K_LEFT, pg.K_a] and keyboard:
            for key, dir in [((pg.K_DOWN, pg.K_s), (0, 1)), ((pg.K_UP, pg.K_w), (0, -1)), ((pg.K_RIGHT, pg.K_d), (1, 0)), ((pg.K_LEFT, pg.K_a), (-1, 0))]:
                if event.key in key and (direction != tuple(x * -1 for x in dir) or not alive):
                    direction = dir
            if not alive:
                snake = [startPos, (startPos[0] + 1, startPos[1])]
            keyboard, start = False, False

    screen.fill(Colors["black2"])
    draw(screen, "Assets/Snake Food.png", (food[0] * w, food[1] * w))
    [draw(screen, f"Assets/Snake {'Body' if i != 0 else 'Head'}.png", (body[0] * w, body[1] * w)) for i, body in enumerate(snake)]

    if food == snake[0]:
        snake.append(snake[-1])
        while food in snake and len(snake) != rows * columns:
            food = random.randint(0, columns - 1), random.randint(0, rows - 1)

    if not (alive := all(0 <= i < j for i, j in zip(snake[0], (columns, rows))) and snake[0] not in snake[1:]) or start:
        centerPrint(screen, "Pressione qualquer tecla para iniciar", (628, 330), (25, 25), Colors["gray"])
        if not alive:
            centerPrint(screen, len(snake[2:]), (628, 280), (25, 25), Colors["gray"], Fonts["demiBold80"])
    else:
        prev, snake[0] = snake[0], tuple(map(sum, zip(snake[0], direction)))
        for i in range(1, len(snake)):
            pos = prev
            prev, snake[i] = snake[i], pos

    keyboard = True, pg.display.update(), pg.time.Clock().tick(15)
