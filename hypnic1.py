from PIL import Image
import math
import random

# Global Constants

# Path to the image used as program input
INPUT_IMG = "input.jpg"

# Path at which the resulting image will be saved
OUTPUT_IMG = "output.jpg"

# Number of times to run the image manipulation function
# Must be an integer greater than or equal to 1
NUM_ITERATIONS = 1


"""
_________________________________________________
TODO
_________________________________________________
 - FIX RGB->HSV and/or HSV->RGB conversions
     - I believe the problem lies specifically with HSV->RGB
     - in SOME cases, converting to HSV and back leads to G being lost and set to be equal to the value of B instead
         - CONFIRMED in the following cases:
             - whenever R == 0 and G < B
         - CHECK the following cases:
             - whenever 0 < R < 255 and G < B
             - whenever R == 255 and G < B
             - whenever 0 < R < 255 and B < G
             - whenever R == 255 and B < G
     = Should write a "flagging" function and look ata outputs to determine other potential problems
     
 - Implement NUM_ITERATIONS variable (should be trivial)
 - Implement ability to perform operations based on neighboring pixels
"""


class Container:

    def __init__(self):
        self.currentX = 0
        self.currentY = 0
        self.imageIn = Image.open(INPUT_IMG)
        self.imageOut = Image.open(INPUT_IMG)
        self.xRes = self.imageIn.size[0]
        self.yRes = self.imageIn.size[1]
        # An array of pixels representing the input image. Used for reference but never modified.
        self.pixelsIn = self.imageIn.load()
        # An array of pixels representing the output image. Initialized identical to self.pixelsIn
        # Modified over time while iterating through rows/columns. Should not be used for reference.
        self.pixelsOut = self.imageOut.load()

    # Converts an RGB color value to an HSV color value
    # Based on algorithm (with modified domain) from:
    #     http://coecsl.ece.illinois.edu/ge423/spring05/group8/finalproject/hsv_writeup.pdf
    # R, G, and B are integers from 0 to 255 inclusive
    # H, conceptually, is measured in degrees and ranges from 0 <= H < 360
    #   This program limits H to integers from 0 to 359 inclusive
    #   An H of 0 represents pure red
    # S is measured from 0 to 255 inclusive
    #   The lower S is, the more gray is present, causing it to appear faded
    # V is measured from 0 to 255 inclusive
    #   V represents brightness, where 0 is fully dark and 255 is fully bright
    #   If V is 0, then the color is always black, regardless of H or S
    @staticmethod
    def fromRGBtoHSV(rgb):
        minRGB = min(rgb)
        maxRGB = max(rgb)
        deltaRGB = maxRGB - minRGB
        h = 0
        s = 0
        v = maxRGB
        # r == g == b == 0
        if maxRGB == 0:
            return (h, s, v)
        else:
            s = round(255 * (deltaRGB / maxRGB))
        # Hue is null
        if deltaRGB == 0:
            return (h, s, v)
        # Hue is non-null
        else:
            # Hue is between yellow and magenta
            if rgb[0] == maxRGB:
                h = round(60 * ((rgb[1] - rgb[2]) / deltaRGB))
            # Hue is between cyan and yellow
            elif rgb[1] == maxRGB:
                h = round(60 * (2 + ((rgb[2] - rgb[0]) / deltaRGB)))
            # Hue is between magenta and cyan
            else:
                h = round(60 * (4 + ((rgb[0] - rgb[2]) / deltaRGB)))
            # Ensure that Hue is in the 0 <= H <= 359 range
            if h < 0:
                h += 360
        return (h, s, v)

    # Converts an HSV color value to an RGB color value
    # Based on algorithm (with modified domain) from:
    #     https://www.rapidtables.com/convert/color/hsv-to-rgb.html
    # H is an integer from 0 to 359 inclusive
    # S and V are integers from 0 to 255 inclusive
    # R, G, and B are integers from 0 to 255 inclusive
    @staticmethod
    def fromHSVtoRGB(hsv):
        c = (hsv[1] * hsv[2]) / (255.0 * 255.0)
        x = c * (1 - abs((hsv[0] / 60.0) % 2 - 1))
        m = (hsv[2] / 255.0) - c

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

        rgb[0] = math.floor(255 * (rgb[0] + m))
        rgb[1] = math.floor(255 * (rgb[1] + m))
        rgb[2] = math.floor(255 * (rgb[2] + m))
        return tuple(rgb)

    # Returns the nearest integer to the distance between two X/Y coordinate pairs
    @staticmethod
    def getDist(x1, y1, x2, y2):
        return round(math.sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2))

    # Defines an algebraic function on the cartesian plane
    # Takes an X value as input and returns a Y value
    # NOTE: Currently returns an error if slope is too negative or y intercept is too low
    #       NEED TO INVESTIGATE WHY THIS HAPPENS
    def cartesianFunc(self, xIn):
        yOut = round(xIn * -0.01 + 2000)
        return yOut

    def modRotate1RGB(self, rgbIn):
        rgbOut = (rgbIn[1],
                  rgbIn[2],
                  rgbIn[0])
        return rgbOut

    def modRotate2RGB(self, rgbIn):
        rgbOut = (rgbIn[2],
                  rgbIn[0],
                  rgbIn[1])
        return rgbOut

    def modFlipRGB(self, rgbIn):
        rgbOut = (rgbIn[2],
                  rgbIn[1],
                  rgbIn[0])
        return rgbOut

    def modFlipRotate1RGB(self, rgbIn):
        rgbOut = (rgbIn[0],
                  rgbIn[2],
                  rgbIn[1])
        return rgbOut

    def modFlipRotate2RGB(self, rgbIn):
        rgbOut = (rgbIn[1],
                  rgbIn[0],
                  rgbIn[2])
        return rgbOut

    def modDistFromCartesianFunc(self, rgbIn):
        maxDist = self.getDist(0, 0, self.xRes, self.yRes)
        cartesianFuncDist = self.getDist(self.currentX,
                                         self.currentY,
                                         self.currentX,
                                         self.cartesianFunc(self.currentX))
        distRatio = (cartesianFuncDist / maxDist)
        rgbOut = ((round(rgbIn[0] * distRatio)) % 255,
                  (round(rgbIn[1] * distRatio)) % 255,
                  (round(rgbIn[2] * distRatio)) % 255)
        return rgbOut

    def modDistFromCartesianFunc2(self, rgbIn):
        maxDist = self.getDist(0, 0, self.xRes, self.yRes)
        cartesianFuncDist = self.getDist(self.currentX,
                                         self.currentY,
                                         self.currentX,
                                         self.cartesianFunc(self.currentX))
        distRatio = (cartesianFuncDist / maxDist)
        rgbOut = (((((round(rgbIn[0] * distRatio)) * 0.1) % 255) + rgbIn[0]) % 255,
                  ((((round(rgbIn[1] * distRatio)) * 0.1) % 255) + rgbIn[1]) % 255,
                  ((((round(rgbIn[2] * distRatio)) * 0.1) % 255) + rgbIn[2]) % 255)
        return rgbOut

    # REWRITE THIS FUNCTION TO BE SIGNIFICANTLY MORE COMPACT
    # AND/OR SPLIT IT INTO 3 SEPARATE FUNCTIONS: 1 for R, 1 for G, 1 for B
    def modCustomDomainRGB(self, rgbIn):
            redOut = rgbIn[0]
            greenOut = rgbIn[1]
            blueOut = rgbIn[2]

            modRed = True
            lowerBoundRed = 120
            upperBoundRed = 136
            belowValueRed = 0
            aboveValueRed = 255
            modGreen = False
            lowerBoundGreen = 120
            upperBoundGreen = 136
            belowValueGreen = 0
            aboveValueGreen = 255
            modBlue = False
            lowerBoundBlue = 120
            upperBoundBlue = 136
            belowValueBlue = 0
            aboveValueBlue = 255

            if modRed:
                if redOut < lowerBoundRed:
                    redOut = belowValueRed
                elif redOut > upperBoundRed:
                    redOut = aboveValueRed
            if modGreen:
                if greenOut < lowerBoundGreen:
                    greenOut = belowValueGreen
                elif greenOut > upperBoundGreen:
                    greenOut = aboveValueGreen
            if modBlue:
                if blueOut < lowerBoundBlue:
                    blueOut = belowValueBlue
                elif blueOut > upperBoundBlue:
                    blueOut = aboveValueBlue
            return (redOut, greenOut, blueOut)

    # Determines the new R/G/B value of a pixel based on X/Y coordinate and existing R/G/B value
    # Currently the only purpose is to call the desired modification function
    def rgbFunc(self):
        rgbResult = self.pixelsIn[self.currentX, self.currentY]

        rgbResult = self.modCustomDomainRGB(rgbResult)
        rgbResult = self.modFlipRotate1RGB(rgbResult)
        print(rgbResult)
        print(self.fromRGBtoHSV(rgbResult))
        print(self.fromHSVtoRGB(self.fromRGBtoHSV(rgbResult)))
        print()
        return rgbResult

    # Encodes a list of integers into R/G/B pixel data of a given .png file
    def manipulate(self):
        for y in range(self.yRes):
            for x in range(self.xRes):
                self.currentX = x
                self.currentY = y

                self.pixelsOut[x, y] = self.rgbFunc()

        self.imageOut.save(OUTPUT_IMG)


def main():
    random.seed(1)
    cont = Container()
    cont.manipulate()
    print("\n\n\n================ C O M P L E T E D ================\n")


main()
