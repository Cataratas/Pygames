import pygame
import random
import sys
import os

pygame.display.init(), pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 620))


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


pygame.display.set_caption("TicTacToe")

font81 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 81)
font21 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 21)
white, blue, red = (255, 255, 255), (0, 113, 188), (193, 39, 45)


def centerprint(variable, x, y, sizeX, sizeY, color=(102, 102, 102), font=font21):
    text = font.render(str(variable), True, color)
    rect = pygame.Rect((x, y, sizeX, sizeY))
    text_rect = text.get_rect()
    text_rect.center = rect.center
    screen.blit(text, text_rect)


class Button:
    def __init__(self, name, color, x, y, size=(121, 121)):
        self.rect = pygame.Rect((x, y), size)
        self.name = name
        self.color = color
        self.c = None

    def show(self, mouse, bool=True, color=(102, 102, 102), br=None, rand=False):
        if self.rect.x + self.rect.width > mouse[0] > self.rect.x and self.rect.y + self.rect.height > mouse[1] > self.rect.y and bool:
            if br is None and not rand:
                draw(resource_path("./Layout/{} 2.png").format(self.color), self.rect.x, self.rect.y)
            elif rand:
                if self.c is None: self.c = random.randint(0, 1)
                if self.c == 1: draw(resource_path("./Layout/{} Blue.png").format(self.color), self.rect.x, self.rect.y); color = blue
                else: draw(resource_path("./Layout/{} Red.png").format(self.color), self.rect.x, self.rect.y); color = red
            elif br: draw(resource_path("./Layout/{} 2Blue.png").format(self.color), self.rect.x, self.rect.y)
            elif not br: draw(resource_path("./Layout/{} 2Red.png").format(self.color), self.rect.x, self.rect.y)
            centerprint(self.name, self.rect.x, self.rect.y - 1, self.rect.w, self.rect.h, color)
        else:
            self.c = None
            draw(resource_path("./Layout/{}.png").format(self.color), self.rect.x, self.rect.y)
            centerprint(self.name, self.rect.x, self.rect.y - 1, self.rect.w, self.rect.h, color)

    def click(self, event, bool=True):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and bool: return self.rect.collidepoint(event.pos)


def draw(path, x, y):
    screen.blit(pygame.image.load(resource_path(path)), (x, y))


