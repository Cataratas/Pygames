Collection of games made with pygame.

To compile each game use:
- Snake:
> pyinstaller --onefile --add-data="./Fonts/berlin-sans-fb-demi-bold.ttf";"./Fonts/" --add-data="./Layout/Snake Head.png";"./Layout/" --add-data="./Layout/Snake Body.png";"./Layout/" --add-data="./Layout/Snake Food.png";"./Layout/" Snake.pyw
- TicTacToe:
> pyinstaller --onefile --add-data="./Fonts/berlin-sans-fb-demi-bold.ttf";"./Fonts/" --add-data="./Layout/X.png";"./Layout/" --add-data="./Layout/O.png";"./Layout/" --add-data="./Layout/BlackCircle.png";"./Layout/" --add-data="./Layout/RedCircle.png";"./Layout/" --add-data="./Layout/BlueCircle.png";"./Layout/" --add-data="./Layout/Tile.png";"./Layout/" --add-data="./Layout/Tile 2.png";"./Layout/" --add-data="./Layout/Tile 2Red.png";"./Layout/" --add-data="./Layout/Tile 2Blue.png";"./Layout/" --add-data="./Layout/Gray.png";"./Layout/" --add-data="./Layout/Gray Red.png";"./Layout/" --add-data="./Layout/Gray Blue.png";"./Layout/" --add-data="./Layout/Long Gray.png";"./Layout/" --add-data="./Layout/Long Gray Blue.png";"./Layout/" --add-data="./Layout/Long Gray Red.png";"./Layout/" TicTacToe.pyw
- Maze:
> pyinstaller --onefile --add-data="./Layout/Player.png";"./Layout/" --add-data="./Layout/Key 0.png";"./Layout/" --add-data="./Layout/Key.png";"./Layout/" --add-data="./Layout/Door 0.png";"./Layout/" --add-data="./Layout/Door.png";"./Layout/" Maze.pyw
- Hangman:
> pyinstaller --onefile --add-data="./Fonts/berlin-sans-fb-demi-bold.ttf";"./Fonts/" --add-data="./Fonts/myriad-pro-8.otf";"./Fonts/" --add-data="./Layout/Blanks.png";"./Layout/" --add-data="./Layout/Post.png";"./Layout/" --add-data="./Layout/Head.png";"./Layout" --add-data="./Layout/Body.png";"./Layout" --add-data="./Layout/Arm.png";"./Layout" --add-data="./Layout/Leg.png";"./Layout" --add-data="./Layout/Face.png";"./Layout" --add-data="./Layout/Gray.png";"./Layout" --add-data="./Layout/Gray 2.png";"./Layout" Hangman.pyw
- Memory:
> pyinstaller --onefile --add-data="./Fonts/seguiemj.ttf";"./Fonts/" Memory.pyw
- Minesweeper:
> pyinstaller --onefile --add-data="./Fonts/seguisym.ttf";"./Fonts/" --add-data="./Fonts/berlin-sans-fb-demi-bold.ttf";"./Fonts/" Minesweeper.pyw
- Pong:
> pyinstaller --onefile --add-data="./Fonts/BIG JOHN.otf";"./Fonts/" Pong.pyw
- Sudoku:
> pyinstaller --onefile --add-data="./Fonts/seguisym.ttf";"./Fonts/" Sudoku.pyw