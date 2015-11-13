# Anthony Kuntz, 11/12/2015
# For use in 15-112
#
# Adapted from code originally written by Tim Brooks

from tkinter import Tk, PhotoImage
import os

# from 112 course website
def hexColor(red, green, blue):
    return ("#%02x%02x%02x" % (red, green, blue))

class Image(object):

    def __init__(self, name):
        filepath = "images" + os.sep + name + ".gif"
        self.image = PhotoImage(file = filepath)
        self.copy  = PhotoImage(file = filepath)

    def applyImageFilter(self, newFilename, filterFunction):
        image = self.image # Go through each pixel in the original
        for row in range(image.height()):
            for col in range(image.width()):
                (red, green, blue) = self.getRGB(col, row) # getRGB takes x and then y

                (newRed, newGreen, newBlue) = filterFunction(col, row, red, green, blue)

                self.setRGB(col, row, newRed, newGreen, newBlue)

        self.saveCopyToFolder(newFilename)

    def saveCopyToFolder(self, newFilename):
        filename = "output" + os.sep + newFilename + ".gif"
        self.copy.write(filename, format="gif")


    def getRGB(self, x, y):
        image = self.image
        value = image.get(x, y)
        return value

    def setRGB(self, x, y, red, green, blue):
        image = self.copy
        color = hexColor(red, green, blue)
        image.put(color, to=(x,y))

    def greyScaleFilter(self, x, y, red, green, blue):
        grey = ( red + green + blue ) // 3
        return (grey, grey, grey)

    def sephiaFilter(self, x, y, red, green, blue):
        sred = 236
        sgreen = 207
        sblue = 113
        newRed = (2*sred + red) // 3
        newGreen = (2*sgreen + green) // 3
        newBlue = (2*sblue + blue) // 3
        return (newRed, newGreen, newBlue)

    def invertFilter(self, x, y, red, green, blue):
        return (255-red, 255-green, 255-blue)

    def sephia(self, newFilename):
        print("Applying sephia filter...")
        self.applyImageFilter(newFilename, self.sephiaFilter)
        print("Finished!")

    def greyScale(self, newFilename):
        print("Applying grey scale filter...")
        self.applyImageFilter(newFilename, self.greyScaleFilter)
        print("Finished!")

    def invert(self, newFilename):
        print("Applying invert filter...")
        self.applyImageFilter(newFilename, self.invertFilter)
        print("Finished!")

    
def main():
    Tk()
    print("Welcome!")
    loadName = input("What is the name of the file you'd like to manipulate? ")
    myImage = Image(loadName)
    saveName = input("What would you like to save the result as? ")
    filterName = input("What filter would you like to apply? ")
    if (filterName == "greyscale"):
        myImage.greyScale(saveName)
    elif (filterName == "invert"):
        myImage.invert(saveName)
    elif (filterName == "sephia"):
        myImage.sephia(saveName)
    else:
        print("Sorry! I don't recognize that filter name.")
    print("Goodbye!")

main()