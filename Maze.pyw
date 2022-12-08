import pygame as pg
import random
from Things import Colors, draw


def generateMaze(width, height):
    grid = [([0 if column % 2 == 1 and row % 2 == 1 else 1 for column in range(width)]) for row in range(height)]
    w, h = (len(grid[0]) - 1) // 2, (len(grid) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x, y):
        vis[y][x], d = 1, [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for xx, yy in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                grid[max(y, yy) * 2][x * 2 + 1] = 0
            if yy == y:
                grid[y * 2 + 1][max(x, xx) * 2] = 0

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))
    return grid


def Maze():
    columns, rows, w, totalKeys = 35, 17, 35, 0
    maze = generateMaze(rows, columns)
    path = [(i, j) for i in range(columns) for j in range(rows) if maze[i][j] == 0]
    player, side, radius, keys, door = list(random.choice(path)), True, 50, [random.choice(path) for _ in range(3)], random.choice(path)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kb = pg.key.get_pressed()
        for key, dir, axis in [((pg.K_RIGHT, pg.K_d), (1, 0), 0), ((pg.K_LEFT, pg.K_a), (-1, 0), 0), ((pg.K_UP, pg.K_w), (0, -1), 1), ((pg.K_DOWN, pg.K_s), (0, 1), 1)]:
            if (kb[key[0]] or kb[key[1]]) and maze[player[0] + dir[0]][player[1] + dir[1]] == 0:
                player[axis] += dir[0] if dir[0] != 0 else dir[1]
        for k, s in [((pg.K_RIGHT, pg.K_d), True), ((pg.K_LEFT, pg.K_a), False)]:
            side = s if kb[k[0]] or kb[k[1]] else side

        if totalKeys == 3 and tuple(player) == door:
            return True

        screen.fill(Colors["black2"])
        [draw(screen, "assets/images/Key.png", ((29 + w * key[0]) + 5, (64 + w * key[1]) + 2)) for key in keys]
        draw(screen, f"assets/Door{'' if totalKeys == 3 else ' 0'}.png", ((29 + w * door[0]) + 6, (64 + w * door[1]) + 2))

        if tuple(player) in keys:
            totalKeys += 1
            del keys[keys.index((player[0], player[1]))]

        for i in range(columns):
            for j in range(rows):
                if player[0] - radius <= i <= player[0] + radius and player[1] - radius <= j <= player[1] + radius:
                    if maze[i][j] == 1:
                        pg.draw.rect(screen, Colors["blue"], [29 + w * i, 64 + w * j, w - 3, w - 3])
                else:
                    pg.draw.rect(screen, Colors["lightgray2"], [29 + w * i, 64 + w * j, w - 3, w - 3])
                if i == 0 or i == columns - 1 or j == 0 or j == rows - 1:
                    pg.draw.rect(screen, Colors["red"], [29 + w * i, 64 + w * j, w - 3, w - 3])

        [draw(screen, "assets/images/Key 0.png", (591 + 35 * i, 18)) for i in range(3)]
        [draw(screen, "assets/images/Key.png", (591 + 35 * i, 18)) for i in range(totalKeys)]
        draw(screen, "assets/images/Player.png", ((29 + w * player[0]) + 8, (64 + w * player[1]) + 4), side)

        pg.display.update(), pg.time.Clock().tick(12)


if __name__ == "__main__":
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Maze")
    Maze()
