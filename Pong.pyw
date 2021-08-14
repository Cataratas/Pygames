import pygame
import time
import random
import math
import sys
import os

pygame.display.init(), pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


pygame.display.set_caption("Pong")

font21 = pygame.font.Font(resource_path(resource_path("./Fonts/BIG JOHN.otf")), 21)
font36 = pygame.font.Font(resource_path(resource_path("./Fonts/BIG JOHN.otf")), 36)
font70 = pygame.font.Font(resource_path(resource_path("./Fonts/BIG JOHN.otf")), 70)
white, gray, black = (255, 255, 255), (77, 77, 77), (25, 25, 25)
blue, red = (0, 113, 188), (165, 2, 39)


def centerprint(variable, x, y, sizeX, sizeY, color=gray, font=font36):
    text = font.render(str(variable), True, color)
    rect = pygame.Rect((x, y, sizeX, sizeY))
    text_rect = text.get_rect()
    text_rect.centerx = rect.centerx
    text_rect.centery = rect.centery
    screen.blit(text, text_rect)


class Button:
    def __init__(self, text, x, y, w, h, color):
        self.t = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = color
        self.rect = pygame.Rect((x, y), (w, h))

    def show(self, mouse):
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(screen, self.c, [self.x, self.y, self.w, self.h])
        else:
            pygame.draw.rect(screen, gray, [self.x, self.y, self.w, self.h])
        centerprint(self.t, self.x, self.y + 2, self.w, self.h, black, font21)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos)


