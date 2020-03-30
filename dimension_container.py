# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. Shift responsibility for window dimension definition to hypnic_launcher.py
#  B. Change dimensions to be less static and more scalable
#    1. Some things still need to remain static, but overall want to write the GUI to support all standard resolutions
#      a. In the future may need to do more advanced stuff with resolution detection
#    2. For now it should suffice to design a layout which fulfills the following requirements:
#      a. Functions at all widths between 33% and 100% of 1920px
#      b. Functions at all heights between 50% and 100% of 1080px
#      c. Functions at all aspect ratios between 4:3 and 16:9
#  D. Instead of hard-coding rightContentWidth I can do percent scaling using the weight specifications
#     (currently within HypnicGUI) in calls of the grid_[row/column]configure() methods!
#    1. This is an amazing StackOverflow answer by Bryan Oakley (of course) which should make things intuitive
#  E. Rename the subframes belonging to Controls Frame to something more meaningful than just integer names!

__name__ = "dimension_container"

# Library Inputs
import math
from tkinter import CENTER


class DimensionContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    def __init__(self, gui_):

        # So that the DimensionContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        # MEMBER VARIABLES
        # I M P O R T A N T     N O T E S :
        # All of these are used by the GUI's StyleContainer instance, so these dimensions must be defined beforehand!
        # Column (COL) and Row (ROW) values provided are zero-indexed!
        # Unless specified otherwise, a widget exists within ROW 0 of its parent widget!
        # Unless specified otherwise, a widget exists within COLUMN (COL) 0 of its parent widget!
        # Unless specified otherwise, padding variables refer to internal padding!
        self.internalPaddingButton = 0  # FLAG: Hard-coded GUI parameter!
        self.externalPaddingButton = 0  # FLAG: Hard-coded GUI parameter!
        self.defaultInternalPaddingGrid = 0  # FLAG: Hard-coded GUI parameter!
        self.defaultExternalPaddingGrid = 0  # FLAG: Hard-coded GUI parameter!

        # Defaults related to the place() method of ttk Label objects
        # Because the grid() method is used heavily, everything should be centered unless otherwise specified
        self.defaultPlaceRelX = 0.5
        self.defaultPlaceRelY = 0.5
        self.defaultPlaceAnchor = CENTER

        # WINDOW AS A WHOLE
        self.windowPadX = self.defaultInternalPaddingGrid
        self.windowPadY = self.defaultInternalPaddingGrid
        self.windowWidth = 1800  # FLAG: Hard-coded GUI parameter!
        self.windowHeight = 1000  # FLAG: Hard-coded GUI parameter!

        # TOP TOOLBAR (ROW 0 OF WINDOW)
        self.topToolbarPadX = self.defaultInternalPaddingGrid
        self.topToolbarPadY = self.defaultInternalPaddingGrid
        self.topToolbarHeight = 60  # FLAG: Hard-coded GUI parameter!

        # BOTTOM TOOLBAR (ROW 2 OF WINDOW)
        self.bottomToolbarPadX = self.defaultInternalPaddingGrid
        self.bottomToolbarPadY = self.defaultInternalPaddingGrid
        self.bottomToolbarHeight = 60  # FLAG: Hard-coded GUI parameter!

        # BOTTOM INFOBAR (ROW 3 OF WINDOW)
        self.bottomInfobarPadX = self.defaultInternalPaddingGrid
        self.bottomInfobarPadY = self.defaultInternalPaddingGrid
        self.bottomInfobarHeight = 30  # FLAG: Hard-coded GUI parameter!

        # MAIN CONTENT (ROW 1 OF WINDOW)
        # Dependent on dimensions of ROW 0, ROW 2, and ROW 3
        self.mainContentPadX = self.defaultInternalPaddingGrid
        self.mainContentPadY = self.defaultInternalPaddingGrid
        self.mainContentHeight = self.windowHeight - self.windowPadY - \
                                 self.topToolbarHeight - self.bottomToolbarHeight - self.bottomInfobarHeight

        # LEFT CONTENT (COL 0 OF MAIN CONTENT)
        # The left content is a square-shaped frame spanning the left side, and entire height, of mainContent
        self.leftContentPadX = self.defaultInternalPaddingGrid
        self.leftContentPadY = self.defaultInternalPaddingGrid
        # Height is equal to the internal height of mainContent
        self.leftContentHeight = self.mainContentHeight - self.mainContentPadY
        # the Left content is a square by design, so its width is initialized as its height
        self.leftContentWidth = self.leftContentHeight

        # PHOTO BOXES ([0,0], [0,1], [1,0], [1,1] OF LEFT CONTENT)
        # Each photo box has half the width and height of leftContent
        # They are arranged in a 2 x 2 square grid layout
        self.photoBoxPadX = self.defaultInternalPaddingGrid
        self.photoBoxPadY = self.defaultInternalPaddingGrid
        self.photoBoxWidth = math.floor((self.leftContentWidth - self.leftContentPadX) / 2)
        self.photoBoxHeight = math.floor((self.leftContentHeight - self.leftContentPadY) / 2)

        # RIGHT CONTENT (COL 2 OF MAIN CONTENT)
        self.rightContentPadX = self.defaultInternalPaddingGrid
        self.rightContentPadY = self.defaultInternalPaddingGrid
        # TODO: Instead of hard-coding rightContentWidth I can do percent scaling using the weight specifications
        #  (currently within HypnicGUI) in calls of the grid_[row/column]configure() methods! See note at top of file.
        self.rightContentWidth = 300  # FLAG: Hard-coded GUI parameter!
        # Height is equal to the internal height of mainContent, which has already been calculated for leftContent
        self.rightContentHeight = self.leftContentHeight

        # CENTER CONTENT (COL 1 OF MAIN CONTENT)
        # The controls frame fills the remaining space within mainContent that is not already occupied
        # by either leftContent or rightContent
        self.centerContentPadX = self.defaultInternalPaddingGrid
        self.centerContentPadY = self.defaultInternalPaddingGrid
        # centerContent's width is that of the entire window minus the widths of leftContent and rightContent
        self.centerContentWidth = self.windowWidth - self.windowPadX - self.leftContentWidth - self.rightContentWidth
        # Height is equal to the internal height of mainContent, which has already been calculated for leftContent
        self.centerContentHeight = self.leftContentHeight

        # CONTROL BOXES WITHIN CENTER CONTENT
        # Sets the number of rows into which the Controls Frame should be divided (evenly)
        self.numControlRows = 5  # FLAG: Hard-coded GUI parameter!
        self.numControlColumns = 2  # FLAG: Hard-coded GUI parameter!
        # No need to define individual widths/heights for these frames as they are all relative to centerContent dims
        self.controlBoxPadX = self.defaultInternalPaddingGrid
        self.controlBoxPadY = self.defaultInternalPaddingGrid
