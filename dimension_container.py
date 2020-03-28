# TODO:
#  A. Shift responsibility for window dimension definition to hypnic_launcher.py
#  B. Change dimensions to be less static and more scalable
#    1. Some things still need to remain static, but overall want to write the GUI to support all standard resolutions
#      a. In the future may need to do more advanced stuff with resolution detection
#    2. For now it should suffice to design a layout which fulfills the following requirements:
#      a. Functions at all widths between 33% and 100% of 1920px
#      b. Functions at all heights between 50% and 100% of 1080px
#      c. Functions at all aspect ratios between 4:3 and 16:9

__name__ = "dimension_container"

# Library Inputs
import math

class DimensionContainer():

    def __init__(self):

        # used by the GUI's StyleContainer instance, so these dimensions must be defined beforehand
        self.internalPaddingButton = 0
        self.externalPaddingButton = 0

        self.defaultInternalPaddingGrid = 0
        self.defaultExternalPaddingGrid = 0

        self.windowPadX = self.defaultInternalPaddingGrid
        self.windowPadY = self.defaultInternalPaddingGrid
        self.windowWidth = 1800
        self.windowHeight = 1000

        self.topToolbarPadX = self.defaultInternalPaddingGrid
        self.topToolbarPadY = self.defaultInternalPaddingGrid
        self.topToolbarHeight = 60

        self.bottomToolbarPadX = self.defaultInternalPaddingGrid
        self.bottomToolbarPadY = self.defaultInternalPaddingGrid
        self.bottomToolbarHeight = 60

        self.bottomInfobarPadX = self.defaultInternalPaddingGrid
        self.bottomInfobarPadY = self.defaultInternalPaddingGrid
        self.bottomInfobarHeight = 30

        self.mainContentPadX = self.defaultInternalPaddingGrid
        self.mainContentPadY = self.defaultInternalPaddingGrid
        self.mainContentHeight = self.windowHeight - self.windowPadY -\
                                 self.topToolbarHeight - self.bottomToolbarHeight - self.bottomInfobarHeight

        self.imagesFramePadX = self.defaultInternalPaddingGrid
        self.imagesFramePadY = self.defaultInternalPaddingGrid
        self.imagesFrameHeight = self.mainContentHeight - self.mainContentPadY
        # the Images Frame is a square by design, so its width is initialized as its height
        self.imagesFrameWidth = self.imagesFrameHeight

        self.imageFramePadX = self.defaultInternalPaddingGrid
        self.imageFramePadY = self.defaultInternalPaddingGrid
        self.imageFrameWidth = math.floor((self.imagesFrameWidth - self.imagesFramePadX) / 2)
        self.imageFrameHeight = math.floor((self.imagesFrameHeight - self.imagesFramePadY) / 2)

        self.controlFramePadX = self.defaultInternalPaddingGrid
        self.controlFramePadY = self.defaultInternalPaddingGrid
        self.controlFrameWidth = self.windowWidth - self.windowPadX - self.imagesFrameWidth
        self.controlFrameHeight = self.imagesFrameHeight
