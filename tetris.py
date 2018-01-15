from tkinter import *
import random
import math

def init(data):
    # set board dimensions and margin
    data.rows = 15
    data.cols = 10
    data.margin = 30
    
    # make board
    data.emptyColor = "yellow"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]

    #pieces
    #Seven "standard" pieces (tetrominoes)
    iPiece = [
    [ True,  True,  True,  True]
    ]

    jPiece = [
    [ True, False, False ],
    [ True, True,  True]
    ]

    lPiece = [
    [ False, False, True],
    [ True,  True,  True]
    ]

    oPiece = [
    [ True, True],
    [ True, True]
    ]

    sPiece = [
    [ False, True, True],
    [ True,  True, False ]
    ]

    tPiece = [
    [ False, True, False ],
    [ True,  True, True]
    ]

    zPiece = [
    [ True,  True, False ],
    [ False, True, True]
    ]

    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "salmon", "sea green", "tomato", \
    "yellow green", "slateblue1", "darkturquoise", "maroon" ]

    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors

    data.fallingPiece, data.fallingPieceColor = 0,0
    data.fallingPieceRow, data.fallingPieceCol = 0,0

    data.callFallingPiece = newFallingPiece(data)

    data.fallingPieceWidth= len(data.fallingPiece[0])
    data.fallingPieceHeight= len(data.fallingPiece)

    data.score = 0
    data.gameOver = False #check game over
    data.paused = False #check paused

def newFallingPiece(data):
    tetrisPieces = data.tetrisPieces
    tetrisPieceColors = data.tetrisPieceColors
    randomNo = random.randint(0,len(tetrisPieces)-1) #choosing random piece
    fallingPiece, fallingPieceColor \
    = tetrisPieces[randomNo], tetrisPieceColors[randomNo]
    fallingPieceWidth= len(fallingPiece[0])
    fallingPieceRow = 0
    fallingPieceCol = data.cols//2 - math.ceil(0.5*fallingPieceWidth)

    data.fallingPiece, data.fallingPieceColor = fallingPiece, fallingPieceColor
    data.fallingPieceRow, data.fallingPieceCol \
    = fallingPieceRow, fallingPieceCol
    
    if not fallingPieceIsLegal(data):
        data.gameOver = True

def drawFallingPiece(canvas, data):
    data.fallingPieceHeight = len(data.fallingPiece)
    data.fallingPieceWidth = len(data.fallingPiece[0])
    for row in range(data.fallingPieceHeight):
        for col in range(data.fallingPieceWidth):
            if data.fallingPiece[row][col] == True: #True is where the block is
                drawRow = row + data.fallingPieceRow
                drawCol = col + data.fallingPieceCol
                drawCell(canvas, data, drawRow, drawCol, data.fallingPieceColor)

def moveFallingPiece(data, drow, dcol):
    row = data.fallingPieceRow
    col = data.fallingPieceCol
    
    newRow = data.fallingPieceRow + drow #new row location
    newCol = data.fallingPieceCol + dcol #new col location
    
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow #return to previous row location
        data.fallingPieceCol -= dcol #return to previous col location
        return False

    return True

def rotateFallingPiece(data):
    oldPiece = data.fallingPiece

    oldRows = data.fallingPieceHeight
    oldCols = data.fallingPieceWidth
    
    oldRow = data.fallingPieceRow 
    oldCol = data.fallingPieceCol

    newRows, newCols = oldCols, oldRows

    newPiece = [ ([0] * newCols) for row in range(newRows) ]

    #this rotates the piece anti clockwise
    for testCol in range(newCols):
        for testRow in range(newRows):
            newPiece[testRow][testCol] = oldPiece[testCol][-testRow-1]

    #calculating the center point
    oldCenterRow = oldRow + oldRows//2
    oldCenterCol = oldCol + oldCols//2

    #new center is the same as old center, since we are rotating about center
    newCenterRow = oldCenterRow
    newCenterCol = oldCenterCol

    #calculating new row and new col based on new center
    newRow = newCenterRow - newRows//2
    newCol = newCenterCol - newCols//2
    
    #load local variables into my "bag"
    data.fallingPiece = newPiece
    data.fallingPieceHeight = newRows
    data.fallingPieceWidth = newCols
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol

    #if the rotated piece is not legal, revert back to the unrotated piece
    if not fallingPieceIsLegal(data):
        data.fallingPiece  = oldPiece
        data.fallingPieceHeight = oldRows
        data.fallingPieceWidth = oldCols
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol

def rotateFallingPieceClockwise(data):
    oldPiece = data.fallingPiece

    oldRows = data.fallingPieceHeight
    oldCols = data.fallingPieceWidth
    
    oldRow = data.fallingPieceRow 
    oldCol = data.fallingPieceCol

    newRows, newCols = oldCols, oldRows

    newPiece = [ ([0] * newCols) for row in range(newRows) ]

    #this rotates the piece anti clockwise
    for testCol in range(newCols):
        for testRow in range(newRows):
            newPiece[testRow][testCol] = oldPiece[testCol][testRow]

    #calculating the center point
    oldCenterRow = oldRow + oldRows//2
    oldCenterCol = oldCol + oldCols//2

    #new center is the same as old center, since we are rotating about center
    newCenterRow = oldCenterRow
    newCenterCol = oldCenterCol

    #calculating new row and new col based on new center
    newRow = newCenterRow - newRows//2
    newCol = newCenterCol - newCols//2
    
    #load local variables into my "bag"
    data.fallingPiece = newPiece
    data.fallingPieceHeight = newRows
    data.fallingPieceWidth = newCols
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol

    #if the rotated piece is not legal, revert back to the unrotated piece
    if not fallingPieceIsLegal(data):
        data.fallingPiece  = oldPiece
        data.fallingPieceHeight = oldRows
        data.fallingPieceWidth = oldCols
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol


