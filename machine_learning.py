#Digit Recognition Demo
#15-112 Optional Lecture
#Edward Dryer

class DrawingGrid(object):
    def __init__(self,rows,cols,data):
        self.grid = []
        self.rows = rows
        self.cols = cols
        self.rWidth = data.width / self.cols
        self.rHeight = data.height / self.rows
        self.clearBoard()

    def clearBoard(self):
        self.grid = []
        for row in range(self.rows):
            c = []
            for col in range(self.cols):
                c.append(1)
            self.grid.append(c)

    def draw(self,canvas,data):
        for row in range(self.rows):
            for col in range(self.cols):
                x = 1  + col * self.rWidth
                y = 1 + row * self.rHeight
                fill = "black" if self.grid[row][col] == 0  else "white"
                canvas.create_rectangle(x,y,x+self.rWidth,y +self.rHeight,fill=fill)

from tkinter import *
from sklearn import *
import numpy as np

####################################
# customize these functions
####################################

def init(data):
    print("r to reset")
    print("c to classify screen")
    print("1 to label as 1")
    print("2 to label as 2")
    print("t to train")
    data.drawingGrid = DrawingGrid(10,10,data)
    data.savedBoards = []
    data.savedLabels = []
    data.X = []
    data.Y = []
    data.pca = decomposition.PCA(2)
    data.classifier = linear_model.Perceptron()
    data.one = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1]]
    data.two = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 0, 0, 0, 1, 1], [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 0, 0, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
 


def mouseDragged(event, data):
    row = int(event.y // data.drawingGrid.rHeight)
    col = int(event.x // data.drawingGrid.rWidth)
    if (row < data.drawingGrid.rows and col < data.drawingGrid.cols):
        if (row >= 0 and col >= 0):
            data.drawingGrid.grid[row][col] = 0

def flattenBoard(b):
    flatBoard = []
    for l in b:
        flatBoard += l
    return flatBoard

def classify(data):
    flatBoard = flattenBoard(data.drawingGrid.grid)
    flatBoard = data.pca.transform([flatBoard])
    if (data.classifier.predict(flatBoard) == ["1"]):
        data.drawingGrid.grid = data.one
    else:
        data.drawingGrid.grid = data.two


def save(data,digit):
    flatBoard = flattenBoard(data.drawingGrid.grid)
    data.savedBoards.append(flatBoard)
    data.savedLabels.append(digit)
    print(data.drawingGrid.grid)

def train(data):
    data.savedBoards = np.array(data.savedBoards)
    data.savedLabels = np.array(data.savedLabels)
    data.pca.fit(data.savedBoards)
    data.X = data.pca.transform(data.savedBoards)
    data.Y = data.savedLabels
    data.classifier.fit(data.X,data.Y)

def keyPressed(event, data):
    if (event.char == "c"):
        print("classified:")
        classify(data)
    if (event.char == "1"):
        print("saving as 1")
        save(data,"1")
    if (event.char == "2"):
        print("saving as 2")
        save(data,"2")
    if (event.char == "t"):
        print("training")
        train(data)
    if (event.char == "r"):
        print("clearing")
        data.drawingGrid.clearBoard()


def timerFired(data):
    pass

def redrawAll(canvas, data):
    data.drawingGrid.draw(canvas,data)
    # draw in canvas
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mouseDraggedWrapper(event, canvas, data):
        mouseDragged(event, data)
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
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    # root.bind("<Button-1>", lambda event:
    #                         mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    #added this
    root.bind("<B1-Motion>",lambda event:
                            mouseDraggedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500,500)