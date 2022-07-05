import contextlib
import random
import pygame
from Things import Colors, Fonts, centerPrint, AbstractButton, TimePiece


class Button(AbstractButton):
    def show(self, mouse):
        if self.under(mouse):
            pygame.draw.rect(screen, Colors["lightgray"], self.rect)
            pygame.draw.rect(screen, Colors["gray"], self.rect, 2)
        else:
            pygame.draw.rect(screen, Colors["lightgray2"], self.rect)
        centerPrint(screen, self.text, self.rect.topleft, self.rect.size, Colors["white"])


class Tile:
    bomb, near, state = False, 0, None


class Grid:
    def __init__(self, columns, rows, bombs):
        self.grid = [[Tile() for _ in range(columns)] for _ in range(rows)]
        while bombs > 0:
            if not (tile := self[random.randint(0, rows - 1)][random.randint(0, columns - 1)]).bomb:
                tile.bomb, bombs = True, bombs - 1

    def bombCounter(self, x, y):
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            with contextlib.suppress(IndexError):
                if y + dy >= 0 and dx + x >= 0 and self[y + dy][x + dx].bomb:
                    self[y][x].near += 1
                self[y][x].state = VIS

    def search(self, x, y):
        if 0 <= x < len(self[0]) and 0 <= y < len(self.grid) and self[y][x].state != VIS and not self[y][x].bomb:
            self.bombCounter(x, y)
            if self[y][x].near == 0:
                [self.search(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]]

    def __getitem__(self, item):
        return self.grid[item]


def Minesweeper(bombs):
    rows, columns, w, lost = 16, 32, 40, False
    grid, timer, countdown = Grid(columns, rows, bombs), TimePiece(), TimePiece()
    textColors = {1: "blue", 2: "green", 3: "red", 4: "darkblue", 5: "darkred", 6: "darkgray", 7: "darkgray", 8: "black2"}

    while True:
        won = all(tile.bomb and tile.state == FLAG or not tile.bomb and tile.state != FLAG for line in grid for tile in line)
        mx, my = pygame.mouse.get_pos()[0] // w, pygame.mouse.get_pos()[1] // w - 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not lost and not won and 0 <= mx < columns and 0 <= my < rows:
                if event.button == 1 and grid[my][mx].state != FLAG:
                    grid.search(mx, my)
                    lost, grid[my][mx].state = grid[my][mx].bomb, VIS
                for button, state in [(2, DOUBT), (3, FLAG)]:
                    if event.button == button and grid[my][mx].state != VIS:
                        grid[my][mx].state = state if grid[my][mx].state != state else None

        screen.fill(Colors["white"])
        pygame.draw.rect(screen, Colors["orange"], pygame.Rect((409, 20, 110, 37)), 1)
        pygame.draw.rect(screen, Colors["gray"], pygame.Rect((762, 20, 110, 37)), 1)
        centerPrint(screen, bombs, (409, 20), (110, 37), Colors["orange"])
        centerPrint(screen, timer, (762, 20), (110, 37), Colors["gray"])

        for y, row in enumerate(grid):
            for x, t in enumerate(row):
                c = Colors["lightred" if t.bomb and t.state == VIS else "red" if t.bomb and lost else "lightorange" if t.state == FLAG else "lightgreen" if t.state == DOUBT else "white" if t.state == VIS else "lightgray2"]
                pygame.draw.rect(screen, c, [x * w, w * 2 + y * w, w, w])
                if t.near > 0:
                    centerPrint(screen, t.near, (x * w, w * 2 + y * w), (w, w), Colors[textColors[t.near]])
                c = Colors["darkgray" if t.state == VIS else "black"]
                pygame.draw.rect(screen, c, pygame.Rect((x * w, w * 2 + y * w, w + 1, w + 1)), 1)

        if 0 <= mx < columns and 0 <= my < rows and not won and not lost and grid[my][mx].state != VIS:
            c = Colors["orange" if grid[my][mx].state == FLAG else "darkgreen" if grid[my][mx].state == DOUBT else "lightgray"]
            pygame.draw.rect(screen, c, [mx * w, my * w + w * 2, w, w])
            pygame.draw.rect(screen, Colors["black"], pygame.Rect((mx * w, my * w + w * 2, w + 1, w + 1)), 1)

        if countdown.seconds > 3:
            return won

        timer.update(not won and not lost), countdown.update(won or lost), pygame.display.update(), pygame.time.Clock().tick(30)


def Menu():
    buttons = [Button(text, (370 + 190 * i, 400), (160, 40)) for i, text in enumerate(["Fácil", "Normal", "Difícil"])]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            [Minesweeper(60 + 20 * i) if buttons[i].click(event) else ... for i in range(len(buttons))]

        screen.fill(Colors["white"])
        centerPrint(screen, "Minesweeper", (340, 100), (600, 100), Colors["gray"], Fonts["demiBold80"])
        [button.show(pygame.mouse.get_pos()) for button in buttons], pygame.display.update(), pygame.time.Clock().tick(30)


VIS, FLAG, DOUBT = 1, 2, 3
if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Minesweeper")
    Menu()
