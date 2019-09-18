import os
from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk
import PIL
import imageio
import cv2
import math
import random


# GLOBAL CONSTANTS
# ________________________________
# GENERAL VARIABLES
# Whether or not the image should be manipulated at all
# Can be disabled, for example, in situations when non-manipulation functionality is being tested
MANIPULATE_IMAGE = True
# Path to the image used as program input
INPUT_IMG = "input.jpg"
# Path at which the resulting image will be saved
OUTPUT_IMG = "output/output"
OUTPUT_IMG_EXTENSION = ".jpg"
# Whether every manipulation pass should cover a random range of the image (as opposed to the entire frame)
RANDOMIZE_MANIPULATION_POSITIONS = False
# If randomizing manipulation positions, defines the minimum and maximum dimensions for a manipulation area
# Defined as a fraction of the entire image dimension along the respective axis
RANDOM_MANIPULATION_MIN_X_DIM = 0.2
RANDOM_MANIPULATION_MAX_X_DIM = 0.8
RANDOM_MANIPULATION_MIN_Y_DIM = 0.2
RANDOM_MANIPULATION_MAX_Y_DIM = 0.8
# Whether or not to generate a new image each time the renderOutputImage() function
#     for an ImageManipulator object is called
MULTIPLE_RENDERS = True
# How many times to repeat the entire image manipulation process
# When a new round of manipulation begins, the final output image of the last round of manipulation is used as the base
#    image in the new round of manipulation
NUM_ROUNDS_OF_MANIPULATION = 1

# GIF-RELATED VARIABLES
# Whether or not to generate an animated GIF from all rendered images
CREATE_GIF = True
# Path at which the resulting animated GIF will be saved, if CREATE_GIF = True
GIF_PATH = "output/animation2.gif"
# The number of seconds for which each frame of the GIF will be displayed
GIF_SECONDS_PER_FRAME = 0.1
# Whether or not to play the animated GIF frames in reverse when the end is reached, transitioning back to the
#     original source image instead of abruptly jumping right back to the start
REVERSE_GIF_AT_END = False
# Number of times to repeat each rendered image during forward animated GIF progression
# Effectively lengthens the time for which each frame is visible in the animated GIF
GIF_FRAMES_PER_IMAGE_FORWARD = 1
# Number of times to repeat each rendered image during reverse animated GIF progression
GIF_FRAMES_PER_IMAGE_REVERSE = 1
# Determines the type of GIF which will be created. Options available are as follows
# 0: Each frame represents an image created from a given manipulation index, in order of creation
# 1: GIF transitions from input image to final output image, wiping along the X direction
# 2: GIF transitions from input image to final output image, wiping along the Y direction
GIF_MODE = 2
# The total number of frames to use in a wipe-style GIF (for example, GIF_MODE values 1 and 2)
GIF_NUM_WIPE_FRAMES = 30


# VIDEO-RELATED VARIABLES
# VIDEO RENDERING FUNCTIONALITY HAS NOT YET BEEN COMPLETED
CREATE_VIDEO = True
# Path at which the resulting video will be saved, if CREATE_GIF = True
VIDEO_PATH = "output/video2.avi"
# Whether or not to play the video frames in reverse when the end is reached, transitioning back to the original source
#    image instead of abruptly jumping right back to the start
REVERSE_VIDEO_AT_END = True
# Number of times to repeat each rendered image during forward video progression
# Effectively lengthens the time for which each frame is visible in the forward progression of the animated GIF
VIDEO_FRAMES_PER_IMAGE_FORWARD = 1
# Number of times to repeat each rendered image during reverse video progression
# Effectively lengthens the time for which each frame is visible in the reverse progression of the animated GIF
VIDEO_FRAMES_PER_IMAGE_REVERSE = 1

# GUI-RELATED VARIABLES
# Whether or not to use the GUI at all
# If disabled, then the program will simply create an image/gif/video based on other global variable values without
# allowing specific control over parameters
ENABLE_GUI = True


"""
_________________________________________________
#TODO
_________________________________________________
 - Implement GIF_MODE global variable as-described in the comments
 - Implement ability to perform operations based on neighboring pixels
 - Add functionality for video output instead of just animated GIFs
 - Update GUI to allow users to interactively apply filters and functions, with deep control over the underlying math
     as well as the ability to render in various formats
 - Condense Window class' createOutputImage(), createGif() and createVideo() code to avoid redundancy
"""

