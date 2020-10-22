import pygame
import pygame.freetype
import random
import time
import sys
import os

pygame.display.init(), pygame.freetype.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))


def resource_path(relative_path):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


font50 = pygame.freetype.Font(resource_path("./Fonts/seguiemj.ttf"), 50)
white = (255, 255, 255)


def centerprint(variable, x, y, sizeX, sizeY, color, font=font50):
	color = color[:-1] + (255, )
	text = font.render(str(variable), color)
	rect = pygame.Rect((x, y, sizeX, sizeY))
	text_rect = text[0].get_rect()
	text_rect.center = rect.center
	screen.blit(text[0], text_rect)


class Tile:
	def __init__(self, symbol, color):
		self.symbol = symbol
		self.color = color
		self.visible = False
		self.paired = False

	def show(self, x, y, mouse, tile, w=121):
		s = pygame.Surface((w, w), pygame.SRCALPHA)
		s.fill((230, 230, 230))
		if mouse == tile: s.fill((214, 214, 214))
		if self.visible or self.paired:
			s.fill(self.color)
			centerprint(self.symbol, x, y, w, w, self.color)
		screen.blit(s, (x, y))


def Memory():
	rows, columns, flips, check, startTime, first, second = 5, 8, 0, False, None, None, None
	start, startTime, seconds = True, time.time(), 0

	symbols = [["⚓", (251, 176, 59, 75)], ["🍇", (102, 45, 145, 75)], ["♻", (57, 181, 74, 75)], ["🐟", (41, 171, 226, 75)], ["💼", (117, 76, 36, 75)], ["🗽", (0, 169, 157, 75)], ["🛰", (27, 20, 100, 75)], ["🧠", (255, 123, 172, 75)], ["🦋", (163, 123, 15, 75)], ["🦊", (241, 90, 36, 75)], ["🦉", (199, 178, 153, 75)], ["🦅", (58, 46, 0, 75)], ["🔮", (160, 113, 167, 75)], ["👽", (0, 104, 55, 75)], ["☂", (0, 113, 188, 75)], ["🐦", (193, 39, 45, 75)], ["👁", (131, 138, 150, 75)], ["🌷", (216, 149, 164, 75)], ["❄", (161, 205, 231, 75)], ["⛄", (136, 157, 201, 75)]]
	symbols += symbols
	random.shuffle(symbols)

	grid = [["" for y in range(columns)] for x in range(rows)]
	for i in range(rows):
		for j in range(columns):
			if grid[i][j] == "":
				grid[i][j] = Tile(symbols[-1][0], symbols[-1][1])
				del symbols[-1]

	while True:
		mouse = pygame.mouse.get_pos()
		mx, my = (mouse[1]-43)//128, (mouse[0]-126)//128

		if start:
			seconds = round(int(time.time() - startTime))
			for i in range(rows):
				for j in range(columns):
					grid[i][j].visible = True
			if seconds > 3:
				for i in range(rows):
					for j in range(columns):
						grid[i][j].visible = False
				start = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				if 0 <= mx < rows and 0 <= my < columns and not grid[mx][my].paired and not grid[mx][my].visible and second is None:
					grid[mx][my].visible = True
					if flips == 0: first = grid[mx][my]
					elif flips == 1: second = grid[mx][my]
					flips += 1
					if flips == 2: check = True; startTime = time.time()

		screen.fill(white)
		x, y = 131, -85
		win = True
		for i in range(rows):
			y += 128
			x = 131
			for j in range(columns):
				grid[i][j].show(x, y, (mx, my), (i, j))
				if not grid[i][j].paired: win = False
				x += 128

		if win: return True

		if first is not None and second is not None and first.symbol == second.symbol:
			first.paired, second.paired = True, True
			first, second = None, None
			flips, check = 0, False

		if startTime is not None: seconds = round(int(time.time() - startTime))

		if check and seconds >= 1:
			first.visible, second.visible = False, False
			first, second = None, None
			flips, check = 0, False

		pygame.display.update()
		clock.tick(25)


if __name__ == "__main__": Memory()