def TicTacToe(oneplayer, easy=True, normal=False, hard=False):
    board = [[0 for i in range(3)] for j in range(3)]
    Buttons = [[0 for i in range(3)] for j in range(3)]

    x, y = 128, 43
    for i in range(3):
        x = 128; y += 129
        for j in range(3):
            Buttons[i][j] = Button(" ", "Tile", x, y)
            x += 129

    userscore, compscore, winscore, start, player = 0, 0, 3, True, True
    if oneplayer: active, br = "x", None
    else:
        active = random.choice(["x", "o"])
        br = active == "x"

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: Menu()

            # Player
            for i in range(3):
                for j in range(3):
                    if Buttons[i][j].click(event, board[i][j] == 0): board[i][j], player = active, False

            if not player and not oneplayer:
                if active == "x": active, player = "o", True
                else: active, player = "x", True

        if start:
            pygame.time.delay(250)
            board = [[0 for i in range(3)] for j in range(3)]
            if oneplayer: player, start = True, False
            else:
                active, player, start = random.choice(["x", "o"]), True, False
                if active == "x": br = True
                else: br = False

        if not oneplayer:
            if active == "x": br = True
            else: br = False

        # Victory / Draw
        if board[0][0] == board[0][1] == board[0][2] == "x" or board[1][0] == board[1][1] == board[1][2] == "x" or \
                board[2][0] == board[2][1] == board[2][2] == "x" or board[0][0] == board[1][0] == board[2][0] == "x" or \
                board[0][1] == board[1][1] == board[2][1] == "x" or board[0][2] == board[1][2] == board[2][2] == "x" or \
                board[0][0] == board[1][1] == board[2][2] == "x" or board[0][2] == board[1][1] == board[2][0] == "x":
            userscore += 1; start = True
        elif board[0][0] == board[0][1] == board[0][2] == "o" or board[1][0] == board[1][1] == board[1][2] == "o" or \
                board[2][0] == board[2][1] == board[2][2] == "o" or board[0][0] == board[1][0] == board[2][0] == "o" or \
                board[0][1] == board[1][1] == board[2][1] == "o" or board[0][2] == board[1][2] == board[2][2] == "o" or \
                board[0][0] == board[1][1] == board[2][2] == "o" or board[0][2] == board[1][1] == board[2][0] == "o":
            compscore += 1; start = True
        elif board[0][0] != 0 and board[0][1] != 0 and board[0][2] != 0 and board[1][0] != 0 and board[1][1] != 0 and \
                board[1][2] != 0 and board[2][0] != 0 and board[2][1] != 0 and board[2][2] != 0:
            start = True

        if userscore == winscore: return True
        elif compscore == winscore: return False

        while not player and not start and oneplayer:  # Computer turn
            if normal and not player:  # Normal module
                for t in ["o", "x"]:
                    for i in range(3):
                        x, y, dr1, dr2, dl1, dl2 = 2, 2, 0, 2, 0, 2
                        for j in range(2):
                            if board[i][j] == t and board[i][j + 1] == t and board[i][x] == 0 and not player:  # Check for X-X-0 (row)
                                board[i][x], player = "o", True
                            else: x = 0
                            if board[j][i] == t and board[j + 1][i] == t and board[y][i] == 0 and not player:  # Check for X-X-0 (column)
                                board[y][i], player = "o", True
                            else: y = 0
                            if board[i][j] == t and board[i][2] == t and board[i][j + 1] == 0 and not player:  # Check for X-0-X (row)
                                board[i][j + 1], player = "o", True
                            if board[j][i] == t and board[2][i] == t and board[j + 1][i] == 0 and not player:  # Check for X-0-X (column)
                                board[j + 1][i], player = "o", True
                            if board[dr1][dr1] == t and board[dr1 + 1][dr1 + 1] == t and board[dr2][dr2] == 0 and not player:  # Check X-X-0 (diagonal - right to left)
                                board[dr2][dr2], player = "o", True
                            else: dr1, dr2 = 1, 0
                            if board[dl1][dl2] == t and board[1][1] == t and board[dl2][dl1] == 0 and not player:  # Check X-X-0 (diagonal - left to right)
                                board[dl2][dl1], player = "o", True
                            else: dl1, dl2 = 2, 0
                            if board[0][0] == t and board[2][2] == t and board[1][1] == 0 and not player:  # Check X-0-X (diagonal - right to left)
                                board[1][1], player = "o", True
                            if board[0][2] == t and board[2][0] == t and board[1][1] == 0 and not player:  # Check X-0-X (diagonal - left to right)
                                board[1][1], player = "o", True
                if hard and not player:  # Hard module
                    if board[1][0] == "x" and board[0][2] == "x" and board[0][0] == 0:
                        board[0][0], player = "o", True
                    elif board[1][2] == "x" and board[0][0] == "x" and board[0][2] == 0:
                        board[0][2], player = "o", True
                    elif board[1][0] == "x" and board[2][2] == "x" and board[2][0] == 0:
                        board[2][0], player = "o", True
                    elif board[1][2] == "x" and board[2][0] == "x" and board[2][2] == 0:
                        board[2][2], player = "o", True
                    elif (board[0][0] == "x" or board[0][2] == "x" or board[2][0] == "x" or board[2][2] == "x") and board[1][1] == 0:  # Check Edges
                        board[1][1], player = "o", True
                    elif board[0][1] == "x" and board[2][1] == 0:
                        board[2][1], player = "o", True
                    elif board[1][0] == "x" and board[1][2] == 0:
                        board[1][2], player = "o", True
                    elif board[1][2] == "x" and board[1][0] == 0:
                        board[1][0], player = "o", True
                    elif board[2][1] == "x" and board[0][1] == 0:
                        board[0][1], player = "o", True
                    elif board[1][1] == "x" and board[0][2] == 0:  # Check Middle
                        board[0][2], player = "o", True
                    elif board[1][1] == "x" and board[2][0] == "x" and board[2][2] == 0:
                        board[2][2], player = "o", True
            if easy and not player:  # Easy module
                i = random.randint(0, 2)
                j = random.randint(0, 2)
                if board[i][j] == 0: board[i][j], player = "o", True

        screen.fill(white)

        for i in range(3):
            draw(resource_path("./Layout/BlackCircle.png"), 100 + 38*i, 47)
            draw(resource_path("./Layout/BlackCircle.png"), 440 + 38*i, 47)
        for i in range(userscore): draw(resource_path("./Layout/BlueCircle.png"), 100 + 38*i, 47)
        for i in range(compscore): draw(resource_path("./Layout/RedCircle.png"), 440 + 38*i, 47)

        for i in range(3):
            for j in range(3):
                Buttons[i][j].show(mouse, board[i][j] == 0, br=br)

        # Display Symbols
        x, y = 150, 197
        for i in range(3):
            for j in range(3):
                if board[i][j] == "x": draw(resource_path("./Layout/X.png"), x, y)
                elif board[i][j] == "o": draw(resource_path("./Layout/O.png"), x, y)
                x += 129
            x = 150; y += 129

        pygame.display.update(), clock.tick(25)


def Menu(mode=True):
    OnePlayer = Button("Singleplayer", "Long Gray", 200, 390, (240, 40))
    TwoPlayer = Button("Multiplayer", "Long Gray", 200, 445, (240, 40))
    Easy = Button("Fácil", "Gray", 220, 335, (200, 40))
    Medium = Button("Normal", "Gray", 220, 390, (200, 40))
    Hard = Button("Difícil", "Gray", 220, 445, (200, 40))
    Return = Button("Voltar", "Gray", 25, 555, (200, 40))

    while True:
        mouse = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: sys.exit()

            if mode:
                if OnePlayer.click(event): mode = False; break
                if TwoPlayer.click(event): TicTacToe(False)
            if not mode:
                if Easy.click(event): TicTacToe(True)
                if Medium.click(event): TicTacToe(True, True, True)
                if Hard.click(event): TicTacToe(True, True, True, True)
                if Return.click(event): mode = True

        screen.fill(white)

        centerprint("TicTacToe", 220, 100, 200, 20, font=font81)

        if mode: OnePlayer.show(mouse, rand=True), TwoPlayer.show(mouse, rand=True)
        if not mode: Easy.show(mouse, rand=True), Medium.show(mouse, rand=True), Hard.show(mouse, rand=True), Return.show(mouse, rand=True)

        pygame.display.update(), clock.tick(25)


if __name__ == "__main__": Menu()