# tkinter instance for GUI display and user interaction related to manipulation of images
# based heavily on code from http://pythonprogramming.net by Sentdex
class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.manipulator = ImageManipulator()


    # Creation of window
    def init_window(self):

        # Change the title of the master widget
        self.master.title("hypnic-functions")
        # Allow the widget to take the full space of the root window
        self.pack(fill = BOTH, expand = 1)
        # Create a button instance
        quitButton = Button(self, text = "Quit", command = self.client_exit)
        # Place the button on the window
        quitButton.place(x = 0, y = 0)
        # Create a menu instance
        menu = Menu(self.master)
        self.master.config(menu = menu)
        # Create the file object
        file = Menu(menu)
        # Add a command called "Exit" to the menu option, which runs the function self.client_exit()
        file.add_command(label = "Exit", command = self.client_exit)
        # Add "File" to the menu
        menu.add_cascade(label = "File", menu = file)
        # Create the file object
        edit = Menu(menu)
        # Add a command called "Undo" to the menu option
        edit.add_command(label="Undo")
        # Add "Edit" to the menu
        menu.add_cascade(label = "Edit", menu = edit)
        # Add commands to the menu for doing the following:
        # Displaying the input image, generating/displaying the output image, showing text, creating an animated GIF,
        # and creating a video
        edit.add_command(label="Show Input Image", command=self.showInputImage)
        edit.add_command(label="Show Output Image", command=self.showOutputImage)
        edit.add_command(label="Create GIF", command=self.createGIF)
        edit.add_command(label="Create Video", command=self.createVideo)


    # Displays the input image
    def showInputImage(self):
        # Load the input image
        load = Image.open(INPUT_IMG)
        render = PIL.ImageTk.PhotoImage(load)
        # Display the input image
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        # Display some text related to displaying the input image
        text = Label(self, text="Input Image:")
        text.pack()

    # Shows the output image
    # If the output image hasn't already been created, creates it first
    def showOutputImage(self):
        if not self.manipulator.outputImageReady:
            # Display some text related to generating the output image
            # NOTE: This text display functionality is currently broken.
            #     Need to research tkinter text display more in order to determine why
            text = Label(self, text="Generating the output image... Please wait!")
            text.pack()
            self.createOutputImage()
        # Load the output image
        load = Image.open(self.manipulator.outputImagePath)
        render = PIL.ImageTk.PhotoImage(load)
        # Display the output image
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        # Display some text related to displaying the output image
        text = Label(self, text="Output Image:")
        text.pack()

    # Generates the output image if it hasn't already been created
    def createOutputImage(self):
        # Checks whether image manipulation has been enabled and responds accordingly
        if not MANIPULATE_IMAGE:
            # Display text notifying the user that image manipulation is disabled
            text = Label(self, text="ERROR: Image manipulation is disabled!")
            text.pack()
        else:
            # Checks if the output image has already been created
            if not self.manipulator.outputImageReady:
                # Tell the ImageManipulator object to perform the manipulation routine
                self.manipulator.manipulate()
                text = Label(self, text="Generating the output image... Please wait!")
                text.pack()
            # Displays the output image
            self.showOutputImage()

    # Generates the output image if it hasn't already been created
    def createGIF(self):
        # Checks whether image manipulation has been enabled and responds accordingly
        if not MANIPULATE_IMAGE:
            # Display text notifying the user that image manipulation is disabled
            text = Label(self, text="ERROR: Can't create GIF because image manipulation is disabled!")
            text.pack()
        elif not CREATE_GIF:
            # Display text notifying the user that animated GIF creation is disabled
            text = Label(self, text="ERROR: Animated GIF creation is disabled!")
            text.pack()
        else:
            # Checks if the output image has already been created
            if not self.manipulator.outputImageReady:
                # Tell the ImageManipulator object to perform the manipulation routine
                self.manipulator.manipulate()
                text = Label(self, text="Generating the output image... Please wait!")
                text.pack()
            # Checks if the animated GIF has already been created
            if not self.manipulator.gifReady:
                # Tell the ImageManipulator object to perform the animated GIF creation routine
                text = Label(self, text="Generating the animated GIF... Please wait!")
                text.pack()
                self.manipulator.generateGIF()
            else:
                text = Label(self, text="Animated GIF has already been created!")
                text.pack()
        self.showOutputImage()

    def createVideo(self):
        # Checks whether image manipulation has been enabled and responds accordingly
        if not MANIPULATE_IMAGE:
            # Display text notifying the user that image manipulation is disabled
            text = Label(self, text="ERROR: Can't create GIF because image manipulation is disabled!")
            text.pack()
        elif not CREATE_VIDEO:
            # Display text notifying the user that video creation is disabled
            text = Label(self, text="ERROR: Video creation is disabled!")
            text.pack()
        else:
            # Checks if the output image has already been created and if not, creates it
            if not self.manipulator.outputImageReady:
                # Tell the ImageManipulator object to perform the manipulation routine
                self.manipulator.manipulate()
                text = Label(self, text="Generating the output image... Please wait!")
                text.pack()
                # Checks if the video has already been created
                if not self.manipulator.videoReady:
                    # Tell the ImageManipulator object to perform the video creation routine
                    text = Label(self, text="Video generation has not yet been implemented!")
                    text.pack()
                    self.manipulator.generateGIF()
                else:
                    text = Label(self, text="Video has already been created!")
                    text.pack()

    # Exit of window
    def client_exit(self):
        exit()