def fallingPieceIsLegal(data):
    row = data.fallingPieceRow
    col = data.fallingPieceCol
    height = len(data.fallingPiece)
    width = len(data.fallingPiece[0])
    rows = data.rows
    cols = data.cols

    if (row < 0 or row+height > rows) or (col < 0 or col+width > cols):
        #this checks whether the piece is out of the board
        return False

    for checkRow in range(len(data.fallingPiece)):
        for checkCol in range(len(data.fallingPiece[0])):
            if data.fallingPiece[checkRow][checkCol] == True \
            and data.board[row + checkRow][col + checkCol] != data.emptyColor:
            #checks for collision
                return False
    return True

def placeFallingPiece(data):
    data.fallingPieceHeight = len(data.fallingPiece)
    data.fallingPieceWidth = len(data.fallingPiece[0])

    for row in range(data.fallingPieceHeight):
        for col in range(data.fallingPieceWidth):
            if data.fallingPiece[row][col] == True:
                drawRow = row + data.fallingPieceRow
                drawCol = col + data.fallingPieceCol
                data.board[drawRow][drawCol]= data.fallingPieceColor
                #coloring the board the color of the piece
                #basically makeing the piece be IN the board

def removeFullRows(data):
    rows = data.rows
    cols = data.cols
    newList =[]
    count = 0

    for row in range(rows-1,-1,-1): #going from last row to first
        newRow = [] #temp variable
        for col in range(cols):
            newRow += [data.board[row][col]]
        if data.emptyColor in newRow:
            newList.insert(0, newRow)
        else:
            count += 1 #number of rows that are filled and removed
    scoringSystemNumber = 2
    data.score += (count ** scoringSystemNumber) #scoring system
    
    while count > 0:
        newList.insert(0,[data.emptyColor]*cols)
        count -= 1
    
    data.board = newList

# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    
    x0 = data.margin + gridWidth * col / data.cols #left
    x1 = data.margin + gridWidth * (col+1) / data.cols #right
    y0 = data.margin + gridHeight * row / data.rows #top
    y1 = data.margin + gridHeight * (row+1) / data.rows #bottom
    
    return (x0, y0, x1, y1) 

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    # for now, for testing purposes, just choose a new falling piece
    # whenever ANY key is pressed!
    if (event.keysym == "Left"):
        moveFallingPiece(data, 0, -1)
    elif (event.keysym == "Right"):
        moveFallingPiece(data, 0, +1)
    elif (event.keysym == "Down"):
        rotateFallingPieceClockwise(data)
    elif (event.keysym == "Up"):
        rotateFallingPiece(data)
    elif(event.char == "r"):
        init(data) #resets the game
    elif (event.char == "p"):
        data.paused = not data.paused
    elif (event.char == " "):
        moveFallingPiece(data, +1, 0) #moves downward


def timerFired(data):
    if (data.paused or data.gameOver): return 
    #games stops when paused or game over
    if not moveFallingPiece(data,+1,0) and not data.gameOver:
        placeFallingPiece(data)
        newFallingPiece(data)
        removeFullRows(data)

def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)

def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])


def drawCell(canvas, data, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 0 # cell outline margin
    
    canvas.create_rectangle(x0, y0, x1, y1, fill="red")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color, outline="gold")

def drawScore(canvas, data):
    (cx, cy) = (data.width - 2*data.margin, data.margin//2)
    canvas.create_text(cx, cy, text="SCORE: %d" % data.score)

def drawGameOver(canvas, data):
    (cx, cy) = (data.width//2, data.height//2)
    (x0, y0) = (data.margin*2, data.height*1//3)
    (x1, y1) = (data.width - data.margin*2, data.height*2//3)
    canvas.create_rectangle(x0,y0,x1,y1, fill="gold", width=10, outline="orange")
    canvas.create_text(cx, cy, text="GAME OVER")

def redrawAll(canvas, data):
    drawGame(canvas, data)
    drawScore(canvas, data)
    if data.gameOver:
        drawGameOver(canvas, data)
    elif (data.paused):
        canvas.create_text(data.width/2, data.height/2, text="Paused!", \
            fill = "firebrick", 
                           font=("Helvetica", 32, "bold"))
    canvas.create_text(data.width//2, data.height-data.margin//2,\
        text="<p> pauses; <r> resets; <up> rotate anti clockwise; \
        \n <down> rotate clockwise; <space> move down")


####################################
# use the run function as-is
####################################

def run(width=400, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    init(data)
    
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
   
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("thanks for playing!")


####################################
# playTetris() [calls run()]
####################################

def playTetris():
    rows = 15 #number of rows
    cols = 10 #number of columns
    margin = 20 # margin around grid
    cellSize = 30 # width and height of each cell
    width = 2*margin + cols*cellSize #width of window
    height = 2*margin + rows*cellSize #height of window
    run(width, height)

run()

# citation: cs112.github.io