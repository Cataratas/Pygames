import pygame, random

pygame.display.init(), pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

font81 = pygame.font.Font('./Fonts/berlin-sans-fb-demi-bold.ttf', 81)
fontABC = pygame.font.Font('./Fonts/myriad-pro-8.otf', 40)
fontW = pygame.font.Font('./Fonts/myriad-pro-8.otf', 36)
white, black = (255, 255, 255), (51, 51, 51)


def centerprint(variable, x, y, sizeX, sizeY, color=(51, 51, 51), font=pygame.font.Font('./Fonts/myriad-pro-8.otf', 21)):
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
            centerprint(self.name, self.rect.x, self.rect.y, self.rect.w, self.rect.h, color1)
        else:
            draw('./Layout/{}.png'.format(self.color), self.rect.x, self.rect.y)
            centerprint(self.name, self.rect.x, self.rect.y, self.rect.w, self.rect.h, color2)

    def click(self, event, bool=True):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and bool: return self.rect.collidepoint(event.pos)


def draw(path, x, y, mirror=False):
    if mirror: screen.blit(pygame.transform.flip(pygame.image.load(path), True, False), (x, y))
    else: screen.blit(pygame.image.load(path).convert_alpha(), (x, y))


def Hangman():
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    list = ["presidente", "escola", "esquecer", "correr", "peixe", "fuja", "assustador", "procure", "juventude", "mundo", "marte", "estados", "derrota", "contando", "estrelas", "universo", "eletricidade", "hotel", "ouro", "dinheiro", "mentir", "sonhar",
            "amanhecer", "desconhecido", "ajudar", "felicidade", "amizade", "desconfiar", "concorrer", "auxiliar", "temperatura", "animal", "advogado", "liberdade", "denunciar", "conhecer", "desculpa", "poder", "achar", "computador", "bicicleta", "vergonha"]
    word = list[random.randint(0, len(list))]
    letters, life = [], 7

    while True:
        for i in range(len(word)):
            if word[i] not in letters: win = False; break
            win = True
        if win: pygame.time.delay(3000); return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT: Menu()

            for i in alphabet:  # Bug: Multiple key pressings not registering lives correctly
                if event.type == pygame.TEXTINPUT and event.text.lower() == i and i not in letters:
                    letters.append(event.text.lower())
                    if event.text not in word: life -= 1

        screen.fill(white)

        draw("./Layout/Post.png", 292, 198)
        if life <= 6: draw("./Layout/Head.png", 393, 235)
        if life <= 5: draw("./Layout/Body.png", 417, 285)
        if life <= 4: draw("./Layout/Leg.png", 390, 351)
        if life <= 3: draw("./Layout/Leg.png", 416, 351, True)
        if life <= 2: draw("./Layout/Arm.png", 398, 296)
        if life <= 1: draw("./Layout/Arm.png", 417, 296, True)
        if life == 0:
            draw("./Layout/Face.png", 405, 250)
            pygame.display.update(), pygame.time.delay(3000)
            return False

        x = 685
        for i in word:
            if i in letters: centerprint(i.upper(), x, 396, 15, 15, black, fontW)
            draw("./Layout/Blanks.png", x-6, 412)
            x += 30

        x = 259
        for i in range(len(alphabet)):
            if alphabet[i] in letters and alphabet[i] in word:
                centerprint(alphabet[i].upper(), x, 650, 15, 15, (140, 198, 63), fontABC)
            elif alphabet[i] in letters:
                centerprint(alphabet[i].upper(), x, 650, 15, 15, (193, 39, 45), fontABC)
            else: centerprint(alphabet[i].upper(), x, 650, 15, 15, (230, 230, 230), fontABC)
            x += 30

        pygame.display.update(), clock.tick(25)


def Menu():
    Play = button("Jogar", "Gray", 540, 390, (200, 40))
    Exit = button("Sair", "Gray", 540, 440, (200, 40))

    while True:
        mouse = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or Exit.click(event): quit()
            elif Play.click(event): Hangman()

        screen.fill(white)

        centerprint("Hangman", 340, 100, 600, 100, font=font81)

        Play.show(mouse), Exit.show(mouse)

        pygame.display.update(), clock.tick(25)


if __name__ == "__main__": Menu()
