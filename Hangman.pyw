import string
import pygame
import random
import json
from Things import Colors, Fonts, centerPrint, draw, AbstractButton


class Button(AbstractButton):
    def __init__(self, text, type, pos):
        super().__init__(text, pos, (200, 40))
        self.type = type

    def show(self, mouse):
        if self.under(mouse):
            draw(screen, f"Assets/{self.type} 2.png", self.rect.topleft)
            centerPrint(screen, self.text, self.rect.topleft, self.rect.size, Colors.WHITE, Fonts.Myriad21)
        else:
            draw(screen, f"Assets/{self.type}.png", self.rect.topleft)
            centerPrint(screen, self.text, self.rect.topleft, self.rect.size, Colors.DARKGRAY, Fonts.Myriad21)


def Hangman(words=json.load(open("./Assets/words.json"))):
    word, alphabet, letters, lives = random.choice(words).upper(), list(string.ascii_uppercase), [], 7

    while True:
        if all(letter in letters for letter in word):
            pygame.time.delay(3000)
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.TEXTINPUT and event.text.upper() in alphabet and event.text.upper() not in letters:
                letters.append(event.text.upper())
                if event.text.upper() not in word:
                    lives -= 1

        screen.fill(Colors["white"])
        draw(screen, "Assets/Post.png", (292, 198))
        if lives <= 6:
            draw(screen, "Assets/Head.png", (393, 235))
        if lives <= 5:
            draw(screen, "Assets/Body.png", (417, 285))
        if lives <= 4:
            draw(screen, "Assets/Leg.png", (390, 351))
        if lives <= 3:
            draw(screen, "Assets/Leg.png", (416, 351), True)
        if lives <= 2:
            draw(screen, "Assets/Arm.png", (398, 296))
        if lives <= 1:
            draw(screen, "Assets/Arm.png", (417, 296), True)
        if lives == 0:
            draw(screen, "Assets/Face.png", (405, 250))
            [centerPrint(screen, letter, (685 + 30 * i, 396), (15, 15), Colors["red"], Fonts["myriad36"]) for i, letter in enumerate(word)]
            pygame.display.update(), pygame.time.delay(3000)
            return

        for i, letter in enumerate(word):
            if letter in letters:
                centerPrint(screen, letter, (685 + 30 * i, 396), (15, 15), Colors["darkgray"], Fonts["myriad36"])
            draw(screen, "Assets/Blanks.png", (685 + 30 * i - 6, 412))
        for i, letter in enumerate(alphabet):
            centerPrint(screen, letter, (259 + 30 * i, 650), (15, 15), Colors["lightgray3"], Fonts["myriad40"])
            if letter in letters:
                centerPrint(screen, letter, (259 + 30 * i, 650), (15, 15), Colors["green" if letter in word else "red"], Fonts["myriad40"])

        pygame.display.update(), pygame.time.Clock().tick(25)


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Hangman")
    Hangman()
