import pygame
import random
import time
import sys
import os

pygame.display.init(), pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

black, s_darkgray, darkgray, gray, gray2, white = (0, 0, 0), (51, 51, 51), (91, 91, 91), (71, 71, 71), (138, 138, 138), (255, 255, 255)
darkred, red, lightgray = (141, 39, 45), (193, 39, 45), (153, 153, 153)
darkblue, blue, lightblue, lighterblue = (0, 75, 188), (0, 113, 188), (41, 146, 226), (41, 171, 226)
lightorange, orange = (247, 127, 45), (247, 107, 30)
darkgreen, green, lightgreen = (0, 175, 69), (0, 146, 69), (72, 181, 89)


def resource_path(relative_path):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


fontUI81 = pygame.font.Font(resource_path("./Fonts/seguisym.ttf"), 81)
font21 = pygame.font.Font(resource_path("./Fonts/berlin-sans-fb-demi-bold.ttf"), 21)


def centerprint(variable, x, y, sizeX, sizeY, color=(51, 51, 51), font=font21):
	text = font.render(str(variable), True, color)
	rect = pygame.Rect((x, y, sizeX, sizeY))
	text_rect = text.get_rect()
	text_rect.center = rect.center
	screen.blit(text, text_rect)


class ButtonBox:
	def __init__(self, number, x, y, w, h):
		self.number = number
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.rect = pygame.Rect((x, y), (self.w, self.h))
		
	def show(self, mouse):
		if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y:
			pygame.draw.rect(screen, darkgray, [self.x, self.y, self.w, self.h])
			centerprint(self.number, self.x, self.y, self.w, self.h, (220, 220, 220))
		else:
			pygame.draw.rect(screen, (220, 220, 220), [self.x, self.y, self.w, self.h])
			pygame.draw.rect(screen, darkgray, pygame.Rect((self.x, self.y, self.w, self.h)), 1)
			centerprint(self.number, self.x, self.y, self.w, self.h, darkgray)
				
	def click(self, event):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1: return self.rect.collidepoint(event.pos)


def draw(path, x, y):
	screen.blit(pygame.image.load(path), (x, y))


