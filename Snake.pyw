import pygame as pg
import random
from Things import Colors, Fonts, draw, centerPrint

screen = pg.display.set_mode((1276, 704))
rows, columns, w, start, direction, alive = 32, 58, 22, True, (0, 0), True
startPos = (columns // 2, rows // 2)
snake, food = [startPos, (startPos[0] + 1, startPos[1])], (random.randint(0, columns - 1), random.randint(0, rows - 1))

while True:
    for i, event in enumerate(pg.event.get((pg.KEYDOWN, pg.QUIT))):
        if event.type == pg.QUIT:
            exit()
        if i == 0 and event.key in [pg.K_DOWN, pg.K_s, pg.K_UP, pg.K_w, pg.K_RIGHT, pg.K_d, pg.K_LEFT, pg.K_a]:
            for key, dir in [((pg.K_DOWN, pg.K_s), (0, 1)), ((pg.K_UP, pg.K_w), (0, -1)), ((pg.K_RIGHT, pg.K_d), (1, 0)), ((pg.K_LEFT, pg.K_a), (-1, 0))]:
                if event.key in key and (direction != tuple(x * -1 for x in dir) or not alive):
                    direction = dir
            if not alive:
                snake = [startPos, (startPos[0] + 1, startPos[1])]
            start = False

    screen.fill(Colors["black3"])
    pg.display.set_caption(f"Snake | Score: {len(snake[2:])}")
    draw(screen, "assets/images/Snake Food.png", (food[0] * w, food[1] * w))
    [draw(screen, f"assets/images/Snake {'Body' if i != 0 else 'Head'}.png", (body[0] * w, body[1] * w)) for i, body in enumerate(snake)]

    if food == snake[0]:
        snake.append(snake[-1])
        while food in snake and len(snake) != rows * columns:
            food = random.randint(0, columns - 1), random.randint(0, rows - 1)

    if not (alive := all(0 <= i < j for i, j in zip(snake[0], (columns, rows))) and snake[0] not in snake[1:]) or start:
        centerPrint(screen, '' if alive else len(snake[2:]), (628, 280), (25, 25), Colors["gray"], Fonts["demiBold80"])
        centerPrint(screen, "Pressione qualquer tecla para iniciar", (628, 330), (25, 25), Colors["gray"])
    else:
        prev, snake[0] = snake[0], tuple(map(sum, zip(snake[0], direction)))
        for i in range(1, len(snake)):
            pos = prev
            prev, snake[i] = snake[i], pos
    pg.display.update(), pg.time.Clock().tick(15)
