import os
from pathlib import Path
from PIL import Image
import imageio
import cv2
import math
import random


# GLOBAL CONSTANTS
# ________________________________
# GENERAL VARIABLES
# Path to the image used as program input
INPUT_IMG = "input3.jpg"
# Path at which the resulting image will be saved
OUTPUT_IMG = "output/output"
OUTPUT_IMG_EXTENSION = ".jpg"
# Whether or not to generate a new image each time the render() function for a Container object is called
MULTIPLE_RENDERS = True
# How many times to repeat the entire image manipulation process
# When a new round of manipulation begins, the final output image of the last round of manipulation is used as the base
#    image in the new round of manipulation
NUM_ROUNDS_OF_MANIPULATION = 5

# GIF-RELATED VARIABLES
# Whether or not to generate an animated .gif from all rendered images
CREATE_GIF = True
# Path at which the resulting animated .gif will be saved, if CREATE_GIF = True
GIF_PATH = "output/animation2.gif"
# Whether or not to play the .gif frames in reverse when the end is reached, transitioning back to the original source
#    image instead of abruptly jumping right back to the start
REVERSE_GIF_AT_END = True
# Number of times to repeat each rendered image during forward .gif progression
# Effectively lengthens the time for which each frame is visible in the animated .gif
GIF_FRAMES_PER_IMAGE_FORWARD = 3
# Number of times to repeat each rendered image during reverse .gif progression
GIF_FRAMES_PER_IMAGE_REVERSE = 1
# Whether or not to generate an additional video from all rendered images

# VIDEO-RELATED VARIABLES
# VIDEO RENDERING FUNCTIONALITY HAS NOT YET BEEN COMPLETED
CREATE_VIDEO = True
# Path at which the resulting video will be saved, if CREATE_GIF = True
VIDEO_PATH = "output/video2.avi"
# Whether or not to play the video frames in reverse when the end is reached, transitioning back to the original source
#    image instead of abruptly jumping right back to the start
REVERSE_VIDEO_AT_END = True
# Number of times to repeat each rendered image during forward video progression
# Effectively lengthens the time for which each frame is visible in the animated .gif
VIDEO_FRAMES_PER_IMAGE_FORWARD = 3
# Number of times to repeat each rendered image during reverse video progression
VIDEO_FRAMES_PER_IMAGE_REVERSE = 1


