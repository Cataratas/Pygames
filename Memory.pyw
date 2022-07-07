import pygame
import random
import json
from Things import Colors, Fonts, centerPrintFreeType, TimePiece


class Tile:
    def __init__(self):
        self.symbol, self.color = symbols[-1][0], symbols[-1][1] + [75, ]
        self.visible, self.paired = True, False
        del symbols[-1]

    def show(self, pos, mouse, tile, size=(121, 121)):
        s = pygame.Surface(size, pygame.SRCALPHA)
        s.fill(Colors["lightgray4" if mouse == tile else "lightgray3"])
        if self.visible or self.paired:
            centerPrintFreeType(screen, self.symbol, pos, size, self.color, Fonts["seguiEmj50"])
            s.fill(self.color)
        screen.blit(s, pos)


def Memory():
    rows, col, check, start, timer = 5, 8, [], True, TimePiece()
    random.shuffle(symbols)
    grid = [[Tile() for _ in range(col)] for _ in range(rows)]

    while True:
        mouse = pygame.mouse.get_pos()
        mx, my = (mouse[1] - 43) // 128, (mouse[0] - 126) // 128

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONUP and 0 <= mx < rows and 0 <= my < col and len(check) != 2 and not grid[mx][my].visible and not grid[mx][my].paired:
                grid[mx][my].visible = True
                check.append((mx, my))

            if len(check) == 2 and (timer.seconds >= 2 or grid[check[0][0]][check[0][1]].symbol == grid[check[1][0]][check[1][1]].symbol):
                match = grid[check[0][0]][check[0][1]].symbol == grid[check[1][0]][check[1][1]].symbol
                grid[check[0][0]][check[0][1]].paired, grid[check[1][0]][check[1][1]].paired = match, match
                grid[check[0][0]][check[0][1]].visible, grid[check[1][0]][check[1][1]].visible, check = False, False, []
                timer.reset()

        if all(tile.paired for row in grid for tile in row):
            return True

        if start and timer.seconds >= 3:
            for row in grid:
                for tile in row:
                    tile.visible = False
            start = False, timer.reset()

        screen.fill(Colors["white"])
        for i, row in enumerate(grid):
            for j, tile in enumerate(row):
                tile.show((131 + 128 * j, 43 + 128 * i), (mx, my), (i, j))

        timer.update(), pygame.display.update(), pygame.time.Clock().tick(30)


symbols = json.load(open("Assets/symbols.json"))
if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Memory")
    Memory()