def map(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


def Pong(AI):
    largura, altura = 1280, 720
    square = pygame.Rect(largura / 2 - 36.5, altura / 2 - 36.5, 75, 75)
    top = pygame.Rect(0, 72, 1280, 1); bottom = pygame.Rect(0, 695, 1280, 1)

    comp, user, winscore, start, count = 0, 0, 3, True, True
    PRD, PRU, PLD, PLU = False, False, False, False
    PaddleRight, PaddleLeft, xspeed, yspeed, x1, y1, r = None, None, 0, 0, 0, 0, 10
    x, y, xspeed1, yspeed1, ball = 0, 0, 0, 0, None

    while True:
        mouse = pygame.mouse.get_pos()

        # Start the Game
        if start:
            x, y = largura / 2, altura / 2
            x1, y1 = x, y
            PaddleLeft = pygame.Rect(16, 172, 16, 136)
            PaddleRight = pygame.Rect(1248, 172, 16, 136)
            ball = pygame.Rect(x, y, r * 2, r * 2)
            xspeed = 6 * math.cos(3.14 / 4)
            yspeed = 6 * math.sin(3.14 / 4)
            xspeed1, yspeed1 = xspeed, yspeed
            if random.choice([1, 2]) == 1: xspeed *= -1; xspeed1 *= -1
            start = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            # Keyboard Control
            if not AI:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: PRD = True
                    if event.key == pygame.K_UP: PRU = True
                    if event.key == pygame.K_s: PLD = True
                    if event.key == pygame.K_w: PLU = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN: PRD = False
                    if event.key == pygame.K_UP: PRU = False
                    if event.key == pygame.K_s: PLD = False
                    if event.key == pygame.K_w: PLU = False

        if not AI:
            if PRD and (PaddleRight.y + PaddleRight.h) < 695: PaddleRight.y += 7
            if PRU and PaddleRight.y > 72: PaddleRight.y -= 7
            if PLD and (PaddleLeft.y + PaddleLeft.h) < 695: PaddleLeft.y += 7
            if PLU and PaddleLeft.y > 72: PaddleLeft.y -= 7

        # A.I.
        if AI and xspeed < 0:
            ball2 = pygame.Rect(x1, y1, r * 2, r * 2)
            x1 += xspeed1 * 1.25
            y1 += yspeed1 * 1.25
            if PaddleLeft.y <= 72 and ball2.y < 72 + PaddleLeft.height / 2:
                PaddleLeft.y = 72 + 2
            elif PaddleLeft.centery < ball2.centery:
                PaddleLeft.centery += 2
            if PaddleLeft.y + PaddleRight.height >= 695 - 2 and ball2.y > 695 - PaddleLeft.height / 2:
                PaddleLeft.y = 695 - PaddleLeft.height
            elif PaddleLeft.centery > ball2.centery:
                PaddleLeft.centery -= 2

        # Mouse Control
        if AI:
            if PaddleRight.y <= 72 and mouse[1] - PaddleRight.height / 2 <= 72:
                PaddleRight.y = 72
            elif (PaddleRight.y + PaddleRight.height) >= 695 and mouse[1] + PaddleRight.height / 2 >= 695:
                PaddleRight.y = 695 - PaddleRight.height
            else:
                PaddleRight.centery = mouse[1]

        # Right Paddle Ball Collision
        if PaddleRight.colliderect(ball):
            diff = y - ((PaddleRight.top + 72) - PaddleRight.height / 2)
            angle = map(diff, 0, PaddleRight.height, math.radians(225), math.radians(135))
            xspeed = 6 * math.cos(angle)
            yspeed = 6 * math.sin(angle)
            x = PaddleRight.x - PaddleRight.width - r
            x1, y1, xspeed1, yspeed1 = x, y, xspeed, yspeed

        # Left Paddle Ball Collision
        if PaddleLeft.colliderect(ball):
            diff = y - ((PaddleLeft.top + 72) - PaddleLeft.height / 2)
            angle = map(diff, 0, PaddleLeft.height, math.radians(-45), math.radians(45))
            xspeed = 6 * math.cos(angle)
            yspeed = 6 * math.sin(angle)
            x = PaddleLeft.x + PaddleLeft.width + r

        # Freezes A.I. ball
        if x1 < 0: xspeed1, yspeed1 = 0, 0

        # Reverse Y (top and bottom limits)
        if y < 77 or y > altura - 38: yspeed *= -1
        if y1 < 77 or y1 > altura - 38: yspeed1 *= -1

        # Resets Game
        if x > largura - r * 2 or x < 0:
            if x > largura - r * 2:
                comp += 1
            else:
                user += 1

            # End
            if user == winscore: return True
            elif comp == winscore: return False

            count = True

        ball = pygame.Rect(x, y, r * 2, r * 2)
        x += xspeed
        y += yspeed

        # Draw Everything to Screen
        screen.fill(black)

        pygame.draw.rect(screen, red, PaddleLeft)
        pygame.draw.rect(screen, blue, PaddleRight)
        pygame.draw.circle(screen, (204, 204, 204), (ball.x + 10, ball.y + 10), 10)
        pygame.draw.rect(screen, gray, top), pygame.draw.rect(screen, gray, bottom)
        centerprint(comp, 536, 15, 50, 60, red, font70), centerprint(user, 696, 15, 50, 60, blue, font70)
        centerprint(winscore, 495, 23, 20, 34), centerprint(winscore, 765, 23, 20, 34)

        if count:
            startTime = time.time()
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: return False

                # Countdown
                seconds = round(int(time.time() - startTime))
                if seconds < 3:
                    pygame.draw.rect(screen, black, square)
                    centerprint(3 - seconds, largura / 2 - 36.5, altura / 2 - 36.5, 75, 75, font=font70)
                if seconds == 3:
                    start = True; break

                pygame.display.update(); clock.tick(120)
            count = False

        pygame.display.update(); clock.tick(120)


def Menu():
    Singleplayer = Button("Singleplayer", 430, 390, 200, 40, blue)
    Multiplayer = Button("Multiplayer", 650, 390, 200, 40, red)
    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if Singleplayer.click(event): Pong(True)
            if Multiplayer.click(event): Pong(False)

        screen.fill(black)
        centerprint("Pong", 340, 100, 600, 100, font=font70)

        Singleplayer.show(mouse), Multiplayer.show(mouse)

        pygame.display.update(); clock.tick(15)


if __name__ == "__main__": Menu()
