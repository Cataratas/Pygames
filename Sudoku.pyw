import pygame, time, random

pygame.display.init(), pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))

fontUI81 = pygame.font.Font('./Fonts/seguisym.ttf', 81)
white, black = (255, 255, 255), (0, 0, 0)
numberList=[1,2,3,4,5,6,7,8,9]

def centerprint(variable, x, y, sizeX, sizeY, color = (51, 51, 51) , font = pygame.font.Font('./Fonts/seguisym.ttf', 21)):
	text = font.render(str(variable), True, color)
	rect = pygame.Rect((x, y, sizeX, sizeY))
	text_rect = text.get_rect()
	text_rect.center = rect.center
	screen.blit(text, text_rect)


class ButtonBox():
		def __init__(self, number, x, y, w, h):
			self.number = number
			self.x = x
			self.y = y
			self.w = w
			self.h = h
			self.rect = pygame.Rect((x, y), (self.w, self.h))
		
		def show(self, mouse, active = None):
			if active == self.number: pressed = True
			else: pressed = False
			if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y and not pressed:
				pygame.draw.rect(screen, (117, 76, 36), [self.x, self.y, self.w, self.h])
				centerprint(self.number, self.x, self.y, self.w, self.h, white)
			elif pressed:
				pygame.draw.rect(screen, (96, 56, 19), [self.x, self.y, self.w, self.h])
				centerprint(self.number, self.x, self.y, self.w, self.h, white)
			else:
				pygame.draw.rect(screen, (96, 56, 19), pygame.Rect((self.x, self.y, self.w, self.h)), 1)
				centerprint(self.number, self.x, self.y, self.w, self.h, (96, 56, 19))
				
		def click(self, event):
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1: return self.rect.collidepoint(event.pos)