# Container class for holding all variables and functions related to manipulation of images
class ImageManipulator:

    def __init__(self):
        # MEMBER VARIABLES UPON INITIALIZATION
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
        # Suffix to apply to the filename of the current version of self.imageOut upon running self.renderOutputImage()
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
        # Path to which the output image is saved
        self.outputImagePath = Path("")
        # Tracks whether or not the output image is ready to be displayed
        self.outputImageReady = False
        # Tracks whether or not the output animated GIF has been created
        self.gifReady = False
        # Tracks whether or not the output video has been created
        self.videoReady = False
        # Internal variable used to track error incidences during debugging
        self.errorCount = 0

        self.prepareDirectories()

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
    def calcCartesianFunc(xIn, slope, yIntercept):
        yOut = round(xIn * slope + yIntercept)
        return yOut

    # Swaps the Saturation and Value values for a pixel
    def modFlipSV(self, rgbIn):
        hsvIn = self.fromRGBtoHSV(rgbIn)
        hsvOut = (hsvIn[0], hsvIn[2], hsvIn[1])
        rgbOut = self.fromHSVtoRGB(hsvOut)
        return rgbOut

    # Moves Saturation and Value values closer together by a given percentage factor of their difference
    # A factor of 100 (100%) leads to Saturation being equal to Value, specifically the two being equal to the average
    #     of their original values
    # If a negative factor is provided, the two are moved away from each other by the same magnitude which would be
    #     present if they were moving closer together
    # To prevent results which lead to invalid output ranges, the final values have a modulus of 1 applied at the end
    def modSlideSV(self, rgbIn, factor):
        rgbOut = rgbIn
        hsvIn = self.fromRGBtoHSV(rgbIn)
        if hsvIn[1] < hsvIn[2]:
            hsvOut = (hsvIn[0], hsvIn[1] + math.fabs(hsvIn[2] - hsvIn[1]) * (float(factor) / 2) % 1, hsvIn[2] - math.fabs(hsvIn[2] - hsvIn[1]) * (float(factor) / 2) % 1)
        elif hsvIn[2] < hsvIn[1]:
            hsvOut = (hsvIn[0], hsvIn[1] - math.fabs(hsvIn[1] - hsvIn[2]) * (float(factor) / 2) % 1, hsvIn[2] + math.fabs(hsvIn[2] - hsvIn[1]) * (float(factor) / 2) % 1)
        else:
            return rgbIn
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
    def calcFromCustomDomainRGB(valIn, lowerBound, upperBound, yIntBelow, slopeBelow, yIntAbove, slopeAbove):
        valOut = valIn
        if valIn <= lowerBound:
            dist = valOut - lowerBound
            valOut += slopeBelow * dist + yIntBelow
        elif valIn >= upperBound:
            dist = upperBound - valOut
            valOut += slopeAbove * dist + yIntAbove
        valOut %= 255
        valOut = int(round(valOut))
        return valOut

    # Allows a H value to be shifted using an algebraic function, if it falls below a lower bound or above an
    #     upper bound. Magnitude of shift is calculated based on a linear equation. Separate slope and Y-intercept
    #     values are used depending on whether the input H value falls below or above a specified bound
    @staticmethod
    def calcFromCustomDomainH(valIn, lowerBound, upperBound, yIntBelow, slopeBelow, yIntAbove, slopeAbove):
        valOut = valIn
        if valIn <= lowerBound:
            dist = valOut - lowerBound
            valOut += slopeBelow * dist + yIntBelow
        elif valIn >= upperBound:
            dist = upperBound - valOut
            valOut += slopeAbove * dist + yIntAbove
        valOut %= 360
        valOut = int(round(valOut))
        return valOut

    # Allows a S or V value to be shifted using an algebraic function, if it falls below a lower bound or above an
    #     upper bound. Magnitude of shift is calculated based on a linear equation. Separate slope and Y-intercept
    #     values are used depending on whether the input S/V value falls below or above a specified bound
    @staticmethod
    def calcFromCustomDomainSV(valIn, lowerBound, upperBound, yIntBelow, slopeBelow, yIntAbove, slopeAbove):
        valOut = valIn
        if valIn <= lowerBound:
            dist = valOut - lowerBound
            valOut += slopeBelow * dist + yIntBelow
        elif valIn >= upperBound:
            dist = upperBound - valOut
            valOut += slopeAbove * dist + yIntAbove
        valOut %= 1
        valOut = int(round(valOut))
        return valOut

    # Determines the new R/G/B value of a pixel based on X/Y coordinate and existing R/G/B value
    # Currently the only purpose is to call the desired modification function(s)
    def rgbFunc(self, manip_index):

        rgbResult = self.pixelsIn[self.currentX, self.currentY]
        rgbResultOriginal = rgbResult
        if manip_index == 1:
            rgbResult = (self.calcFromCustomDomainRGB(rgbResult[0], 127, 128, 0, 0.5, 128, -1),
                         self.calcFromCustomDomainRGB(rgbResult[0], 127, 128, 0, 0.5, 128, -1),
                         self.calcFromCustomDomainRGB(rgbResult[0], 127, 128, 0, 0.5, 128, -1))
        elif manip_index == 2:
            rgbResult = (self.calcFromCustomDomainRGB(rgbResult[1], 127, 128, 32, 0, 64, -1),
                         self.calcFromCustomDomainRGB(rgbResult[1], 127, 128, 64, 0, 64, -1),
                         self.calcFromCustomDomainRGB(rgbResult[1], 127, 128, 128, 0, 64, -1))
        elif manip_index == 3:
            rgbResult = (self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 64, 0, 32, -1),
                         self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 128, 0, 32, -1),
                         self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 255, 0, 32, -1))
        elif manip_index == 4:
            rgbResult = (self.calcFromCustomDomainRGB(rgbResult[0], 127, 128, 10, 0, 128, 1),
                         self.calcFromCustomDomainRGB(rgbResult[0], 127, 128, 90, 0, 128, 1),
                         self.calcFromCustomDomainRGB(rgbResult[0], 127, 128, 50, 0, 128, 1))
        elif manip_index == 5:
            rgbResult = (self.calcFromCustomDomainRGB(rgbResult[1], 127, 128, 90, 0, 64, 1),
                         self.calcFromCustomDomainRGB(rgbResult[1], 127, 128, 180, 0, 64, 1),
                         self.calcFromCustomDomainRGB(rgbResult[1], 127, 128, 45, 0, 64, 1))
        elif manip_index == 6:
            rgbResult = (self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 19, 0, 32, 1),
                         self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 39, 0, 32, 1),
                         self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 29, 0, 32, 1))
        elif manip_index == 7:
            rgbResult = self.modSlideSV(rgbResult, 1)

        else:
            print("Invalid manip_index: " + str(manip_index) + ".  No manipulation performed")
            self.manipulationComplete = True
            return 0
        """
        if manip_index == 1:
            rgbResult = self.modHueShift(rgbResult, ((self.currentX + 1) % (self.currentY + 1)) % 360)
        elif manip_index == 2:
            rgbResult = self.modHueShift(rgbResult, (self.currentY + 1) % random.randrange(90, 270))
        elif manip_index == 3:
            rgbResult = self.modHueShift(rgbResult, self.currentY)
        elif manip_index == 4:
            rgbResult = self.modHueShift(rgbResult, (self.currentX + 1) % random.randrange(90, 270))
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
        """
        return rgbResult
        #"""

    def manipulate(self):

        for n in range(NUM_ROUNDS_OF_MANIPULATION):
            self.manipulationComplete = False
            m = 1
            while self.manipulationComplete == False:
                render = True
                if RANDOMIZE_MANIPULATION_POSITIONS:
                    x_bound_diff = 0
                    y_bound_diff = 0
                    while (x_bound_diff < self.xRes * RANDOM_MANIPULATION_MIN_X_DIM) or\
                            (x_bound_diff > self.xRes * RANDOM_MANIPULATION_MAX_X_DIM):
                        x_bound_1 = random.randrange(0, self.xRes)
                        x_bound_2 = random.randrange(0, self.xRes)
                        x_bound_diff = abs(x_bound_2 - x_bound_1)
                    while (y_bound_diff < self.yRes * RANDOM_MANIPULATION_MIN_Y_DIM) or\
                            (y_bound_diff > self.yRes * RANDOM_MANIPULATION_MAX_Y_DIM):
                        y_bound_1 = random.randrange(0, self.yRes)
                        y_bound_2 = random.randrange(0, self.yRes)
                        y_bound_diff = abs(y_bound_2 - y_bound_1)
                else:
                    y_bound_1 = 0
                    y_bound_2 = self.yRes - 1
                    x_bound_1 = 0
                    x_bound_2 = self.xRes - 1
                for y in range(min(y_bound_1, y_bound_2), max(y_bound_1, y_bound_2)):
                    if self.manipulationComplete:
                        break
                    for x in range(min(x_bound_1, x_bound_2), max(x_bound_1, x_bound_2)):
                        if self.manipulationComplete:
                            break
                        self.currentX = x
                        self.currentY = y
                        result = self.rgbFunc(m)
                        if result != 0:
                            self.pixelsOut[self.currentX, self.currentY] = result
                            render = True
                        else:
                            render = False
                m += 1
                if render:
                    self.renderOutputImage()
        return 0

    # Saves an output image with filename based on the current frame number
    def renderOutputImage(self):
        if MULTIPLE_RENDERS:
            self.currentFrame += 1
        self.outputImagePath = Path(OUTPUT_IMG + "_" + str(self.currentFrame) + OUTPUT_IMG_EXTENSION)
        self.outputFileList.append(self.outputImagePath)
        self.imageOut.save(self.outputImagePath)
        print("Output image " + str(self.currentFrame) + " rendered and saved.")
        self.outputImageReady = True
        return 0

    # Creates an animated GIF with a separate frame for each rendered image
    def generateGIF(self):
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
        print("Saving animated GIF...")
        kargs = {'duration': GIF_SECONDS_PER_FRAME}
        imageio.mimsave(GIF_PATH, images, format = "GIF", **kargs)
        print("Animated GIF saved.")
        self.gifReady = True
        return 0

    # Creates a video animation with a separate frame for each rendered image
    def generateVideo(self):
        print("Video generation has not yet been implemented!")
        #self.videoReady = True
        return 0

    # Ensures that the directory specified for the output image(s) exists to avoid errors
    @staticmethod
    def prepareDirectories():
        print("PREPARING DIRECTORIES...")
        if MANIPULATE_IMAGE:
            output_image_directory = os.path.dirname(OUTPUT_IMG)
            os.makedirs(output_image_directory, exist_ok=True)
        if CREATE_GIF:
            gif_directory = os.path.dirname(GIF_PATH)
            os.makedirs(gif_directory, exist_ok=True)
        if CREATE_VIDEO:
            video_directory = os.path.dirname(GIF_PATH)
            os.makedirs(video_directory, exist_ok=True)

def main():
    # Initializes the random number generator
    random.seed("three hundred and thirty three")

    if ENABLE_GUI:

        root = Tk()

        # Creating the Window instance, and by extension the ImageManipulator instance
        app = Window(root)
        # Defining GUI window size
        root.geometry(str(app.manipulator.xRes) + "x" + str(app.manipulator.yRes))

        # Initiating GUI window display
        root.mainloop()
    else:
        manip = ImageManipulator()
        if MANIPULATE_IMAGE:
            manip.manipulate()
        if CREATE_GIF:
            manip.generateGIF()
        if CREATE_VIDEO:
            manip.generateVideo()

    print("\n================ C O M P L E T E D ================\n")
    return 0

main()