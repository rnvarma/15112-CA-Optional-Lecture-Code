# deltaGraphicsExample.py
# Made by Anthony Kuntz
# Adapted from course notes for CMU 15-112
"""
##########################
PLEASE READ THE FOLLOWING:
##########################

During lecture I joked about how MVC violations, such as passing canvas
to our event functions, are frowned upon greatly by the course leadership.
These statements were, in part, exaggerated, but mostly true.

It is important to understand when violating MVC is okay:
  - Never during a homework assignment.
  - Only when using delta graphics for a project (TP or your own personal thing).

This latter is allowed since delta graphics inherently requires a violation of MVC.

Next, recall that delta graphics is not a module, program, or library.
Instead, it is just a different way of managing animations.

Finally, remember that the code below demonstrates a few of the
neat things that Delta Graphics can do, but by no means represents
its limit. Please play around with the concept to see what you can do.
Classes are optional, but make your code and your life much simpler.
"""

from Tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.anthony = Player(100,100,"dog.gif",data.canvas)
    # Make an instance of a class, just for fun!

    data.circleCoords = (0,0,50,50)
    # Remember to accurately record any object's coordinates!
    # This can also be done inside a class

    data.myCircle = data.canvas.create_oval(data.circleCoords,fill="red")
    # Get a handle on the circle
    
    data.keys = []
    data.timerDelay = 10
    # 10 is very fast. Less than 10 is unnecessary

    data.lift = True # This was to demonstrate a silly example

def mousePressed(event, data):
    data.anthony.kill(data.canvas)
    # This method calls canvas.delete
    # this could have been done as follows:
    # data.canvas.delete(data.anthony.image)

def mouseMoved(event, data):
    data.anthony.moveTo(event.x, event.y, data.canvas)

def keyPressed(event, data):
    if event.keysym not in data.keys:
        data.keys.append(event.keysym)
        # manage data.keys for multi-directional movement

def keyReleased(event, data):
    if event.keysym in data.keys:
        data.keys.remove(event.keysym)

def timerFired(data):
    data.lift = not data.lift
    # Change the flag every time for a silly example
    if data.lift:
        data.anthony.liftPlayer(data.canvas)
    else:
        data.anthony.lowerPlayer(data.canvas)
    # An example of calling a method to cause a canvas function
    # like lift or lower to occur.

    if "Up" in data.keys:
        data.anthony.moveDelta(0,-1,data.canvas)
    if "Down" in data.keys:
        data.anthony.moveDelta(0,+1,data.canvas)
    if "Right" in data.keys:
        data.anthony.moveDelta(1,0,data.canvas)
    if "Left" in data.keys:
        data.anthony.moveDelta(-1,0,data.canvas)
    # Calling methods which in turn call canvas.coords

class Player(object):
# Example class (optional)

    def __init__(self, x, y, filename, canvas):
        self.x = x
        self.y = y
        self.picture = PhotoImage(file = filename)
        self.image = canvas.create_image(x, y, image = self.picture)
        # Get a handle for the Player's image

    def moveDelta(self, dx, dy, canvas):
        self.x += dx
        self.y += dy
        canvas.coords( self.image, self.x, self.y )
        # Coords takes in: the handle of the drawing you wish to move
        #                  and the new coordinates (either 2 or 4)

    def moveTo(self, x, y, canvas):
        self.x = x
        self.y = y
        canvas.coords( self.image, self.x, self.y )

    def liftPlayer(self, canvas):
        canvas.lift(self.image)
        # lift can be called on the handle to any canvas drawing

    def lowerPlayer(self, canvas):
        canvas.lower(self.image)
        # lower can be called on the handle to any canvas drawing

    def kill(self, canvas):
        canvas.delete(self.image)
        # Delete can be called on the handle to any canvas drawing


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
   
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        # Removed the call to redrawAll

    def mouseMovedWrapper(event, canvas, data):
        mouseMoved(event, data)
        # Removed the call to redrawAll

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        # Removed the call to redrawAll

    def keyReleasedWrapper(event, canvas, data):
        keyReleased(event, data)
        # Removed the call to redrawAll

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        # Removed the call to redrawAll
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    data.canvas = canvas # Save canvas in data so any fn can access it

    init(data) # Make sure to call init AFTER data.canvas

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
                            mouseMovedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<KeyRelease>", lambda event:
                            keyReleasedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)