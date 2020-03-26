import math

__name__ = "dimension_container"

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
        self.mainContentHeight = self.windowHeight - self.windowPadY - self.topToolbarHeight - self.bottomToolbarHeight - self.bottomInfobarHeight

        self.imagesFramePadX = self.defaultInternalPadding
        self.imagesFramePadY = self.defaultInternalPadding
        self.imagesFrameHeight = self.mainContentHeight - self.mainContentPadY
        self.imagesFrameWidth = self.imagesFrameHeight

        self.imageFramePadX = self.defaultInternalPadding
        self.imageFramePadY = self.defaultInternalPadding
        self.imageFrameWidth = math.floor((self.imagesFrameWidth - self.imagesFramePadX) / 2)
        self.imageFrameHeight = math.floor((self.imagesFrameHeight - self.imagesFramePadY) / 2)
        self.print(self.imagesFrameWidth, self.imagesFrameHeight, self.imageFrameWidth, self.imageFrameHeight)

        self.controlFramePadX = self.defaultInternalPadding
        self.controlFramePadY = self.defaultInternalPadding
        self.controlFrameWidth = self.windowWidth - self.windowPadX - self.imagesFrameWidth
        self.controlFrameHeight = self.imagesFrameHeight