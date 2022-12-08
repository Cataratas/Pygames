import copy
import pygame as pg
import itertools
from assets.sudokuAssets import generatePuzzle, remove, printMenu
from Things import Colors, Fonts, centerPrint, AbstractButton, TimePiece


class Button(AbstractButton):
    def __init__(self, text, pos, size):
        super().__init__(text, pos, size)

    def show(self, mouse, active=None):
        if self.under(mouse) or not self.under(mouse) and str(active) == self.text:
            pg.draw.rect(screen, Colors["lightgray4"], self.rect, self.rect.h // 2, 4)
        pg.draw.rect(screen, Colors["gray"],  pg.Rect(self.rect), 1, 4)
        centerPrint(screen, self.text, self.rect.topleft, self.rect.size, Colors["black"], Fonts["seguisym21"])


def Sudoku(difficultyStr, difficultyInt):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    generatePuzzle(grid)
    solution = copy.deepcopy(grid)
    remove(grid, difficultyInt)

    w, active, actions, timer, mGrid = 40, None, [[], []], TimePiece(), copy.deepcopy(grid)
    delete, backward, foward = Button("✕", (15, 480), (40, 40)), Button("←", (535, 480), (40, 40)), Button("→", (585, 480), (40, 40))

    while True:
        pg.display.set_caption(f"Sudoku - {difficultyStr} - {timer}")
        mouse = pg.mouse.get_pos()
        mx, my = (mouse[0] - 20) // w - 3, mouse[1] // w - 2

        for event in pg.event.get():
            if event.type == pg.QUIT or solution == grid:
                return

            if event.type == pg.KEYDOWN and event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                active = event.key - 48

            if delete.click(event):
                active = "✖"
            elif backward.click(event) and actions[0]:
                actions[1].append([actions[0][-1][0], actions[0][-1][1], grid[actions[0][-1][0]][actions[0][-1][1]]])
                grid[actions[0][-1][0]][actions[0][-1][1]] = actions[0][-1][2]
                del actions[0][-1]
            elif foward.click(event) and actions[1]:
                actions[0].append([actions[1][-1][0], actions[1][-1][1], grid[actions[1][-1][0]][actions[1][-1][1]]])
                grid[actions[1][-1][0]][actions[1][-1][1]] = actions[1][-1][2]
                del actions[1][-1]

            if 0 <= mx <= 8 and 0 <= my <= 8 and event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if grid[my][mx] == 0 and active != 0 and active != "✖" and active is not None:
                    actions[0].append([my, mx, grid[my][mx]])
                    grid[my][mx] = active
                elif mGrid[my][mx] == 0 and active == "✖":
                    actions[0].append([my, mx, grid[my][mx]])
                    grid[my][mx] = 0
                elif grid[my][mx] != 0:
                    active = grid[my][mx]

        screen.fill(Colors["white"])

        for i, j in itertools.product(range(9), range(9)):
            if active == "✖" and grid[i][j] != mGrid[i][j]:
                pg.draw.rect(screen, Colors["lightcoral"], [140 + j * w, w * 2 + i * w, w, w])
            elif grid[i][j] == active:
                pg.draw.rect(screen, Colors["lightgray4"], [140 + j * w, w * 2 + i * w, w, w])

        if active == "✖" and 0 <= mx <= 8 and 0 <= my <= 8 and mGrid[my][mx] == 0 and grid[my][mx] != 0:
            pg.draw.rect(screen, Colors["lightred"], [140 + mx * w, w * 2 + my * w, w, w])

        for row, col in itertools.product(range(9), range(9)):
            pg.draw.rect(screen, Colors["lightgray"], (140 + col * w, w * 2 + row * w, w + 1, w + 1), 1)
            if grid[row][col] != 0:
                centerPrint(screen, grid[row][col], (140 + col * w, w * 2 + row * w), (w, w), font=Fonts["seguisym18"])
        for i in range(4):
            pg.draw.line(screen, Colors["black"], (w * 3.5, w * 2 + 120 * i), (w * 12.5, w * 2 + 120 * i), 3)
            pg.draw.line(screen, Colors["black"], (w * 3.5 + 120 * i, w * 2), (w * 3.5 + 120 * i, w * 11), 3)

        delete.show(mouse, active), backward.show(mouse), foward.show(mouse)
        timer.update(), pg.display.update(), pg.time.Clock().tick(25)


def Menu():
    buttons = [Button(text, (50 + 190 * i, 400), (160, 36)) for i, text in enumerate(["Fácil", "Médio", "Difícil"])]
    printGame = Button("Imprimir", (240, 455), (160, 36))

    while True:
        pg.display.set_caption("Sudoku")
        mouse = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if printGame.click(event):
                printMenu()
            [Sudoku(buttons[i].text, round((i+1)**1.85)) if buttons[i].click(event) else ... for i in range(len(buttons))]

        screen.fill(Colors["white"])
        centerPrint(screen, "Sudoku", (20, 100), (600, 100), Colors["darkgray"], Fonts["seguisym81"])
        printGame.show(mouse), [button.show(mouse) for button in buttons], pg.display.update(), pg.time.Clock().tick(25)


if __name__ == "__main__":
    screen = pg.display.set_mode((640, 535))
    Menu()
