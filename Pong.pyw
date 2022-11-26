import pygame as pg
import random
import math
from Things import Colors, Fonts, centerPrint, AbstractButton, TimePiece


class Button(AbstractButton):
    def __init__(self, text, pos, size, color):
        super().__init__(text, pos, size)
        self.color = color

    def show(self, mouse):
        pg.draw.rect(screen, self.color if self.under(mouse) else Colors["gray"], self.rect.topleft + self.rect.size)
        centerPrint(screen, self.text, (self.rect.x, self.rect.y + 2), self.rect.size, Colors["black2"], Fonts["bigJohn21"])


def Pong(singleplayer):
    paddleLeft, paddleRight = pg.Rect(16, 172, 16, 136), pg.Rect(1248, 172, 16, 136)
    topLimit, bottomLimit = pg.Rect(0, 72, 1280, 1), pg.Rect(0, 695, 1280, 1)
    score, start, count, timer, r = [0, 0, 3], False, True, TimePiece(), 10
    paddleDir, ballSpeed, ballSpeed2 = [0, 0], [0, 0], [0, 0]
    x, y = x2, y2 = width / 2, height / 2
    ball, ghostBall = pg.Rect(x, y, r * 2, r * 2), None

    while True:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if not singleplayer:
                if event.type == pg.KEYDOWN:
                    for side, keys in enumerate([(pg.K_DOWN, pg.K_UP), (pg.K_s, pg.K_w)]):
                        if event.key in keys:
                            paddleDir[side] = -1 if event.key == keys[0] else 1
                if event.type == pg.KEYUP:
                    for side, keys in enumerate([(pg.K_DOWN, pg.K_UP), (pg.K_s, pg.K_w)]):
                        if event.key in keys:
                            dir = 1 if event.key == keys[0] else -1
                            paddleDir[side] = 0 if paddleDir[side] != dir else dir

        if start:
            x, y = x2, y2 = width / 2, height / 2
            ballSpeed = ballSpeed2[:] = [6 * math.cos(math.pi / 4), 6 * math.sin(math.pi / 4)]
            ballSpeed[0] = ballSpeed2[0] = ballSpeed[0] * (-1 if random.choice([1, 2]) == 1 else 1)
            start = False

        if not singleplayer:
            for side, paddle in enumerate([paddleRight, paddleLeft]):
                if paddleDir[side] == -1 and paddle.y + paddle.h < 693:
                    paddle.y += 7
                elif paddleDir[side] == 1 and paddle.y > 75:
                    paddle.y -= 7
        elif paddleRight.y <= 72 and mouse[1] - paddleRight.height / 2 <= 72:
            paddleRight.y = 72
        elif (paddleRight.y + paddleRight.height) >= 695 and mouse[1] + paddleRight.height / 2 >= 695:
            paddleRight.y = 695 - paddleRight.height
        else:
            paddleRight.centery = mouse[1]

        if ballSpeed[0] < 0 and singleplayer:
            ghostBall = pg.Rect(x2, y2, r * 2, r * 2)
            x2, y2 = x2 + ballSpeed2[0] * 1.25, y2 + ballSpeed2[1] * 1.25
            if ghostBall.x > paddleLeft.x:
                if paddleLeft.y <= 72 and ghostBall.y < 72 + paddleLeft.height / 2:
                    paddleLeft.y = 72 + 2
                elif paddleLeft.centery < ghostBall.centery:
                    paddleLeft.centery += 2
                if paddleLeft.y + paddleRight.height >= 695 - 2 and ghostBall.y > 695 - paddleLeft.height / 2:
                    paddleLeft.y = 695 - paddleLeft.height
                elif paddleLeft.centery > ghostBall.centery:
                    paddleLeft.centery -= 2

        for side, paddle in enumerate([paddleRight, paddleLeft]):
            if paddle.colliderect(ball):
                ballSpeed = ballSpeed2[:] = [ballSpeed[0] * -1, ballSpeed[1]]
                x = (paddle.x - paddle.width - r) if side == 0 else (paddle.x + paddle.width + r)
                x2, y2 = x, y

        if topLimit.colliderect(ball) or bottomLimit.colliderect(ball):
            ballSpeed[1] *= -1
        if y2 < 77 or y2 > height - 38:
            ballSpeed2[1] *= -1

        if (playerWon := score[0] == score[2]) or score[1] == score[2]:
            return playerWon

        ball.x, ball.y = x, y = x + ballSpeed[0], y + ballSpeed[1]
        screen.fill(Colors["black2"])

        pg.draw.rect(screen, Colors["red"], paddleLeft)
        pg.draw.rect(screen, Colors["blue"], paddleRight)
        pg.draw.circle(screen, Colors["lightgray"], (ball.x + r, ball.y + r), r)
        pg.draw.rect(screen, Colors["gray"], topLimit), pg.draw.rect(screen, Colors["gray"], bottomLimit)
        centerPrint(screen, score[1], (640-110, 15), (50, 60), Colors["red"], Fonts["bigJohn70"])
        centerPrint(screen, score[0], (640+110-30, 15), (50, 60), Colors["blue"], Fonts["bigJohn70"])
        centerPrint(screen, f"{score[2]}{' ' * 30}{score[2]}", (640, 23), (20, 34), Colors["gray"], Fonts["bigJohn21"])

        if count and timer.seconds <= 3:
            if timer.seconds == 3:
                timer.reset()
                start, count = True, False
            pg.draw.rect(screen, Colors["black2"], pg.Rect(width / 2 - 36.5, height / 2 - 36.5, 75, 75))
            centerPrint(screen, str(3 - timer.seconds), (width/2 - 36.5, height/2 - 36.5), (75, 75), Colors["gray"], Fonts["bigJohn70"])
        elif not count and ball.x < 0 or ball.x > width:
            score[0 if ball.x < 0 else 1] += 1
            count = True

        timer.update(count), pg.display.update(), pg.time.Clock().tick(120)


def Menu():
    Singleplayer = Button("Singleplayer", (430, 390), (200, 40), Colors["blue"])
    Multiplayer = Button("Multiplayer", (650, 390), (200, 40), Colors["red"])

    while True:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if (singleplayer := Singleplayer.click(event)) or Multiplayer.click(event):
                Pong(singleplayer)

        screen.fill(Colors["black2"])
        centerPrint(screen, "Pong", (340, 100), (600, 100), Colors["gray"], Fonts["bigJohn70"])

        Singleplayer.show(mouse), Multiplayer.show(mouse), pg.display.update(), pg.time.Clock().tick(25)


if __name__ == "__main__":
    screen = pg.display.set_mode((1280, 720))
    width, height = screen.get_size()
    pg.display.set_caption("Pong")
    Menu()