def Sudoku(difficulty):
	
	def checkGrid(grid):
		for row in range(0,9):
			for col in range(0,9):
				if grid[row][col]==0: return False
		return True 
	
	
	def GenerateSudoku(grid):
		global counter
		#Find next empty cell
		for i in range(0,81):
			row=i//9
			col=i%9
			if grid[row][col]==0:
				random.shuffle(numberList)      
				for value in numberList:
					#Check that this value has not already be used on this row
					if not(value in grid[row]):
						#Check that this value has not already be used on this column
						if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
							#Identify which of the 9 squares we are working on
							square=[]
							if row<3:
								if col<3:
									square=[grid[i][0:3] for i in range(0,3)]
								elif col<6:
									square=[grid[i][3:6] for i in range(0,3)]
								else:  
									square=[grid[i][6:9] for i in range(0,3)]
							elif row<6:
								if col<3:
									square=[grid[i][0:3] for i in range(3,6)]
								elif col<6:
									square=[grid[i][3:6] for i in range(3,6)]
								else:  
									square=[grid[i][6:9] for i in range(3,6)]
							else:
								if col<3:
									square=[grid[i][0:3] for i in range(6,9)]
								elif col<6:
									square=[grid[i][3:6] for i in range(6,9)]
								else:  
									square=[grid[i][6:9] for i in range(6,9)]
							#Check that this value has not already be used on this 3x3 square
							if not value in (square[0] + square[1] + square[2]):
								grid[row][col]=value
								if checkGrid(grid):
									return True
								else:
									if GenerateSudoku(grid):
										return True
				break
		grid[row][col]=0
	
	
	def Remove(grid, difficulty):
		global counter
		attempts = difficulty
		counter=1
		while attempts>0:
			#Select a random cell that is not already empty
			row = random.randint(0,8)
			col = random.randint(0,8)
			while grid[row][col]==0:
				row = random.randint(0,8)
				col = random.randint(0,8)
			#Remember its cell value in case we need to put it back  
			backup = grid[row][col]
			grid[row][col]=0
 
			#Take a full copy of the grid
			copyGrid = []
			for r in range(0,9):
				copyGrid.append([])
				for c in range(0,9):
					copyGrid[r].append(grid[r][c])
  
			#Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
			counter=0      
			solveGrid(copyGrid)   
			#If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
			if counter!=1:
				grid[row][col]=backup
				#We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
				attempts -= 1
	
	
	def solveGrid(grid):
		global counter
		#Find next empty cell
		for i in range(0,81):
			row=i//9
			col=i%9
			if grid[row][col]==0:
				for value in range (1,10):
					#Check that this value has not already be used on this row
					if not(value in grid[row]):
						#Check that this value has not already be used on this column
						if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
							#Identify which of the 9 squares we are working on
							square=[]
							if row<3:
								if col<3:
									square=[grid[i][0:3] for i in range(0,3)]
								elif col<6:
									square=[grid[i][3:6] for i in range(0,3)]
								else:
									square=[grid[i][6:9] for i in range(0,3)]
							elif row<6:
								if col<3:
									square=[grid[i][0:3] for i in range(3,6)]
								elif col<6:
									square=[grid[i][3:6] for i in range(3,6)]
								else:
									square=[grid[i][6:9] for i in range(3,6)]
							else:
								if col<3:
									square=[grid[i][0:3] for i in range(6,9)]
								elif col<6:
									square=[grid[i][3:6] for i in range(6,9)]
								else:
									square=[grid[i][6:9] for i in range(6,9)]
							#Check that this value has not already be used on this 3x3 square
							if not value in (square[0] + square[1] + square[2]):
								grid[row][col]=value
								if checkGrid(grid):
									counter+=1
									break
								else:
									if solveGrid(grid):
										return True
				break
		grid[row][col]=0
	
	
	def ShowSudoku(grid):
		for row in range(9):
			for col in range(9):
				rect = pygame.Rect(((width*11.5)+row*width, (width*3)+col*width, width+1, width+1))
				pygame.draw.rect(screen, (112, 112, 112), rect, 1)
				if grid[row][col] != 0: centerprint(grid[row][col], (width*11.5)+row*width, (width*3)+col*width, width, width)
		for i in range(4):
			pygame.draw.line(screen, black, ((width*11.5), (width*3)+120*i), ((width*20.5), (width*3)+120*i), 3)
			pygame.draw.line(screen, black, ((width*11.5)+120*i, (width*3)), ((width*11.5)+120*i, width*12), 3)
		
	
	Grid = []
	for i in range(9): Grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
	
	width, active, actions = 40, None, []
	startTime, minutes = time.time(), 0
	GenerateSudoku(Grid)
	
	s_grid = []
	for r in range(0,9):
		s_grid.append([])
		for c in range(0,9):
			s_grid[r].append(Grid[r][c])
	
	Remove(Grid, difficulty)
	
	m_grid = []
	for r in range(0,9):
		m_grid.append([])
		for c in range(0,9):
			m_grid[r].append(Grid[r][c])
	
	Delete, Reverse = ButtonBox("✖", 330, 578, 47, 47), ButtonBox("↩", 902, 578, 47, 47)
	One, Two, Three = ButtonBox(1, 387, 578, 47, 47), ButtonBox(2, 444, 578, 47, 47), ButtonBox(3, 501, 578, 47, 47)
	Four, Five, Six = ButtonBox(4, 558, 578, 47, 47), ButtonBox(5, 615, 578, 47, 47), ButtonBox(6, 673, 578, 47, 47)
	Seven, Eight, Nine = ButtonBox(7, 730, 578, 47, 47), ButtonBox(8, 787, 578, 47, 47), ButtonBox(9, 845, 578, 47, 47)
	
	while True:
		mouse = pygame.mouse.get_pos()
		mx, my = (mouse[0]-20)//width-11, mouse[1]//width-3
		
		win = True
		for i in range(9):
			for j in range(9):
				if s_grid[i][j] != Grid[i][j]: win = False; break
		if win: return True
		
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT: Menu()
			
			if Delete.click(event): active = "✖"
			elif One.click(event): active = 1
			elif Two.click(event): active = 2
			elif Three.click(event): active = 3
			elif Four.click(event): active = 4
			elif Five.click(event): active = 5
			elif Six.click(event): active = 6
			elif Seven.click(event): active = 7
			elif Eight.click(event): active = 8
			elif Nine.click(event): active = 9
			elif Reverse.click(event):
				try: 
					revert = actions[-1]
					Grid[revert[0]][revert[1]] = revert[2]
					del actions[-1]
				except IndexError: continue
			
			if mx >= 0 and mx <= 8 and my >= 0 and my <= 8:
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if Grid[mx][my] == 0 and active is not None and active != "✖":
						p = Grid[mx][my]
						Grid[mx][my] = active
						actions.append([mx, my, p])
					elif m_grid[mx][my] == 0 and active == "✖":
						p = Grid[mx][my]
						Grid[mx][my] = 0
						actions.append([mx, my, p])
				
		screen.fill(white)
		
		for i in range(9):
			for j in range(9):
				if active == "✖" and Grid[i][j] != m_grid[i][j]:
					pygame.draw.rect(screen, (253, 171, 159), [(width*11.5)+i*width, (width*3)+j*width, width, width])
				elif Grid[i][j] == active:
					pygame.draw.rect(screen, (210, 210, 210), [(width*11.5)+i*width, (width*3)+j*width, width, width])
		
		if mx >= 0 and mx <= 8 and my >= 0 and my <= 8 and Grid[mx][my] == 0 and active is not None and active != "✖":
			centerprint(active, (width*11.5)+mx*width, (width*3)+my*width, width+1, width+1, (125, 125, 125))
		if active == "✖":
			if mx >= 0 and mx <= 8 and my >= 0 and my <= 8 and m_grid[mx][my] == 0 and Grid[mx][my] != 0:
				pygame.draw.rect(screen, (253, 112, 104), [(width*11.5)+mx*width, (width*3)+my*width, width, width])
		
		ShowSudoku(Grid)
		
		seconds = round(int(time.time() - startTime))
		if seconds > 59:
			minutes += 1
			startTime = time.time()
			pygame.time.delay(50)
		centerprint("{}:{}".format("{:02d}".format(minutes), "{:02d}".format(seconds)), 575, 40, 130, 40, (96, 56, 19))
		
		Delete.show(mouse, active), Reverse.show(mouse, active)
		One.show(mouse, active), Two.show(mouse, active), Three.show(mouse, active)
		Four.show(mouse, active), Five.show(mouse, active), Six.show(mouse, active)
		Seven.show(mouse, active), Eight.show(mouse, active), Nine.show(mouse, active)	
		
		pygame.display.update()
		clock.tick(30)


def Menu():
	Easy = ButtonBox("Fácil", 370, 400, 160, 40)
	Medium = ButtonBox("Médio", 560, 400, 160, 40)
	Hard = ButtonBox("Difícil", 750, 400, 160, 40)
	
	while True:
		mouse = pygame.mouse.get_pos()
		
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT: quit()
			
			if Easy.click(event): Sudoku(1)
			if Medium.click(event): Sudoku(3)
			if Hard.click(event): Sudoku(5)
		
		screen.fill(white)
		centerprint("Sudoku", 340, 100, 600, 100, font = fontUI81)
		
		Easy.show(mouse), Medium.show(mouse), Hard.show(mouse)
		
		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__": Menu()
