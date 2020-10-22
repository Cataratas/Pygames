import pygame
import random
import sys
import os

pygame.display.init(), pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

white, blue, red = (255, 255, 255), (0, 113, 188), (193, 39, 45)
black = (25, 25, 25)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


pygame.display.set_caption("Maze")


def draw(path, x, y, mirror=False):
    if mirror:
        screen.blit(pygame.transform.flip(pygame.image.load(resource_path(path)), True, False), (x, y))
    else:
        screen.blit(pygame.image.load(resource_path(path)).convert_alpha(), (x, y))


def maze():
    class Character:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.radius = 2
            self.right = True

        def show(self):
            global n_keys
            if self.right:
                draw(resource_path("./Layout/Player.png"), self.x, self.y - 5, True)
            else:
                draw(resource_path("./Layout/Player.png"), self.x, self.y - 5, False)
            for i in range(3):
                try:
                    if self.x == Keys[i].x and self.y == Keys[i].y:
                        del Keys[i]
                        n_keys += 1
                except IndexError:
                    continue

        def update(self):
            p_k = pygame.key.get_pressed()
            if (p_k[pygame.K_RIGHT] or p_k[pygame.K_d]) and (self.x + width, self.y) and (self.x - 8 + width, self.y - 8) not in Wall:
                self.x += width
            elif (p_k[pygame.K_LEFT] or p_k[pygame.K_a]) and (self.x - width, self.y) and (self.x - 8 - width, self.y - 8) not in Wall:
                self.x -= width
                self.right = False
            elif (p_k[pygame.K_UP] or p_k[pygame.K_w]) and (self.x, self.y - width) and (self.x - 8, self.y - 8 - width) not in Wall:
                self.y -= width
            elif (p_k[pygame.K_DOWN] or p_k[pygame.K_s]) and (self.x, self.y + width) and (self.x - 8, self.y - 8 + width) not in Wall:
                self.y += width
            if p_k[pygame.K_RIGHT] or p_k[pygame.K_d]: self.right = True
            if p_k[pygame.K_LEFT] or p_k[pygame.K_a]: self.right = False

    class Key:
        def __init__(self):
            self.x = 0
            self.y = 0

        def show(self):
            draw(resource_path("./Layout/Key.png"), self.x - 3, self.y - 5)

    class Exit:
        def __init__(self):
            self.x = 0
            self.y = 0

        def show(self, n_keys):
            if n_keys == 3:
                draw(resource_path("./Layout/Door.png"), self.x - 2, self.y - 5)
            else:
                draw(resource_path("./Layout/Door 0.png"), self.x - 2, self.y - 5)

    def create_grid(width, height):
        Grid = []
        for row in range(height):
            Grid.append([])
            for column in range(width):
                if column % 2 == 1 and row % 2 == 1:
                    Grid[row].append(0)
                elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                    Grid[row].append(1)
                else:
                    Grid[row].append(1)
        return Grid

    def make_maze(Grid):
        w = (len(Grid[0]) - 1) // 2
        h = (len(Grid) - 1) // 2
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

        def walk(x: int, y: int):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            random.shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    Grid[max(y, yy) * 2][x * 2 + 1] = 0
                if yy == y:
                    Grid[y * 2 + 1][max(x, xx) * 2] = 0

                walk(xx, yy)

        walk(random.randrange(w), random.randrange(h))

        return Grid

    global n_keys
    # Initialize Variables
    Wall, Path, COLUMNS, ROWS, width, n_keys = [], [], 35, 17, 35, 0
    Player, Keys, Exit = Character(), [], Exit()

    Grid = create_grid(ROWS, COLUMNS)
    make_maze(Grid)

    # Append Maze to List
    for i in range(COLUMNS):
        for j in range(ROWS):
            if Grid[i][j] == 1:
                Wall.append((29 + width * i, 64 + width * j))
            elif Grid[i][j] == 0:
                Path.append(((29 + width * i) + 8, (64 + width * j) + 8))

    # Randomly Position Stuff
    Player.x, Player.y = random.choice(Path)
    for s in range(len(Path)):
        if (Player.x, Player.y) == (Path[s]): del Path[s]; break
    for i in range(3):
        Keys.append(Key())
        Keys[i].x, Keys[i].y = random.choice(Path)
        for s in range(len(Path)):
            if (Keys[i].x, Keys[i].y) == (Path[s]): del Path[s]; break
    Exit.x, Exit.y = random.choice(Path)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Victory
        if n_keys == 3 and Player.x == Exit.x and Player.y == Exit.y: return True

        # Display Stuff
        screen.fill(black)
        for i in range(3):
            try:
                Keys[i].show()
            except IndexError:
                continue
        Exit.show(n_keys)

        for x in range(29, 1220, width):
            for y in range(64, 659, width):
                if Player.x + (Player.radius * 32) + 32 > x > Player.x - (Player.radius * 32) - 32 and Player.y + (Player.radius * 32) + 32 > y > Player.y - (Player.radius * 32) - 32:
                    if (x, y) in Wall: pygame.draw.rect(screen, blue, [x, y, width - 3, width - 3])
                else:
                    pygame.draw.rect(screen, (151, 151, 151), [x, y, 32, 32])

        for x in range(q := 29, 1220, width):
            pygame.draw.rect(screen, red, [x, 64, width - 3, width - 3])  # Top
            pygame.draw.rect(screen, red, [x, 624, width - 3, width - 3])  # Bottom
            if x < 600: pygame.draw.rect(screen, red, [q, x + 35, width - 3, width - 3])  # Left
            if x < 600: pygame.draw.rect(screen, red, [1219, x + 35, width - 3, width - 3])  # Right
        for x in range(3): draw(resource_path("./Layout/Key 0.png"), 591 + 35 * x, 18)
        for x in range(n_keys): draw(resource_path("./Layout/Key.png"), 591 + 35 * x, 18)

        Player.update(); Player.show()
        pygame.display.update(); clock.tick(12)


maze()
