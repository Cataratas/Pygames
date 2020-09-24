import pygame, random

pygame.display.init(), pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

font81 = pygame.font.Font('./Fonts/berlin-sans-fb-demi-bold.ttf', 81)
white, blue, red = (255, 255, 255), (0, 113, 188), (193, 39, 45)


def centerprint(variable, x, y, sizeX, sizeY, color=(51, 51, 51), font=pygame.font.Font('./Fonts/berlin-sans-fb-demi-bold.ttf', 21)):
    text = font.render(str(variable), True, color)
    rect = pygame.Rect((x, y, sizeX, sizeY))
    text_rect = text.get_rect()
    text_rect.center = rect.center
    screen.blit(text, text_rect)


class button():
    def __init__(self, name, color, x, y, size=(121, 121)):
        self.rect = pygame.Rect((x, y), size)
        self.name = name
        self.color = color

    def show(self, mouse, bool=True, color1=(230, 230, 230), color2=(77, 77, 77), br=None):
        if self.rect.x + self.rect.width > mouse[0] > self.rect.x and self.rect.y + self.rect.height > mouse[
            1] > self.rect.y and bool:
            if br == None:
                draw('./Layout/{} 2.png'.format(self.color), self.rect.x, self.rect.y)
            elif br == True:
                draw('./Layout/{} 2Blue.png'.format(self.color), self.rect.x, self.rect.y)
            elif br == False:
                draw('./Layout/{} 2Red.png'.format(self.color), self.rect.x, self.rect.y)
            centerprint(self.name, self.rect.x, self.rect.y - 1, self.rect.w, self.rect.h, color1)
        else:
            draw('./Layout/{}.png'.format(self.color), self.rect.x, self.rect.y)
            centerprint(self.name, self.rect.x, self.rect.y - 1, self.rect.w, self.rect.h, color2)

    def click(self, event, bool=True):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and bool: return self.rect.collidepoint(event.pos)


def draw(path, x, y):
    screen.blit(pygame.image.load(path), (x, y))


