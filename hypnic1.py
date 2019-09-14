import os
from pathlib import Path
from PIL import Image
import math
import random


# Global Constants
# Path to the image used as program input
INPUT_IMG = "input.jpg"
# Path at which the resulting image will be saved
OUTPUT_IMG = "output/output"
OUTPUT_IMG_EXTENSION = ".jpg"
# Whether or not to generate a new image each time the render() function for a Container object is called
MULTIPLE_RENDERS = True
# Whether or not to generate an additional animated .gif from all rendered images
ANIMATE = True


"""
_________________________________________________
TODO
_________________________________________________
 - Add ability to generate animated GIFs when more than one output images is
   created throughout the function application process
 - Implement ability to perform operations based on neighboring pixels
"""


class Container:

    def __init__(self):
        # The image to modify
        self.imageIn = Image.open(INPUT_IMG)
        # A copy of the input image to which the functions are applied
        self.imageOut = Image.open(INPUT_IMG)
        # The X resolution of self.imageIn
        self.xRes = self.imageIn.size[0]
        # The Y resolution of self.imageIn
        self.yRes = self.imageIn.size[1]
        # The X value of the current pixel being edited
        self.currentX = 0
        # The Y value of the current pixel being edited
        self.currentY = 0
        # Suffix to apply to the filename of the current version of self.imageOut upon running self.render()
        self.currentFrame = 0
        # An array of pixels representing the input image. Used for reference but never modified.
        self.pixelsIn = self.imageIn.load()
        # An array of pixels representing the output image. Initialized identical to self.pixelsIn
        #     Modified over time while iterating through rows/columns. Should not be used for reference.
        self.pixelsOut = self.imageOut.load()
        # Internal variable used to track error incidences during debugging
        self.errorCount = 0

    # Converts an RGB color value to an HSV color value
    # Based on algorithm (with modified domain) from:
    #     http://coecsl.ece.illinois.edu/ge423/spring05/group8/finalproject/hsv_writeup.pdf
    # R, G, and B are integers from 0 to 255 inclusive
    # H, S, and V are each measured on a continuous scale
    # H, conceptually, is measured in degrees and ranges from 0 <= H < 360
    # S is measured from 0 to 1 inclusive
    #   The lower S is, the more gray is present, causing it to appear faded
    # V is measured from 0 to 1 inclusive
    #   V represents brightness, where 0 is fully dark and 1 is fully bright
    #   If V is 0, then the color is always black, regardless of H or S
    @staticmethod
    def fromRGBtoHSV(rgb):
        minRGB = float(min(rgb))
        maxRGB = float(max(rgb))
        deltaRGB = maxRGB - minRGB
        h = 0
        s = 0
        v = maxRGB / 255
        # r == g == b == 0
        if maxRGB == 0:
            return (h, s, v)
        else:
            s = deltaRGB / maxRGB
        # Hue is null
        if deltaRGB == 0:
            return (h, s, v)
        # Hue is non-null
        else:
            # Hue is between yellow and magenta
            if rgb[0] == maxRGB:
                h = round(60 * ((rgb[1] - rgb[2]) / (deltaRGB)))
            # Hue is between cyan and yellow
            elif rgb[1] == maxRGB:
                h = round(60 * (2 + ((rgb[2] - rgb[0]) / (deltaRGB))))
            # Hue is between magenta and cyan
            else:
                h = round(60 * (4 + ((rgb[0] - rgb[1]) / (deltaRGB))))
            # Ensure that Hue is in the 0 <= H < 360 range
            h %= 360
        return (h, s, v)

    # Converts an HSV color value to an RGB color value
    # Based on algorithm (with modified domain) from:
    #     https://www.rapidtables.com/convert/color/hsv-to-rgb.html
    # R, G, and B are integers from 0 to 255 inclusive
    # H, S, and V are each measured on a continuous scale
    # H is measured in degrees on the domain of 0 <= H < 360
    # S and V range from 0 to 1 inclusive
    @staticmethod
    def fromHSVtoRGB(hsv):
        c = hsv[1] * hsv[2]
        x = c * (1 - abs((hsv[0] / 60.0) % 2 - 1))
        m = hsv[2] - c
        if hsv[0] < 180:
            if hsv[0] < 120:
                # 0 <= H < 60
                if hsv[0] < 60:
                    rgb = [c, x, 0]
                # 60 <= H < 120
                else:
                    rgb = [x, c, 0]
            # 120 <= H < 180
            else:
                rgb = [0, c, x]
        else:
            # 180 <= H < 240
            if hsv[0] < 240:
                rgb = [0, x, c]
            else:
                # 240 <= H < 300
                if hsv[0] < 300:
                    rgb = [x, 0, c]
                # 300 <= H < 360
                else:
                    rgb = [c, 0, x]
        rgb[0] = int(round(255 * (rgb[0] + m)))
        rgb[1] = int(round(255 * (rgb[1] + m)))
        rgb[2] = int(round(255 * (rgb[2] + m)))
        return tuple(rgb)

    # Returns the nearest integer to the distance between two X/Y coordinate pairs
    @staticmethod
    def calcDist(x1, y1, x2, y2):
        return round(math.sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2))

    # Defines an algebraic function on the cartesian plane
    # Takes an X value as input and returns the Y value at X on that algebraic function
    # NOTE: Currently returns an error if slope is too negative or y intercept is too low
    #       NEED TO INVESTIGATE WHY THIS HAPPENS
    @staticmethod
    def calcCartesianFunc(xIn):
        yOut = round(xIn * -0.01 + 2000)
        return yOut

    # Swaps the Saturation and Value values for a pixel
    def modFlipSV(self, rgbIn):
        hsvIn = self.fromRGBtoHSV(rgbIn)
        hsvOut = (hsvIn[0], hsvIn[2], hsvIn[1])
        rgbOut = self.fromHSVtoRGB(hsvOut)
        return rgbOut

    # Shifts the Hue value by a given number of degrees
    def modHueShift(self, rgbIn, hueShift):
        hsvIn = self.fromRGBtoHSV(rgbIn)
        hsvOut = ((hsvIn[0] + hueShift) % 360, hsvIn[1], hsvIn[2])
        rgbOut = self.fromHSVtoRGB(hsvOut)
        return rgbOut

    # Rotates the R/G/B values of a pixel by 1
    @staticmethod
    def modRotate1RGB(rgbIn):
        rgbOut = (rgbIn[1], rgbIn[2], rgbIn[0])
        return rgbOut

    # Rotates the R/G/B values of a pixel by 2
    @staticmethod
    def modRotate2RGB(rgbIn):
        rgbOut = (rgbIn[2], rgbIn[0], rgbIn[1])
        return rgbOut

    # Swaps the R and B values of a pixel
    @staticmethod
    def modFlipRGB(rgbIn):
        rgbOut = (rgbIn[2], rgbIn[1], rgbIn[0])
        return rgbOut

    # Swaps the G and B values of a pixel
    @staticmethod
    def modFlipRotate1RGB(rgbIn):
        rgbOut = (rgbIn[0], rgbIn[2], rgbIn[1])
        return rgbOut

    # Swaps the R and G values of a pixel
    @staticmethod
    def modFlipRotate2RGB(rgbIn):
        rgbOut = (rgbIn[1], rgbIn[0], rgbIn[2])
        return rgbOut

    # Test function to edit the RGB values of a pixel based on a defined algebraic function
    def modDistFromCartesianFunc(self, rgbIn):
        maxDist = self.calcDist(0, 0, self.xRes, self.yRes)
        cartesianDist = self.calcDist(self.currentX,
                                         self.currentY,
                                         self.currentX,
                                         self.calcCartesianFunc(self.currentX))
        distRatio = (cartesianDist / maxDist)
        rgbOut = ((round(rgbIn[0] * distRatio)) % 255,
                  (round(rgbIn[1] * distRatio)) % 255,
                  (round(rgbIn[2] * distRatio)) % 255)
        return rgbOut

    # Another est function to edit the RGB values of a pixel based on a defined algebraic function
    def modDistFromCartesianFunc2(self, rgbIn):
        maxDist = self.calcDist(0, 0, self.xRes, self.yRes)
        cartesianDist = self.calcDist(self.currentX,
                                         self.currentY,
                                         self.currentX,
                                         self.calcCartesianFunc(self.currentX))
        distRatio = (cartesianDist / maxDist)
        rgbOut = (((((round(rgbIn[0] * distRatio)) * 0.1) % 255) + rgbIn[0]) % 255,
                  ((((round(rgbIn[1] * distRatio)) * 0.1) % 255) + rgbIn[1]) % 255,
                  ((((round(rgbIn[2] * distRatio)) * 0.1) % 255) + rgbIn[2]) % 255)
        return rgbOut

    # Allows a R, G, or B value to be shifted using an algebraic function, if it falls below a lower bound or above an
    #     upper bound. Magnitude of shift is calculated based on a linear equation. Separate slope and Y-intercept
    #     values are used depending on whether the input R/G/B value falls below or above a specified bound
    @staticmethod
    def calcColorFromCustomDomain(valIn, lowerBound, upperBound, yIntBelow, slopeBelow, yIntAbove, slopeAbove):
        colorOut = valIn
        if valIn <= lowerBound:
            dist = colorOut - lowerBound
            colorOut += slopeBelow * dist + yIntBelow
        elif valIn >= upperBound:
            dist = upperBound - colorOut
            colorOut += slopeAbove * dist + yIntAbove
        colorOut %= 255
        return colorOut

    # Determines the new R/G/B value of a pixel based on X/Y coordinate and existing R/G/B value
    # Currently the only purpose is to call the desired modification function(s)
    def rgbFunc(self):
        rgbResult = self.pixelsIn[self.currentX, self.currentY]
        rgbResult = self.modHueShift(rgbResult, ((self.currentX + 1) % (self.currentY + 1)) % 360)
        rgbResult = self.modHueShift(rgbResult, (self.currentY + 1) % 90)
        rgbResult = self.modHueShift(rgbResult, self.currentY)
        return rgbResult

    def manipulate(self):
        for y in range(self.yRes):
            frameRendered = False
            for x in range(self.xRes):
                self.currentX = x
                self.currentY = y
                self.pixelsOut[self.currentX, self.currentY] = self.rgbFunc()
                if (y % 5 == 0) and (frameRendered == False):
                    print(y)
                    self.render()
                    frameRendered = True
        return 0

    # Saves an output image with filename based on the current frame number
    def render(self):
        if MULTIPLE_RENDERS:
            self.currentFrame += 1
        self.imageOut.save(Path(OUTPUT_IMG + "_" + str(self.currentFrame) + OUTPUT_IMG_EXTENSION))
        print("Frame " + str(self.currentFrame) + " rendered.")
        return 0

    # Creates an animated .gif with a separate frame for each rendered image
    def animate(self):
        return 0

    # Ensures that the directory specified for the output image(s) exists to avoid errors in self.render()
    @staticmethod
    def prepareDirectory():
        directory = os.path.dirname(OUTPUT_IMG)
        os.makedirs(directory, exist_ok=True)
        return 0

def main():
    random.seed(1)
    cont = Container()
    cont.prepareDirectory()
    cont.manipulate()
    if ANIMATE:
        cont.animate()
    print("\n================ C O M P L E T E D ================\n")


main()
