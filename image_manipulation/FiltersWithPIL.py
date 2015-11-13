# Anthony Kuntz, 11/12/2015
# For use in 15-112
#
# Adapted from code originally written by Tim Brooks

from PIL import Image
import os

def hexColor(red, green, blue):
    return ("#%02x%02x%02x" % (red, green, blue))

class ImageStructure(object):

    def __init__(self, name):
        filepath = "images" + os.sep + name + ".jpg"
        self.image = Image.open(filepath)
        self.copy  = Image.open(filepath)
        self.width, self.height = self.image.size
        self.pixels = self.image.load()
        self.copyPixels = self.copy.load()

    def applyImageFilter(self, newFilename, filterFunction):
        image = self.image # Go through each pixel in the original
        for row in range(self.height):
            for col in range(self.width):
                (red, green, blue) = self.getRGB(col, row) # getRGB takes x and then y

                (newRed, newGreen, newBlue) = filterFunction(col, row, red, green, blue)

                self.setRGB(col, row, newRed, newGreen, newBlue)

        self.saveCopyToFolder(newFilename)

    def saveCopyToFolder(self, newFilename):
        filename = "output" + os.sep + newFilename + ".jpg"
        self.copy.save(filename, 'jpeg')

    def getRGB(self, x, y):
        return self.pixels[x, y]

    def setRGB(self, x, y, red, green, blue):
        self.copyPixels[x, y] = (red, green, blue)

    def greyScaleFilter(self, x, y, red, green, blue):
        grey = ( red + green + blue ) // 3
        return (grey, grey, grey)

    def vignetteFilter(self, x, y, red, green, blue):
        cx = self.width / 2
        cy = self.height / 2

        dist = ( (x-cx)**2 + (y-cy)**2)**.5
        constant = .2
        amount = int(dist*constant)

        red = red - amount if red >= amount else 0
        green = max(green - amount, 0)
        blue = (blue - amount)*(blue >= amount)

        return (red, green, blue)
    

    def greyScale(self, newFilename):
        print("Applying grey scale filter...")
        self.applyImageFilter(newFilename, self.greyScaleFilter)
        print("Finished!")

    def vignette(self, newFilename):
        print("Applying vignette filter...")
        self.applyImageFilter(newFilename, self.vignetteFilter)
        print("Finished!")

    
def main():
    print("Welcome!")
    loadName = input("What is the name of the file you'd like to manipulate? ")
    myImage = ImageStructure(loadName)
    saveName = input("What would you like to save the result as? ")
    filterName = input("What filter would you like to apply? ")
    if (filterName == "greyscale"):
        myImage.greyScale(saveName)
    elif (filterName == "vignette"):
        myImage.vignette(saveName)
    else:
        print("Sorry! I don't recognize that filter name.")
    print("Goodbye!")

main()

# Dead Code Below:
# This was used to make the green screen Kosbie picture.
#
# image1 = ImageStructure("skydiving")
# image2 = ImageStructure("sky")
# for row in range(image1.image.height):
#     for col in range(image1.image.width):
#         (red, green, blue) = image1.getRGB(col, row) # getRGB takes x and then y
#         (red2, green2, blue2) = image2.getRGB(col, row)

#         if (70<red<100 and 150<green and 50<blue<70):
#             (newRed, newGreen, newBlue) = (red2, green2, blue2)
#         else:
#             (newRed, newGreen, newBlue) = (red, green, blue)

#         image2.setRGB(col, row, newRed, newGreen, newBlue)

# image2.saveCopyToFolder("koz")
# print("hellooooo")
