# TODO:
#  ==============================================================================
#  S. I'm running into some pretty major efficiency issues already (see grayscalePixels() for example) and really need
#     to be careful about preventing things from going too far in that direction
#    1. It's okay for now while I just focus on the possibility of functionality, BUT
#    2. At the same time I don't want to back myself into a corner of requiring huge rework (like a new class) later on
#  ==============================================================================
#  A. Write some sort of "filtering" framework (maybe a new class) to make the application of simple filters (like
#       grayscale, etc.) possible with shorter, more straightforward functions
#  B. Consider combining addPixels and subtractPixels (and future related functions) into one common function.
#    1. They are massively similar in content and, although not improving computational efficiency, would be pretty easy
#  C. Write some sort of framework to make interpolation between colors (and extrapolation operations) more streamlined

__name__ = "edit_container"

# Library Imports
import random
import PIL
import math

# Local Imports
import hypnic_helpers


class EditContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    def __init__(self, gui_):

        # So that the ManipContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        self.defaultScaleResampleMode = PIL.Image.LANCZOS

    # Resizes an image, preserving aspect ratio
    # o is the index of the target image slot for output, within the ImageContainer's pilImages list
    # i is the index of the image to be used for input
    # Essentially an extended implementation of PIL.Image.resize() with support for limitations and relative scaling
    # USAGE INSTRUCTIONS:
    # With absolute set to True, image will be scaled such that the pixel dimensions are equal to xParam and yParam
    # With absolute set to False, image dimensions will be multiplied by xParam and yParam
    #   In order to prevent accidental overgrowth which could lead to RAM issues, xParam and yParam are limited as follows:
    #     a value above 2.0 with absolute=False will reset val to equal scaleImageDefaultRatio
    #     and a value above 2000 with absolute=True will reset it to scaleImageDefaultMaxDim
    #   Similarly, too-low values will be reset to their defaults from within self.gui.dims
    # TODO: TEST THE DIFFERENT SCALE RESAMPLE MODES
    #   Options are:
    #    - PIL.Image.NEAREST (default)
    #    - PIL.Image.BILINEAR
    #    - PIL.Image.BICUBIC
    #    - PIL.Image.LANCZOS (current choice and presumed to be the highest quality)
    #   Since scaling isn't happening much as of yet, high quality is preferred over optimizing algorithm speed
    def scaleImage(self, o, i, absolute=True, xParam=0, yParam=0):  # FLAG: Hard-coded GUI parameter!

        print("Executing EditContainer.scaleImage() with i = " + str(i) +
              "; absolute = " + str(absolute) +
              "; xParam = " + str(xParam) +
              "; xParam = " + str(xParam))

        # Allows a warning to be printed if either param ends up being rejected and reset
        warnRejectedX = False
        warnRejectedY = False
        # (Re)sets xParam and yParam values if necessary
        if absolute:
            if (xParam is None) or (xParam > self.gui.dims.scaleImageMaxAbsolute) or (xParam < 1):
                xParam = self.gui.dims.scaleImageDefaultAbsolute
                warnRejectedX = True
            if (yParam is None) or (yParam > self.gui.dims.scaleImageMaxAbsolute) or (yParam < 1):
                yParam = self.gui.dims.scaleImageDefaultAbsolute
                warnRejectedY = True
        else:
            if (xParam is None) or (xParam > self.gui.dims.scaleImageMaxRelative) or (xParam <= 0):
                xParam = self.gui.dims.scaleImageDefaultRatio
                warnRejectedX = True
            if (yParam == None) or (yParam > self.gui.dims.scaleImageMaxRelative) or (yParam <= 0):
                yParam = self.gui.dims.scaleImageDefaultRatio
                warnRejectedY = True
            # In the RELATIVE CASE, regardless of reset: Ensures that the ratios are not mistakenly handled as integers
            xParam = float(xParam)
            yParam = float(yParam)

        # Warns the user, if deemed necessary in the above if/else blocks
        if warnRejectedX or warnRejectedY:
            print("================================================================")
            print("WARNING: One or more of the provided scaling parameters were rejected as invalid.")
            print("All rejected parameters have been reset to DimensionContainer.scaleImageMax[Absolute/Relative].")
            print("Relevant Python file:                           edit_container.py")
            print("Relevant function:                              EditContainer.scaleImage()")
            print("Relevant parameters:")
            if warnRejectedX:
                print("     - xParam of " + str(xParam) + " rejected by EditContainer.scaleImage()")
            if warnRejectedY:
                print("     - yParam of " + str(yParam) + " rejected by EditContainer.scaleImage()")
            print()

        # Gets the necessary image parameters
        # TODO: Add some sort of invariant to ensure that pilImagesTemp is empty?
        self.gui.img.pilImagesTemp = [self.gui.img.pilImages[i].copy()]
        pixels = self.gui.img.pilImagesTemp[0].load()
        # The X and Y resolutions of the current element within ImageContainer.pilImages
        xResCurrent = self.gui.img.pilImages[i].size[0]
        yResCurrent = self.gui.img.pilImages[i].size[1]

        # If absolute then the new resolutions are simply equal to the params
        if absolute:
            xResNew = xParam
            yResNew = yParam
        # If not absolute then xResNew and yResNew are params multiplied by xResCurrent and yResCurrent respectively
        # math.ceil() is used as opposed to math.floor() in an attempt to avoid ever achieving a dimension of 0
        else:
            xResNew = math.ceil(xParam * xResCurrent)
            yResNew = math.ceil(yParam * yResCurrent)

        # Performs the scaling operation
        self.gui.img.pilImagesTemp[0] = self.gui.img.pilImagesTemp[0].resize((xResNew, yResNew),
                                                                             self.defaultScaleResampleMode)

        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(o)

        return o


    # Turns an image (image i) into a grayscale version of itself and places that image into the Photo Box of index o
    # ratio defines the magnitude of the change, which is 1.0 (100%) by default
    #   e.g. 1.0 implies full transition to grayscale; 0.5 will cause each pixel to go halfway and 0.0 does nothing
    def grayscalePixels(self, o, i, ratio_=1.0):

        # Ensures that the ratio is not erroneously handled as an integer
        ratio = float(ratio_)

        # Loads the PIL Image into gui.img.pilImagesTemp for editing
        # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
        # TODO: Add some sort of invariant to ensure that pilImagesTemp is empty?
        self.gui.img.pilImagesTemp = [self.gui.img.pilImages[i].copy()]
        pixelsEdit = self.gui.img.pilImagesTemp[0].load()
        # The X and Y resolutions of the current element within ImageContainer.pilImages
        xRes = self.gui.img.pilImages[i].size[0]
        yRes = self.gui.img.pilImages[i].size[1]
        # Iterates through each row and column of the image, manipulating pixels accordingly
        for row in range(yRes):
            for col in range(xRes):
                colorIn = pixelsEdit[col, row]
                colorOut = list(colorIn)
                luminosityVal = hypnic_helpers.getLuminosity(colorIn)

                # If ratio is 1.0, then each of r/g/b are all equal to the luminosity
                if ratio == 1.0:
                    colorOut = [luminosityVal, luminosityVal, luminosityVal]
                # If ratio is not 1.0, the change in each pixel is only partial
                else:
                    print("FUCK")
                    # TODO: Replace this operation with a function for interpolation and extrapolation
                    colorOut = [math.floor(colorIn[0] + ratio * (luminosityVal - colorIn[0])),
                                math.floor(colorIn[1] + ratio * (luminosityVal - colorIn[1])),
                                math.floor(colorIn[2] + ratio * (luminosityVal - colorIn[2]))]

                # Excludes channels if necessary, based on the ch[Red/GreenBlue]Channel state variables
                if not self.gui.stateObj.chRedChannel.get():
                    colorOut[0] = colorIn[0]
                if not self.gui.stateObj.chGreenChannel.get():
                    colorOut[1] = colorIn[1]
                if not self.gui.stateObj.chBlueChannel.get():
                    colorOut[2] = colorIn[2]

                # Updates the pixel color
                pixelsEdit[col, row] = tuple(colorOut)


        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(o)

        return o


    # Turns some fraction of an image's pixels to random colors
    # o is the index of the target image slot for output, within the ImageContainer's pilImages list
    # i is the index of the image to be used for input
    # ratio_ is a float between 0 and 1 inclusive representing the fraction of pixels to be transformed
    # If no value for ratio_ is provided, all pixels in the entire image will be randomized
    def randomizePixelColors(self, o, i, ratio_=1.0):

        # Ensures that the ratio is not erroneously handled as an integer
        ratio = float(ratio_)

        # Loads the PIL Image into gui.img.pilImagesTemp for editing
        # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
        # TODO: Add some sort of invariant to ensure that pilImagesTemp is empty?
        self.gui.img.pilImagesTemp = [self.gui.img.pilImages[i].copy()]
        pixelsEdit = self.gui.img.pilImagesTemp[0].load()
        # The X and Y resolutions of the current element within ImageContainer.pilImages
        xRes = self.gui.img.pilImages[i].size[0]
        yRes = self.gui.img.pilImages[i].size[1]
        # Iterates through each row and column of the image, manipulating pixels accordingly
        for row in range(yRes):
            for col in range(xRes):
                if random.random() <= ratio:
                    pixelsEdit[col, row] = hypnic_helpers.getRandomRGB()

        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(o)

        return o

    # Adds one image to another image
    # o is the index of the target image slot for output, within the ImageContainer's pilImages list
    # i1 is the index of the primary image to be used for input
    # i2 is the index of the secondary image to be used for input
    def addPixels(self, o, i1, i2):

        # Whether or not pixel colors should "wrap" when below 0 or above 255, instead of just min/maxing out
        wrapInt = self.gui.stateObj.chWrapColors.get()
        wrapBool = False
        if wrapInt:
            wrapBool = True

        # Loads the PIL Image into gui.img.pilImagesTemp for editing
        # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
        # TODO: Add some sort of invariant to ensure that pilImagesTemp is empty?
        self.gui.img.pilImagesTemp = [self.gui.img.pilImages[i1].copy()]
        pixelsEdit = self.gui.img.pilImagesTemp[0].load()
        # Also creates and loads a copy of the secondary input image, to get its pixel color data
        #   NOTE: No need to do this for the primary input image because it's stored in pixelsEdit already
        pixelsIn2 = self.gui.img.pilImages[i2].copy().load()
        # The X and Y resolutions over which to iterate are the minimums from each of the two input images
        xRes = min(self.gui.img.pilImages[i1].size[0], self.gui.img.pilImages[i2].size[0])
        yRes = min(self.gui.img.pilImages[i1].size[1], self.gui.img.pilImages[i2].size[1])
        # Iterates through each row and column of the image, manipulating pixels accordingly
        for row in range(yRes):
            for col in range(xRes):
                color1 = pixelsEdit[col, row]
                color2 = pixelsIn2[col, row]
                # uses fixOutOfRangeColors() from hypnic_helpers to ensure all values are between 0 and 255 inclusive
                pixelsEdit[col, row] = hypnic_helpers.fixOutOfRangeColors((color1[0] + color2[0],
                                                                           color1[1] + color2[1],
                                                                           color1[2] + color2[2]),
                                                                          wrapBool)
        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(o)

        return o

    # Subtracts one image from another image
    # o is the index of the target image slot for output, within the ImageContainer's pilImages list
    # i1 is the index of the primary image to be used for input
    # i2 is the index of the secondary image to be used for input
    def subtractPixels(self, o, i1, i2):

        # Whether or not pixel colors should "wrap" when below 0 or above 255, instead of just min/maxing out
        wrapInt = self.gui.stateObj.chWrapColors.get()
        wrapBool = False
        if wrapInt:
            wrapBool = True

        # Loads the PIL Image into gui.img.pilImagesTemp for editing
        # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
        # TODO: Add some sort of invariant to ensure that pilImagesTemp is empty?
        self.gui.img.pilImagesTemp = [self.gui.img.pilImages[i1].copy()]
        pixelsEdit = self.gui.img.pilImagesTemp[0].load()
        # Also creates and loads a copy of the secondary input image, to get its pixel color data
        #   NOTE: No need to do this for the primary input image because it's stored in pixelsEdit already
        pixelsIn2 = self.gui.img.pilImages[i2].copy().load()
        # The X and Y resolutions over which to iterate are the minimums from each of the two input images
        xRes = min(self.gui.img.pilImages[i1].size[0], self.gui.img.pilImages[i2].size[0])
        yRes = min(self.gui.img.pilImages[i1].size[1], self.gui.img.pilImages[i2].size[1])
        # Iterates through each row and column of the image, manipulating pixels accordingly
        for row in range(yRes):
            for col in range(xRes):
                color1 = pixelsEdit[col, row]
                color2 = pixelsIn2[col, row]
                # uses fixOutOfRangeColors() from hypnic_helpers to ensure all values are between 0 and 255 inclusive
                pixelsEdit[col, row] = hypnic_helpers.fixOutOfRangeColors((color1[0] - color2[0],
                                                                           color1[1] - color2[1],
                                                                           color1[2] - color2[2]),
                                                                          wrapBool)  # TODO: Specify WRAP via a radiobutton!
        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(o)

        return o