import itertools
import math
import pygame
from Things import Colors, Fonts, draw, centerPrint, AbstractButton


class Button(AbstractButton):
    def __init__(self, text, pos, size=(121, 121), type="Tile"):
        super().__init__(text, pos, size)
        self.type = type

    def show(self, mouse, enabled=True, player=None):
        if self.under(mouse) and enabled:
            draw(screen, f"assets/{self.type} 2{'' if player is None else 'Blue' if player else 'Red'}.png", self.rect.topleft)
        else:
            draw(screen, f"assets/{self.type}.png", self.rect.topleft)
        centerPrint(screen, self.text, (self.rect.x, self.rect.y - 1), self.rect.size, Colors["lightgray"])


class Tile:
    def __init__(self, pos):
        self.value, self.button = None, Button("", pos)

    def __eq__(self, other):
        return self.value == other.value if self.value is not None else False


class Board:
    def __init__(self, active):
        self.board = [[Tile((128 + 129 * j, 172 + 129 * i)) for i in range(3)] for j in range(3)]
        self.active = active

    def click(self, event):
        if any((tile := self[i][j]).button.click(event, tile.value is None) for i in range(3) for j in range(3)):
            tile.value = self.active
            return True

    def show(self, mouse):
        for i, j in itertools.product(range(3), range(3)):
            self[i][j].button.show(mouse, self[i][j].value is None, player=self.active == "x")
            if self[i][j].value is not None:
                draw(screen, f"assets/{self[i][j].value}.png", (150 + 129 * i, 197 + 129 * j))

    def check(self):
        if (v := self[0][0]) == self[1][1] == self[2][2] or (v := self[0][2]) == self[1][1] == self[2][0] or \
                any((v := self[i][0]) == self[i][1] == self[i][2] or (v := self[0][i]) == self[1][i] == self[2][i] for i in range(3)):
            score[0 if v.value == "x" else 1] += 1
            self.__init__("x")
        if all(self[i][j].value is not None for i in range(3) for j in range(3)):
            self.__init__("x")

    def __getitem__(self, i):
        return self.board[i]


def minMax(state, depth, player):
    best = [-1, -1, (0 if depth == 0 else -math.inf if player == "o" else math.inf)]

    if depth == 0 or (v := state[0][0]) == state[1][1] == state[2][2] or (v := state[0][2]) == state[1][1] == state[2][0] or \
            any((v := state[i][0]) == state[i][1] == state[i][2] or (v := state[0][i]) == state[1][i] == state[2][i] for i in range(3)):
        return [-1, -1, 0 if depth == 0 else -1 if v.value == "x" else 1]

    for cell in [(i, j) for i in range(3) for j in range(3) if state[i][j].value is None]:
        state[cell[0]][cell[1]].value = player
        score = minMax(state, depth - 1, "x" if player == "o" else "o")
        state[cell[0]][cell[1]].value = None
        score[0], score[1] = cell[0], cell[1]

        if player == "o" and score[2] > best[2] or player != "o" and score[2] < best[2]:
            best = score
    return best


def TicTacToe(singleplayer):
    global score
    board, score = Board("x"), [0, 0]

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if board.click(event):
                board.active = "x" if board.active == "o" else "o"
                board.show(mouse), pygame.display.update(), pygame.time.wait(100), board.check()

                if singleplayer and board.active == "o":
                    move = minMax(board, len([(i, j) for i in range(3) for j in range(3) if board[i][j].value is None]), board.active)
                    board[move[0]][move[1]].value, board.active = "o", "x"
                    board.show(mouse), pygame.display.update(), pygame.time.wait(100), board.check()

        if score[0] == winningScore or score[1] == winningScore:
            return score[0] == winningScore

        screen.fill(Colors["white"])
        for i in range(winningScore):
            draw(screen, "assets/images/BlackCircle.png", (100 + 38 * i, 47))
            draw(screen, "assets/images/BlackCircle.png", (440 + 38 * i, 47))
        for i in range(score[0]):
            draw(screen, "assets/images/BlueCircle.png", (100 + 38 * i, 47))
        for i in range(score[1]):
            draw(screen, "assets/images/RedCircle.png", (440 + 38 * i, 47))

        board.show(mouse), pygame.display.update(), pygame.time.Clock().tick(25)


def Menu():
    Singleplayer = Button("Singleplayer", (200, 390), (240, 40), "Long Gray")
    Multiplayer = Button("Multiplayer", (200, 445), (240, 40), "Long Gray")

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if (singleplayer := Singleplayer.click(event)) or Multiplayer.click(event):
                TicTacToe(singleplayer)

        screen.fill(Colors["white"])
        centerPrint(screen, "TicTacToe", (220, 100), (200, 20), Colors["gray"], Fonts["demiBold80"])
        Singleplayer.show(mouse), Multiplayer.show(mouse), pygame.display.update(), pygame.time.Clock().tick(25)


score, winningScore = [0, 0], 3
if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 620))
    pygame.display.set_caption("TicTacToe")
    Menu()
