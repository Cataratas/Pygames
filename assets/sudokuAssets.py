import copy
import random
import itertools
from tkinter import ttk
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
import tkinter
import threading
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
import os

numberList, counter = list(range(1, 10)), 0


def printMenu():
    def printPuzzles():
        puzzles = [[[[0 for _ in range(9)] for _ in range(9)], 1 if i < int(easy.get()) else 4 if i < int(normal.get()) + int(easy.get()) else 8] for i in range(sum(map(int, (easy.get(), normal.get(), hard.get()))))]
        [generatePuzzle(puzzle) for puzzle, d in puzzles]
        threads = [threading.Thread(target=remove, args=(puzzle, d, )) for puzzle, d in puzzles]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        canvas, grid = SimpleDocTemplate("Sudoku.pdf", pagesize=A4), []
        for puzzle, d in puzzles:
            puzzle = [[f"{str(number) if number != 0 else ''}" for number in row] for row in puzzle]

            grid.append(Paragraph(f"{'Fácil' if d == 1 else 'Médio' if d == 4 else 'Difícil'}", ParagraphStyle(name="Difficulty", alignment=TA_CENTER, fontSize=16, leading=12, spaceAfter=14)), )
            grid.append(Table(puzzle, 9*[0.45*inch], 9*[0.45*inch], spaceAfter=50))
            grid[-1].setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                         ("LINEBELOW", (0, 2), (8, 2), 1.75, colors.black), ("LINEBELOW", (0, 5), (8, 5), 1.75, colors.black),
                                         ("LINEAFTER", (2, 0), (2, 8), 1.75, colors.black), ("LINEAFTER", (5, 0), (5, 8), 1.75, colors.black),
                                         ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black), ("BOX", (0, 0), (-1, -1), 1.75, colors.black)]))
        canvas.build(grid)
        os.startfile("Sudoku.pdf")
        window.destroy()

    window = tkinter.Tk()
    window.eval("tk::PlaceWindow . center")
    window.title("Imprimir Sudoku")
    window.geometry("400x130")
    ttk.Label(window, text=" " * 10 + "Fácil:").place(x=15, y=15)
    easy = ttk.Spinbox(window, from_=1, to=99, width=15, wrap=True)
    ttk.Label(window, text=" " * 9 + "Médio:").place(x=15, y=49)
    normal = ttk.Spinbox(window, from_=1, to=99, width=15, wrap=True)
    ttk.Label(window, text=" " * 9 + "Difícil:").place(x=15, y=87)
    hard = ttk.Spinbox(window, from_=1, to=99, width=15, wrap=True)
    button = ttk.Button(window, text="Imprimir", width=9, command=printPuzzles)

    easy.set(0), normal.set(0), hard.set(0)
    easy.place(x=125, y=14), normal.place(x=125, y=50), hard.place(x=125, y=87), button.place(x=320, y=92)
    window.mainloop()


def checkGrid(grid):
    return all(grid[row][col] != 0 for row, col in itertools.product(range(9), range(9)))


def getSquare(grid, i, row, col):
    x, y = 0 if row < 3 else 3 if row < 6 else 6, 0 if col < 3 else 3 if col < 6 else 6
    return [grid[i][y:y + 3] for i in range(x, x + 3)]


def generatePuzzle(grid, row=0, col=0):
    for i in range(81):
        row, col = i // 9, i % 9
        if grid[row][col] == 0:
            random.shuffle(numberList)
            for value in numberList:
                if value not in grid[row] and value not in [grid[_][col] for _ in range(9)]:
                    square = getSquare(grid, i, row, col)
                    if value not in (square[0] + square[1] + square[2]):
                        grid[row][col] = value
                        if checkGrid(grid) or generatePuzzle(grid):
                            return True
            break
    grid[row][col] = 0


def remove(grid, difficulty):
    global counter
    counter = 1
    while difficulty > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        backup = grid[row][col]
        grid[row][col], counter = 0, 0
        solve(copy.deepcopy(grid))
        if counter != 1:
            grid[row][col] = backup
            difficulty -= 1


def solve(grid, row=0, col=0):
    global counter
    for i in range(81):
        row, col = i // 9, i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                if value not in grid[row] and value not in [grid[_][col] for _ in range(9)]:
                    square = getSquare(grid, i, row, col)
                    if value not in (square[0] + square[1] + square[2]):
                        grid[row][col] = value
                        if checkGrid(grid):
                            counter += 1
                            break
                        elif solve(grid):
                            return True
            break
    grid[row][col] = 0
