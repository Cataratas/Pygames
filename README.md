Collection of games made with pygame.

To compile each game use:
- Snake:
> pyinstaller --onefile --add-data="./Fonts/berlin-sans-fb-demi-bold.ttf";"./Fonts/" --add-data="./Layout/Snake Head.png";"./Layout/" --add-data="./Layout/Snake Body.png";"./Layout/" --add-data="./Layout/Snake Food.png";"./Layout/" Snake.pyw
- TicTacToe:
> pyinstaller --onefile --add-data="./Fonts/berlin-sans-fb-demi-bold.ttf";"./Fonts/" --add-data="./Layout/X.png";"./Layout/" --add-data="./Layout/O.png";"./Layout/" --add-data="./Layout/BlackCircle.png";"./Layout/" --add-data="./Layout/RedCircle.png";"./Layout/" --add-data="./Layout/BlueCircle.png";"./Layout/" --add-data="./Layout/Tile.png";"./Layout/" --add-data="./Layout/Tile 2.png";"./Layout/" --add-data="./Layout/Tile 2Red.png";"./Layout/" --add-data="./Layout/Tile 2Blue.png";"./Layout/" --add-data="./Layout/Gray.png";"./Layout/" --add-data="./Layout/Gray Red.png";"./Layout/" --add-data="./Layout/Gray Blue.png";"./Layout/" --add-data="./Layout/Long Gray.png";"./Layout/" --add-data="./Layout/Long Gray Blue.png";"./Layout/" --add-data="./Layout/Long Gray Red.png";"./Layout/" TicTacToe.pyw