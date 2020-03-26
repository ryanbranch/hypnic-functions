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

import math

class DimensionContainer():

    def __init__(self):

        self.defaultInternalPadding = 0
        self.defaultExternalPadding = 0

        self.windowPadX = self.defaultInternalPadding
        self.windowPadY = self.defaultInternalPadding
        self.windowWidth = 1800
        self.windowHeight = 1010

        self.topToolbarPadX = self.defaultInternalPadding
        self.topToolbarPadY = self.defaultInternalPadding
        self.topToolbarHeight = 60

        self.bottomToolbarPadX = self.defaultInternalPadding
        self.bottomToolbarPadY = self.defaultInternalPadding
        self.bottomToolbarHeight = 60

        self.bottomInfobarPadX = self.defaultInternalPadding
        self.bottomInfobarPadY = self.defaultInternalPadding
        self.bottomInfobarHeight = 30

        self.mainContentPadX = self.defaultInternalPadding
        self.mainContentPadY = self.defaultInternalPadding
        self.mainContentHeight = self.windowHeight - self.windowPadY -\
                                 self.topToolbarHeight - self.bottomToolbarHeight - self.bottomInfobarHeight

        self.imagesFramePadX = self.defaultInternalPadding
        self.imagesFramePadY = self.defaultInternalPadding
        self.imagesFrameHeight = self.mainContentHeight - self.mainContentPadY
        # the Images Frame is a square by design, so its width is initialized as its height
        self.imagesFrameWidth = self.imagesFrameHeight

        self.imageFramePadX = self.defaultInternalPadding
        self.imageFramePadY = self.defaultInternalPadding
        self.imageFrameWidth = math.floor((self.imagesFrameWidth - self.imagesFramePadX) / 2)
        self.imageFrameHeight = math.floor((self.imagesFrameHeight - self.imagesFramePadY) / 2)

        self.controlFramePadX = self.defaultInternalPadding
        self.controlFramePadY = self.defaultInternalPadding
        self.controlFrameWidth = self.windowWidth - self.windowPadX - self.imagesFrameWidth
        self.controlFrameHeight = self.imagesFrameHeight
