# TODO:
#  A. Shift responsibility for window dimension definition to hypnic_launcher.py
#  B. Change dimensions to be less static and more scalable
#    1. Some things still need to remain static, but overall want to write the GUI to support all standard resolutions
#      a. In the future may need to do more advanced stuff with resolution detection
#    2. For now it should suffice to design a layout which fulfills the following requirements:
#      a. Functions at all widths between 33% and 100% of 1920px
#      b. Functions at all heights between 50% and 100% of 1080px
#      c. Functions at all aspect ratios between 4:3 and 16:9
#  C. Rename "Right Frame" to something more meaningful
#    1. Trying to have yellow text in all points of the code (even in other files) where the name comes up
#    2. Will be more intuitive once I set a true plan for what to include in that frame
#  D. Instead of hard-coding rightFrameWidth I can do percent scaling using the weight specifications
#     (currently within HypnicGUI) in calls of the grid_[row/column]configure() methods!
#    1. This is an amazing StackOverflow answer by Bryan Oakley (of course) which should make things intuitive
#  E. Rename the subframes belonging to Controls Frame to something more meaningful than just integer names!

__name__ = "dimension_container"

# Library Inputs
import math

class DimensionContainer():

    def __init__(self):

        # I M P O R T A N T     N O T E S :
        # All of these are used by the GUI's StyleContainer instance, so these dimensions must be defined beforehand!
        # Column (COL) and Row (ROW) values provided are zero-indexed!
        # Unless specified otherwise, a widget exists within ROW 0 of its parent widget!
        # Unless specified otherwise, a widget exists within COLUMN (COL) 0 of its parent widget!
        # Unless specified otherwise, padding variables refer to internal padding!
        self.internalPaddingButton = 0 # Hard coded dimension value!
        self.externalPaddingButton = 0 # Hard coded dimension value!
        self.defaultInternalPaddingGrid = 0 # Hard coded dimension value!
        self.defaultExternalPaddingGrid = 0 # Hard coded dimension value!

        # WINDOW AS A WHOLE
        self.windowPadX = self.defaultInternalPaddingGrid
        self.windowPadY = self.defaultInternalPaddingGrid
        self.windowWidth = 1800 # Hard coded dimension value!
        self.windowHeight = 1000 # Hard coded dimension value!

        # TOP TOOLBAR (ROW 0 OF WINDOW)
        self.topToolbarPadX = self.defaultInternalPaddingGrid
        self.topToolbarPadY = self.defaultInternalPaddingGrid
        self.topToolbarHeight = 60 # Hard coded dimension value!

        # BOTTOM TOOLBAR (ROW 2 OF WINDOW)
        self.bottomToolbarPadX = self.defaultInternalPaddingGrid
        self.bottomToolbarPadY = self.defaultInternalPaddingGrid
        self.bottomToolbarHeight = 60 # Hard coded dimension value!

        # BOTTOM INFOBAR (ROW 3 OF WINDOW)
        self.bottomInfobarPadX = self.defaultInternalPaddingGrid
        self.bottomInfobarPadY = self.defaultInternalPaddingGrid
        self.bottomInfobarHeight = 30 # Hard coded dimension value!

        # MAIN CONTENT (ROW 1 OF WINDOW)
        # Dependent on dimensions of ROW 0, ROW 2, and ROW 3
        self.mainContentPadX = self.defaultInternalPaddingGrid
        self.mainContentPadY = self.defaultInternalPaddingGrid
        self.mainContentHeight = self.windowHeight - self.windowPadY -\
                                 self.topToolbarHeight - self.bottomToolbarHeight - self.bottomInfobarHeight

        # IMAGES FRAME (COL 0 OF MAIN CONTENT)
        # The images frame is a square-shaped frame spanning the left side, and entire height, of mainContent
        self.imagesFramePadX = self.defaultInternalPaddingGrid
        self.imagesFramePadY = self.defaultInternalPaddingGrid
        # Height is equal to the internal height of mainContent
        self.imagesFrameHeight = self.mainContentHeight - self.mainContentPadY
        # the Images Frame is a square by design, so its width is initialized as its height
        self.imagesFrameWidth = self.imagesFrameHeight

        # IMAGE FRAMES ([0,0], [0,1], [1,0], [1,1] OF IMAGES FRAME)
        # Each image frame has half the width and height of the imageFrame
        # They are arranged in a 2 x 2 square grid layout
        self.imageFramePadX = self.defaultInternalPaddingGrid
        self.imageFramePadY = self.defaultInternalPaddingGrid
        self.imageFrameWidth = math.floor((self.imagesFrameWidth - self.imagesFramePadX) / 2)
        self.imageFrameHeight = math.floor((self.imagesFrameHeight - self.imagesFramePadY) / 2)

        # RIGHT FRAME (COL 2 OF MAIN CONTENT)
        # The right frame is a temporarily named frame occupying the right side of mainContent, for its entire height
        # TODO: Rename Right Frame to something more meaningful
        self.rightFramePadX = self.defaultInternalPaddingGrid
        self.rightFramePadY = self.defaultInternalPaddingGrid
        # TODO: Instead of hard-coding rightFrameWidth I can do percent scaling using the weight specifications
        #  (currently within HypnicGUI) in calls of the grid_[row/column]configure() methods! See note at top of file.
        self.rightFrameWidth = 300 # Hard coded dimension value!
        # Height is equal to the internal height of mainContent, which has already been calculated for imagesFrame
        self.rightFrameHeight = self.imagesFrameHeight

        # TODO: Consider entirely renaming from "Controls Frame" to "Controls Frames", since it's a parent frame which
        #       will contain subframes that are all related to control.
        #       This would be more in-line with the naming convention of "Images Frame"
        # CONTROLS FRAME (COL 1 OF MAIN CONTENT)
        # The controls frame fills the remaining space within mainContent that is not already occupied
        # by either imagesFrame or rightFrame
        # TODO: Rename Right Frame to something more meaningful [not in code below but in comment(s) above]
        self.controlsFramePadX = self.defaultInternalPaddingGrid
        self.controlsFramePadY = self.defaultInternalPaddingGrid
        # controlsFrame's width is that of the entire window minus the widths of imagesFrame and rightFrame
        self.controlsFrameWidth = self.windowWidth - self.windowPadX - self.imagesFrameWidth - self.rightFrameWidth
        # Height is equal to the internal height of mainContent, which has already been calculated for imagesFrame
        self.controlsFrameHeight = self.imagesFrameHeight

        # CONTROL FRAMES WITHIN CONTROLS FRAME
        # Sets the number of rows into which the Controls Frame should be divided (evenly)
        self.numControlRows = 5 # Hard coded dimension value!
        # No need to define individual widths/heights for these frames as they are all relative to controlsFrame dims
        self.controlFramePadX = self.defaultInternalPaddingGrid
        self.controlFramePadY = self.defaultInternalPaddingGrid