"""
_________________________________________________
TODO
_________________________________________________
 - Implement ability to perform operations based on neighboring pixels
 - Add functionality for video output instead of just .gif animations
 - Create GUI to allow users to interactively apply filters and functions, with deep control over the underlying math
     as well as the ability to render in various formats
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
        # List of file paths of all rendered images
        self.outputFileList = []
        # An array of pixels representing the input image. Used for reference but never modified.
        self.pixelsIn = self.imageIn.load()
        # An array of pixels representing the output image. Initialized identical to self.pixelsIn
        # Modified over time while iterating through rows/columns. Should not be used for reference.
        self.pixelsOut = self.imageOut.load()
        # Tracks when all image manipulation routines are complete
        self.manipulationComplete = False
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
    def modHueShift(self, rgbIn, shift):
        hsvIn = self.fromRGBtoHSV(rgbIn)
        hsvOut = ((hsvIn[0] + shift) % 360, hsvIn[1], hsvIn[2])
        rgbOut = self.fromHSVtoRGB(hsvOut)
        return rgbOut

    # Shifts the Saturation value by a given number of degrees
    def modSaturationShift(self, rgbIn, shift):
        hsvIn = self.fromRGBtoHSV(rgbIn)
        hsvOut = (hsvIn[0], (hsvIn[1] + shift) % 360, hsvIn[2])
        rgbOut = self.fromHSVtoRGB(hsvOut)
        return rgbOut

    # Shifts the Value value by a given number of degrees
    def modValueShift(self, rgbIn, shift):
        hsvIn = self.fromRGBtoHSV(rgbIn)
        hsvOut = (hsvIn[0], hsvIn[1], (hsvIn[2] + shift) % 360)
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
    def rgbFunc(self, manip_index):
        rgbResult = self.pixelsIn[self.currentX, self.currentY]
        """
        rgbResult = self.modHueShift(rgbResult, ((self.currentX + 1) % (self.currentY + 1)) % 360)
        rgbResult = self.modHueShift(rgbResult, (self.currentY + 1) % 90)
        rgbResult = self.modHueShift(rgbResult, self.currentY)
        """
        if manip_index == 1:
            rgbResult = self.modHueShift(rgbResult, ((self.currentX + 1) % (self.currentY + 1)) % 360)
        elif manip_index == 2:
            rgbResult = self.modHueShift(rgbResult, (self.currentY + 1) % 90)
        elif manip_index == 3:
            rgbResult = self.modHueShift(rgbResult, self.currentY)
        elif manip_index == 4:
            rgbResult = self.modRotate1RGB(rgbResult)
        elif manip_index == 5:
            rgbResult = self.modHueShift(rgbResult, 69)
        elif manip_index == 6:
            rgbResult = self.modValueShift(rgbResult, -0.3)
        elif manip_index == 7:
            rgbResult = self.modValueShift(rgbResult, 0.3)
        elif manip_index == 8:
            rgbResult = self.modSaturationShift(rgbResult, -0.3)
        elif manip_index == 9:
            rgbResult = self.modSaturationShift(rgbResult, 0.3)
        else:
            print("Invalid manip_index: " + str(manip_index) + ".  No manipulation performed")
            self.manipulationComplete = True
            return 0
        #"""
        return rgbResult

    def manipulate(self):
        for n in range(NUM_ROUNDS_OF_MANIPULATION):
            self.manipulationComplete = False
            m = 1
            while self.manipulationComplete == False:
                x_bound_diff = 0
                y_bound_diff = 0
                while (x_bound_diff < self.xRes * 0.2) or (x_bound_diff > self.xRes * 0.8):
                    x_bound_1 = random.randrange(0, self.xRes)
                    x_bound_2 = random.randrange(0, self.xRes)
                    x_bound_diff = abs(x_bound_2 - x_bound_1)
                while (y_bound_diff < self.yRes * 0.2) or (y_bound_diff > self.yRes * 0.8):
                    y_bound_1 = random.randrange(0, self.yRes)
                    y_bound_2 = random.randrange(0, self.yRes)
                    y_bound_diff = abs(y_bound_2 - y_bound_1)
                for y in range(min(y_bound_1, y_bound_2), max(y_bound_1, y_bound_2)):
                    if self.manipulationComplete:
                        break
                    for x in range(min(x_bound_1, x_bound_2), max(x_bound_1, x_bound_2)):
                        if self.manipulationComplete:
                            break
                        self.currentX = x
                        self.currentY = y
                        self.pixelsOut[self.currentX, self.currentY] = self.rgbFunc(m)
                m += 1
                self.render()
        return 0

    # Saves an output image with filename based on the current frame number
    def render(self):
        if MULTIPLE_RENDERS:
            self.currentFrame += 1
        outputFilePath = Path(OUTPUT_IMG + "_" + str(self.currentFrame) + OUTPUT_IMG_EXTENSION)
        self.outputFileList.append(outputFilePath)
        self.imageOut.save(outputFilePath)
        print("Output image " + str(self.currentFrame) + " rendered.")
        return 0

    # Creates a .gif animation with a separate frame for each rendered image
    def createGIF(self):
        images = []
        currentFrame = 1
        for filename in self.outputFileList:
            for i in range(GIF_FRAMES_PER_IMAGE_FORWARD):
                images.append(imageio.imread(filename))
                print("Frame " + str(currentFrame) + " of " + GIF_PATH + " rendered.")
                currentFrame += 1
        if REVERSE_GIF_AT_END:
            for filename in reversed(self.outputFileList):
                for i in range(GIF_FRAMES_PER_IMAGE_REVERSE):
                    images.append(imageio.imread(filename))
                    print("Frame " + str(currentFrame) + " of " + GIF_PATH + " rendered.")
                    currentFrame += 1
        print("Saving .gif animation...")
        imageio.mimsave(GIF_PATH, images)
        print(".gif animation saved.")
        return 0

    # Creates a video animation with a separate frame for each rendered image
    def createVideo(self):
        return 0

    # Ensures that the directory specified for the output image(s) exists to avoid errors in self.render()
    @staticmethod
    def prepareDirectory():
        output_image_directory = os.path.dirname(OUTPUT_IMG)
        os.makedirs(output_image_directory, exist_ok=True)
        gif_directory = os.path.dirname(GIF_PATH)
        os.makedirs(gif_directory, exist_ok=True)
        video_directory = os.path.dirname(GIF_PATH)
        os.makedirs(video_directory, exist_ok=True)
        return 0

def main():
    random.seed("3:33")
    cont = Container()
    cont.prepareDirectory()
    cont.manipulate()
    if CREATE_GIF:
        cont.createGIF()
    if CREATE_VIDEO:
        cont.createVideo()
    print("\n================ C O M P L E T E D ================\n")
    return 0

main()