def TicTacToe(oneplayer, easy=True, normal=False, hard=False):
    a1, a2, a3 = button(" ", "Tile", 451, 172), button(" ", "Tile", 580, 172), button(" ", "Tile", 709, 172)
    b1, b2, b3 = button(" ", "Tile", 451, 301), button(" ", "Tile", 580, 301), button(" ", "Tile", 709, 301)
    c1, c2, c3 = button(" ", "Tile", 451, 430), button(" ", "Tile", 580, 430), button(" ", "Tile", 709, 430)
    board, userscore, compscore, winscore, start = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0, 3, True
    if oneplayer:
        active, br = "x", None
    else:
        active = random.choice(["x", "o"])
        if active == "x":
            br = True
        else:
            br = False

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: Menu()

            # Player
            if a1.click(event, board[0][0] == 0): board[0][0], player = active, False
            if a2.click(event, board[0][1] == 0): board[0][1], player = active, False
            if a3.click(event, board[0][2] == 0): board[0][2], player = active, False
            if b1.click(event, board[1][0] == 0): board[1][0], player = active, False
            if b2.click(event, board[1][1] == 0): board[1][1], player = active, False
            if b3.click(event, board[1][2] == 0): board[1][2], player = active, False
            if c1.click(event, board[2][0] == 0): board[2][0], player = active, False
            if c2.click(event, board[2][1] == 0): board[2][1], player = active, False
            if c3.click(event, board[2][2] == 0): board[2][2], player = active, False
            if not (player or oneplayer):
                if active == "x": active, player = "o", True
                else: active, player = "x", True

        if start:
            pygame.time.delay(250)
            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            if oneplayer:
                player, start = True, False
            else:
                active, player, start = random.choice(["x", "o"]), True, False
                if active == "x": br = True
                else: br = False

        if not oneplayer:
            if active == "x": br = True
            else: br = False

        # Player Victory
        if board[0][0] == board[0][1] == board[0][2] == "x" or board[1][0] == board[1][1] == board[1][2] == "x" or \
                board[2][0] == board[2][1] == board[2][2] == "x" or board[0][0] == board[1][0] == board[2][0] == "x" or \
                board[0][1] == board[1][1] == board[2][1] == "x" or board[0][2] == board[1][2] == board[2][2] == "x" or \
                board[0][0] == board[1][1] == board[2][2] == "x" or board[0][2] == board[1][1] == board[2][0] == "x":
            userscore += 1
            start = True

        # Computer Victory
        elif board[0][0] == board[0][1] == board[0][2] == "o" or board[1][0] == board[1][1] == board[1][2] == "o" or \
                board[2][0] == board[2][1] == board[2][2] == "o" or board[0][0] == board[1][0] == board[2][0] == "o" or \
                board[0][1] == board[1][1] == board[2][1] == "o" or board[0][2] == board[1][2] == board[2][2] == "o" or \
                board[0][0] == board[1][1] == board[2][2] == "o" or board[0][2] == board[1][1] == board[2][0] == "o":
            compscore += 1
            start = True

        # Draw
        elif board[0][0] != 0 and board[0][1] != 0 and board[0][2] != 0 and board[1][0] != 0 and board[1][1] != 0 and \
                board[1][2] != 0 and board[2][0] != 0 and board[2][1] != 0 and board[2][2] != 0:
            start = True

        # Player Victory
        if userscore == winscore: return True

        # Computer Victory
        elif compscore == winscore: return False

        while not player and not start and oneplayer:  # Computer turn
            if not player and normal:  # Normal module
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
                if hard:  # Hard module
                    if board[1][0] == "x" and board[0][2] == "x" and board[0][0] == 0 and not player:
                        board[0][0], player = "o", True
                    if board[1][2] == "x" and board[0][0] == "x" and board[0][2] == 0 and not player:
                        board[0][2], player = "o", True
                    if board[1][0] == "x" and board[2][2] == "x" and board[2][0] == 0 and not player:
                        board[2][0], player = "o", True
                    if board[1][2] == "x" and board[2][0] == "x" and board[2][2] == 0 and not player:
                        board[2][2], player = "o", True
                    if (board[0][0] == "x" or board[0][2] == "x" or board[2][0] == "x" or board[2][2] == "x") and board[1][1] == 0 and not player:  # Check Edges
                        board[1][1], player = "o", True
                    if board[0][1] == "x" and board[2][1] == 0 and not player:
                        board[2][1], player = "o", True
                    if board[1][0] == "x" and board[1][2] == 0 and not player:
                        board[1][2], player = "o", True
                    if board[1][2] == "x" and board[1][0] == 0 and not player:
                        board[1][0], player = "o", True
                    if board[2][1] == "x" and board[0][1] == 0 and not player:
                        board[0][1], player = "o", True
                    if board[1][1] == "x" and board[0][2] == 0 and not player:  # Check Middle
                        board[0][2], player = "o", True
                    if board[1][1] == "x" and board[2][0] == "x" and board[2][2] == 0 and not player:
                        board[2][2], player = "o", True
            if not player and easy:  # Easy module
                i = random.randint(0, 2)
                j = random.randint(0, 2)
                if board[i][j] == 0: board[i][j], player = "o", True

        screen.fill(white)

        for i in range(3):  # winscore = 3
            draw("./Layout/BlackCircle.png", 400 + 38 * i, 47)
            draw("./Layout/BlackCircle.png", 778 + 38 * i, 47)
        for i in range(userscore):
            draw("./Layout/BlueCircle.png", 400 + 38 * i, 47)
        for i in range(compscore):
            draw("./Layout/RedCircle.png", 778 + 38 * i, 47)

        a1.show(mouse, board[0][0] == 0, br=br), a2.show(mouse, board[0][1] == 0, br=br), a3.show(mouse, board[0][2] == 0, br=br)
        b1.show(mouse, board[1][0] == 0, br=br), b2.show(mouse, board[1][1] == 0, br=br), b3.show(mouse, board[1][2] == 0, br=br)
        c1.show(mouse, board[2][0] == 0, br=br), c2.show(mouse, board[2][1] == 0, br=br), c3.show(mouse, board[2][2] == 0, br=br)

        # Display Symbols
        x, y = 475, 197
        for i in range(3):
            for j in range(3):
                if board[i][j] == "x": draw("./Layout/X.png", x, y)
                elif board[i][j] == "o": draw("./Layout/O.png", x, y)
                x += 129
            x = 475
            y += 129

        pygame.display.update(), clock.tick(25)


def Menu(mode=True):
    OnePlayer = button("Singleplayer", "Gray", 540, 390, (200, 40))
    TwoPlayer = button("Multiplayer", "Gray", 540, 445, (200, 40))
    Easy = button("Fácil", "Gray", 325, 410, (200, 40))
    Medium = button("Normal", "Gray", 540, 410, (200, 40))
    Hard = button("Difícil", "Gray", 755, 410, (200, 40))
    Return = button("Voltar", "Gray", 25, 655, (200, 40))

    while True:
        mouse = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: quit()

            if mode is True:
                if OnePlayer.click(event): mode = False; break
                if TwoPlayer.click(event): TicTacToe(False)
            if mode is False:
                if Easy.click(event): TicTacToe(True)
                if Medium.click(event): TicTacToe(True, True, True)
                if Hard.click(event): TicTacToe(True, True, True, True)
                if Return.click(event): mode = True

        screen.fill(white)

        centerprint("TicTacToe", 340, 100, 600, 100, font=font81)

        if mode is True: OnePlayer.show(mouse), TwoPlayer.show(mouse)
        if mode is False: Easy.show(mouse), Medium.show(mouse), Hard.show(mouse), Return.show(mouse)

        pygame.display.update(), clock.tick(30)


if __name__ == "__main__": Menu()