def Minesweeper(bombs):
	class Tile:
		def __init__(self):
			self.bomb = False
			self.near = 0
			self.visible = False
			self.flag = False
			self.doubt = False

	global flags, startTime1, seconds
	width, rows, columns, flags = 40, 16, 32, bombs
	lose, seconds1, startTime, minutes = False, None, time.time(), 0
	grid = [[Tile() for y in range(columns)] for x in range(rows)]  # Generate the grid

	def bombcounter(x, y):  # Checks for bombs around tile
		bombnear = 0
		for (cx, cy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
			try:
				if y+cy < 0 or x+cx < 0:  # Avoid off grid checking
					raise IndexError
				if grid[y+cy][x+cx].bomb: 
					bombnear += 1
					grid[y][x].near = bombnear
				grid[y][x].visible = True
			except IndexError:
				pass

	def search(x, y, rows=rows, columns=columns):
		global flags
		if 0 <= x < columns and 0 <= y < rows:
			tile = grid[y][x]
			if tile.visible or tile.bomb:  # Stop when it reaches an already visited tile or tile is a bomb
				return
			bombcounter(x, y)  # Counts the number of adjacent bombs
			if tile.near > 0:
				if tile.flag:
					flags += 1
				return
			if tile.flag:
				flags += 1
			tile.visible = True
			for (cx, cy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
				search(x+cx, y+cy)

	for b in range(bombs):  # Place the bombs
		while True:
			x = random.randint(0, rows-1)
			y = random.randint(0, columns-1)
			if not grid[x][y].bomb:
				grid[x][y].bomb = True
				break

	while True: 
		if lose:  # Defeat
			if seconds1 is None: startTime1 = time.time()
			seconds1 = round(int(time.time() - startTime1))
			if seconds1 > 3: return False

		win = True
		for r in grid:
			for t in r:
				if t.bomb and not t.flag:
					win = False; break
		if win:  # Victory
			if seconds1 is None: startTime1 = time.time()
			seconds1 = round(int(time.time() - startTime1))
			if seconds1 > 3: return True

		mouse = pygame.mouse.get_pos()
		if not win and not lose:  # Stop Counter if Game Ends
			seconds = round(int(time.time() - startTime))
		if seconds > 59:
			startTime = time.time()
			minutes += 1
			pygame.time.delay(50)

		screen.fill(white)

		pygame.draw.rect(screen, orange, pygame.Rect((409, 20, 110, 37)), 1)
		pygame.draw.rect(screen, gray, pygame.Rect((762, 20, 110, 37)), 1)
		centerprint(flags, 409, 20, 110, 37, orange)
		centerprint("{}:{}".format("{:02d}".format(minutes), "{:02d}".format(seconds)), 762, 20, 110, 37, gray)

		mx = mouse[0]//width
		my = mouse[1]//width-2
		y = width*2  # Display the grid *2
		for row in grid:
			x = 0  # width*1
			for tile in row:
				if tile.bomb and not tile.flag:
					win = False
				if tile.bomb and lose:  # Display tiles with bombs
					pygame.draw.rect(screen, red, [x, y, width, width])
				else:  # Display not visible tiles
					pygame.draw.rect(screen, lightgray, [x, y, width, width])
				if tile.flag and not lose:  # Display flagged tiles
					pygame.draw.rect(screen, lightorange, [x, y, width, width])
				if tile.doubt and not lose:  # Display doubted tiles
					pygame.draw.rect(screen, lightgreen, [x, y, width, width])
				if tile.visible and not tile.bomb:  # Display quantity of near bombs
					pygame.draw.rect(screen, white, [x, y, width, width])
					if tile.near == 1:
						centerprint(tile.near, x, y, width, width, blue)
					elif tile.near == 2:
						centerprint(tile.near, x, y, width, width, green)
					elif tile.near == 3:
						centerprint(tile.near, x, y, width, width, red)
					elif tile.near == 4:
						centerprint(tile.near, x, y, width, width, darkblue)
					elif tile.near == 5:
						centerprint(tile.near, x, y, width, width, darkred)
					elif tile.near > 5:
						centerprint(tile.near, x, y, width, width, s_darkgray) 
				if not tile.visible:  # Display Grid
					rect1 = pygame.Rect((x, y, width+1, width+1))
					pygame.draw.rect(screen, black, rect1, 1)
				if tile.visible:
					rect = pygame.Rect((x, y, width+1, width+1))
					pygame.draw.rect(screen, darkgray, rect, 1)
				if 0 <= mx < columns and 0 <= my < rows and grid[my][mx].near == 0 and not lose and not grid[my][mx].visible and not win:  # Mouse following
					if grid[my][mx].flag:
						pygame.draw.rect(screen, orange, [mx*width, my*width+width*2, width, width])
					if grid[my][mx].doubt:
						pygame.draw.rect(screen, darkgreen, [mx*width, my*width+width*2, width, width])
					if not grid[my][mx].flag and not grid[my][mx].doubt:
						pygame.draw.rect(screen, gray2, [mx*width, my*width+width*2, width, width])
					rect = pygame.Rect((mx*width, my*width+width*2, width+1, width+1))
					pygame.draw.rect(screen, black, rect, 1)
				x += width
			y += width

		for event in pygame.event.get():  # Check events
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.MOUSEBUTTONDOWN and not lose and not win:
				if event.button == 1 and 0 <= mx < columns and 0 <= my < rows:
					if not grid[my][mx].flag:  # Lock flagged tile
						search(mx, my)
						if grid[my][mx].bomb:  # Checks Defeat
							lose = True
				if event.button == 3 and 0 <= mx < columns and 0 <= my < rows:  # Flag clicked tile
					if not grid[my][mx].visible:
						if grid[my][mx].flag:
							grid[my][mx].flag = False
							grid[my][mx].doubt = True
							flags += 1
						else:
							if flags > 0 and not grid[my][mx].doubt:
								grid[my][mx].flag = True
								flags -= 1
							else: grid[my][mx].doubt = False

		pygame.display.update(); clock.tick(30)


def Menu():
	Easy = ButtonBox("Fácil", 370, 400, 160, 40)
	Medium = ButtonBox("Médio", 560, 400, 160, 40)
	Hard = ButtonBox("Difícil", 750, 400, 160, 40)
	
	while True:
		mouse = pygame.mouse.get_pos()
		
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT: sys.exit()
			
			if Easy.click(event): Minesweeper(45)
			if Medium.click(event): Minesweeper(65)
			if Hard.click(event): Minesweeper(95)
						
		screen.fill(white)
		centerprint("Minesweeper", 340, 100, 600, 100, font=fontUI81)
		
		Easy.show(mouse), Medium.show(mouse), Hard.show(mouse)
		
		pygame.display.update(); clock.tick(15)


if __name__ == "__main__": Menu()
