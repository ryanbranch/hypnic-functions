# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. Placeholder

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

    # Resizes an image (at index i of the gui.img.pilImages list), preserving aspect ratio
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
    def scaleImage(self, i, absolute=True, xParam = 0, yParam = 0):  # FLAG: Hard-coded GUI parameter!

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
        pilImage = self.gui.img.pilImages[i]
        xResCurrent = pilImage.size[0]
        yResCurrent = pilImage.size[1]
        xResNew = xResCurrent
        yResNew = yResCurrent
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
        self.gui.img.pilImages[i] = pilImage.resize((xResNew, yResNew), self.defaultScaleResampleMode)

        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(i)

        return i

    # Turns some fraction of an image's pixels to random colors
    # i is the index of the relevant image, within the ImageContainer's pilImages list
    # ratio_ is a float between 0 and 1 inclusive representing the fraction of pixels to be transformed
    # If no value for ratio_ is provided, all pixels in the entire image will be randomized
    def randomizePixelColors(self, i, ratio_ = 1.0):

        # Ensures that the ratio is not erroneously handled as an integer
        ratio = float(ratio_)
        print("Executing EditContainer.initializeCommandNames() with i = " + str(i) + "; ratio_ = " + str(ratio_))

        # Loads the PIL Image for editing
        # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
        pixels = self.gui.img.pilImages[i].load()
        # The X and Y resolutions of the current element within ImageContainer.pilImages
        xRes = self.gui.img.pilImages[i].size[0]
        yRes = self.gui.img.pilImages[i].size[1]
        # Iterates through each row and column of the image, manipulating pixels accordingly
        for row in range(yRes):
            for col in range(xRes):
                if random.random() <= ratio:
                    pixels[col, row] = hypnic_helpers.getRandomRGB()

        # Updates the relevant ImageTk PhotoImage and GUI Image Label
        self.gui.img.updateImageLabel(i)

        return i
