# TODO:
#  A. Implement functionalities which result from changes in focus between frames
#  B. Add member variable arrays to HypnicGUI which store the grid, frame, label objects in a dictionary
#  C. Keys should be strings like "topToolbar", "photoBoxTR", etc.
#    1. Don't have to write code to support SOLELY managing the objects via list operations
#    2. But should still support it for keeping code clean and for using list operations WHERE REASONABLE.
#  D. Consider creating a new widget_container.py file (or some other name with similar meaning)
#    1. Not immediately necessary, but the GUI is gonna become more and more complicated so it may make more sense
#       to handle initialization-related aspects of the program within a class
#    2. A WidgetContainer object would likely hold the StyleContainer instance (which itself holds a DimensionContainer)
#    3. It's REALLY not great practice that I'm initializing member variables like frames outside of __init__()
#      a. Would be better to, at that point within defineGrid(), initialize a WidgetContainer() instance which holds
#         those widgets as member variables AND defines them within its __init__ function
#  E. If clearing IS important, consider using
#             del tempList[:]
#         But don't jump to conclusions on doing so
#    1. Don't want to accidentally call any destructors for ttk objects and such,
#       since many will be referenced by two or more lists

__name__ = "hypnic_gui"

# Library Inputs
import tkinter
from tkinter import CENTER, ttk

# Local Inputs
import image_container
import style_container
import hypnic_helpers

# G L O B A L   V A R I A B L E S
# Path to the text document which lists the paths to all input images
# TODO: Remove this global and define it from user input at runtime
INPUT_IMAGE_PATHS_FILE = "hypnic_images.txt"  # FLAG: Hard-coded GUI parameter!


class HypnicGUI(tkinter.Tk):

    def __init__(self, wrapper_, *args, **kwargs):

        # TODO: Consider using dicts instead of lists, for storing the ttk widgets and such

        # I N I T I A L I Z A T I O N     O F     W I D G E T - R E L A T E D     V A R I A B L E S
        # GENERAL WIDGET LIST
        # Stores all of the ttk widgets that belong to the GUI
        # Widgets include but are not limited to instances of Frame, Label, Button, etc.
        self.widgets = []

        # SPECIFIC WIDGET LISTS
        # Stores  the ttk INPUT-RELATED widget instances.
        # NOTE: This *CAN* include ttk Button objects for example, even though they have their own wider-scoped list
        self.inputWidgets = []

        # I N I T I A L I Z A T I O N     O F     F R A M E - R E L A T E D     V A R I A B L E S
        # GENERAL FRAME LIST
        # Stores all of the ttk Frame objects that belong to the GUI
        # Any time a Frame is created, it should be placed in this list to support iteration
        self.frames = []

        # CUSTOM FRAME LISTS (mainly for storing frames which do not have their own individual member variables)
        #     - Also potentially useful for keeping narrow-scope groups of similar frames together
        # self.photoBoxFrames stores each of the 4 frames held within self.photoBox
        #   NOTE: self.leftContent is currently not defined until self.defineGrid()
        #         This may change if something like a WidgetContainer/TtkContainer class is written for the purpose
        #           of ensuring that all member variables can be initialized within some class' __init__() function
        # TODO: I really don't feel great about this naming convention and should at least consider changing it
        #  Perhaps "photoBox" is a horrible name, since both "image" and "frame" will be incredibly common generic
        #  terms appearing within variable names
        #  Frame names like "mainContent", "topToolbar" etc. are pretty good
        #    Might be even better with the word "Frame" at the end to denote this!
        self.photoBoxFrames = []
        # self.controlBoxFrames stores each frame from each row within self.controlBox
        #   NOTE: self.controlBox is currently not defined until self.defineGrid()
        #         This may change if something like a WidgetContainer/TtkContainer class is written for the purpose
        #           of ensuring that all member variables can be initialized within some class' __init__() function
        self.controlBoxFrames = []

        # I N I T I A L I Z A T I O N     O F     L A B E L - R E L A T E D     V A R I A B L E S
        # GENERAL LABEL LIST
        # Stores all of the ttk Label objects that belong to the GUI
        # Any time a Label is created, it should be placed in this list to support iteration
        self.labels = []

        # SPECIFIC LABEL LISTS
        # Divides labels into separate lists based on whether or not they contain associated images or text
        #   NOTE: There is no need to create a "SPECIFIC IMAGE LABEL LISTS" section, or anything of the sort
        #         Instead, it's enough to have a "Specific __ List" for each widget type (Frame, Label, etc.)
        # Stores  the ttk Label objects which have an assigned image property
        # NOTE: If a Label doe not contain an image but is developed for the ability to contain one, include it in here
        self.imageLabels = []
        # Stores  the ttk Label objects which have some assigned text property
        # NOTE: If a Label doe not inherently/immediately contain text but is developed to contain it, include it
        # TODO: Determine whether textvariable Label objects should also be included within the array for text Labels,
        #       and/or vice versa, or kept mutually exclusive from one another
        self.textLabels = []
        # Stores  the ttk Label objects which have some assigned textvariable property
        # NOTE: If a Label doe not contain a textvariable but is developed to potentially contain it, include it
        self.textvariableLabels = []

        # CUSTOM LABEL LISTS (Mainly for storing labels which do not have their own individual member variables)
        #     - Also potentially useful for keeping narrow-scope groups of similar frames together
        # self.photoBoxImageLabels stores each of the 4 Labels which hold images for each of the 4 "photoBox*" frames
        self.photoBoxImageLabels = []

        # I N I T I A L I Z A T I O N     O F     B U T T O N - R E L A T E D     V A R I A B L E S
        # GENERAL BUTTON LIST
        # Stores all of the ttk Button objects that belong to the GUI
        # Any time a Button is created, it should be placed in this list to support iteration
        self.buttons = []

        # CUSTOM BUTTON LISTS (mainly for storing labels which do not have their own individual member variables)
        #     - Also potentially useful for keeping narrow-scope groups of similar frames together

        # Stores each of the buttons that fall within any of the Control Box frames in CenterContent
        # The number of buttons in this array is currently based on the row/col vals set manually in DimensionContainer
        # May support multiple buttons per grid cell in the future
        self.controlBoxButtons = []



        # self.wrapper should ALWAYS reference "app" from within hypnic_wrapper.py's main() function
        # a new HypnicWrapper instance should never be defined
        self.wrapper = wrapper_

        # Begins by running the initialization function for the basic instance of tkinter.Tk
        tkinter.Tk.__init__(self, *args, **kwargs)

        # StyleContainer Object instance
        # self.scObj should be the ONLY StyleContainer instance!
        # it should hold a DimensionContainer instance at self.scObj.dims (defined within StyleContainer.__init__()!
        # self.scObj.dims should be the ONLY DimensionContainer instance!
        self.scObj = style_container.StyleContainer()

        # ImageContainer Object Instance
        # self.img should be the ONLY ImageContainer instance!
        # TODO: Replace INPUT_IMAGE_PATHS_FILE with runtime user input, the entire reason it's passed in by the GUI
        self.img = image_container.ImageContainer(INPUT_IMAGE_PATHS_FILE)

        # Configuring additional overarching GUI window properties
        # It's completely fine for these to be hard-coded as it's not anything the user should have or need control over
        self.iconbitmap(default='media/hficon.ico')
        self.wm_title("hypnic-functions GUI Client")
        # NOTE: The line below can be uncommented in order to force a specific set of window dimensions
        # self.minsize(width=self.scObj.dims.windowWidth, height=self.scObj.dims.windowHeight)
        self.maxsize(width=self.scObj.dims.windowWidth, height=self.scObj.dims.windowHeight)
        self.state('zoomed')

        # Calls functions related to constructing the GUI and initializes associated values
        self.defineGrid()
        self.colorFrames()
        self.fillGrid()
        self.styleWidgets()

    # Defines the GUI layout using tkinter's grid() and Frame() modules
    def defineGrid(self):

        # tempList is a temporary list used to store elements which will be appended to member variable lists which
        #   contain relevant ttk objects such as self.frames, self.widgets, etc.
        # This is being done as a best practice for code readability as things can get ugly when dealing with appends
        #   to more than just one of the member variable lists
        tempList = []

        # FRAMES WHICH ARE CHILDREN OF THE WINDOW AS A WHOLE
        # Defines the main 4 containers: Top Toolbar, Main Content, Bottom Toolbar, and Bottom Infobar
        self.topToolbar = tkinter.ttk.Frame(self, height=self.scObj.dims.topToolbarHeight)
        self.mainContent = tkinter.ttk.Frame(self)
        self.bottomToolbar = tkinter.ttk.Frame(self, height=self.scObj.dims.bottomToolbarHeight)
        self.bottomInfobar = tkinter.ttk.Frame(self, height=self.scObj.dims.bottomInfobarHeight)

        # Specifies that mainContent is the (only) row which should have expansion priority
        self.grid_rowconfigure(1, weight=1)
        # Specifies that column 0 (the only column, containing all of the 4 main frames) should expand to maximum width
        # This is important so that columns within the frames of each mainContent row have proper width behavior
        self.grid_columnconfigure(0, weight=1)

        # Populates templist with the newly defined frames
        tempList = [self.topToolbar, self.mainContent, self.bottomToolbar, self.bottomInfobar]
        # Iterates through the newly-defined tempList, appending all values to the relevant widget lists
        for e in tempList:
            self.widgets.append(e)
            self.frames.append(e)

        # In this case because each element has separate values for padding, the current DimensionContainer framework
        # does not support iteratively calling the ttk.Frame.grid() method for the newly created frames
        # So we arrange the 4 main containers manually instead
        self.topToolbar.grid(row=0, sticky="nsew", ipadx=self.scObj.dims.topToolbarPadX,
                             ipady=self.scObj.dims.topToolbarPadY)
        self.mainContent.grid(row=1, sticky="nsew", ipadx=self.scObj.dims.mainContentPadX,
                              ipady=self.scObj.dims.mainContentPadY)
        self.bottomToolbar.grid(row=2, sticky="nsew", ipadx=self.scObj.dims.bottomToolbarPadX,
                                ipady=self.scObj.dims.bottomToolbarPadY)
        self.bottomInfobar.grid(row=3, sticky="nsew", ipadx=self.scObj.dims.bottomInfobarPadX,
                                ipady=self.scObj.dims.bottomInfobarPadY)
        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []

        # FRAMES WHICH ARE CHILDREN OF self.mainContent
        # Defines the 3 container frames within Main Content: Left Content, Center Content, and Right Content
        self.leftContent = tkinter.ttk.Frame(self.mainContent, width=self.scObj.dims.leftContentWidth)
        self.centerContent = tkinter.ttk.Frame(self.mainContent)
        # NOTE: Instead of hard-coding the width of rightContent, can set it relative to centerContent by removing the
        #       explicit width definition and calling grid_columnconfigure() for BOTH columns 1 AND 2
        # TODO: Consider implementing the above NOTE
        self.rightContent = tkinter.ttk.Frame(self.mainContent, width=self.scObj.dims.rightContentWidth)

        # Specifies that mainContent's row 0 (the only row) and column 1 (Center Content) have priority for space-filling
        self.mainContent.grid_rowconfigure(0, weight=1)
        self.mainContent.grid_columnconfigure(1, weight=1)

        # Populates templist with the newly defined frames
        tempList = [self.leftContent, self.centerContent, self.rightContent]
        # Iterates through the newly-defined tempList, appending all values to the relevant widget lists
        for e in tempList:
            self.widgets.append(e)
            self.frames.append(e)

        # In this case because each element has separate values for padding, the current DimensionContainer framework
        # does not support iteratively calling the ttk.Frame.grid() method for the newly created frames
        # So we arrange each of the three column containers manually
        self.leftContent.grid(row=0, column=0, sticky="nsew", ipadx=self.scObj.dims.leftContentPadX,
                              ipady=self.scObj.dims.leftContentPadY)
        self.centerContent.grid(row=0, column=1, sticky="nsew", ipadx=self.scObj.dims.centerContentPadX,
                                ipady=self.scObj.dims.centerContentPadY)
        self.rightContent.grid(row=0, column=2, sticky="nsw", ipadx=self.scObj.dims.rightContentPadX,
                               ipady=self.scObj.dims.rightContentPadY)

        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []

        # FRAMES WHICH ARE CHILDREN OF self.leftContent
        # Defines the individual image display frames within the Left Content
        self.photoBoxTL = tkinter.ttk.Frame(self.leftContent, width=self.scObj.dims.photoBoxWidth,
                                            height=self.scObj.dims.photoBoxHeight)
        self.photoBoxTR = tkinter.ttk.Frame(self.leftContent, width=self.scObj.dims.photoBoxWidth,
                                            height=self.scObj.dims.photoBoxHeight)
        self.photoBoxBL = tkinter.ttk.Frame(self.leftContent, width=self.scObj.dims.photoBoxWidth,
                                            height=self.scObj.dims.photoBoxHeight)
        self.photoBoxBR = tkinter.ttk.Frame(self.leftContent, width=self.scObj.dims.photoBoxWidth,
                                            height=self.scObj.dims.photoBoxHeight)

        # Specifies that each row and column within the Left Content has equal priority for space-filling
        self.leftContent.grid_rowconfigure(0, weight=1)
        self.leftContent.grid_columnconfigure(0, weight=1)
        self.leftContent.grid_rowconfigure(1, weight=1)
        self.leftContent.grid_columnconfigure(1, weight=1)



        # Populates templist with the newly defined frames
        tempList = [self.photoBoxTL, self.photoBoxTR, self.photoBoxBL, self.photoBoxBR]
        # Iterates through the newly-defined tempList,
        # Also arranges the grid elements, making use of getGridPos() from hypnic_helpers.py
        # e is the Frame object within tempList and i is the index of that object
        for i, e in enumerate(tempList):
            # Appends to the relevant lists
            self.widgets.append(e)
            self.frames.append(e)
            self.photoBoxFrames.append(e)
            # leftContent has 2 rows and 2 columns
            # hypnic_helpers.getGridPos is used to convert i to a (row, col) tuple based on the 2 x 2 arrangement
            pos = hypnic_helpers.getGridPos(i, 2, 2)
            # Uses pos to configure placement within the grid
            e.grid(row=pos[0], column=pos[1], sticky="nsew", ipadx=self.scObj.dims.photoBoxPadX,
                   ipady=self.scObj.dims.photoBoxPadY)

        # In this case because each element has separate values for row/column, I originally wrote the grid arrangement
        #   code in a non-iterative fashion. Keeping this down here just in case.
        """
        # TODO: Remove eventually, as it's now being done iteratively
        self.photoBoxTL.grid(row=0, column=0, sticky="nsew", ipadx=self.scObj.dims.photoBoxPadX,
                               ipady=self.scObj.dims.photoBoxPadY)
        self.photoBoxTR.grid(row=0, column=1, sticky="nsew", ipadx=self.scObj.dims.photoBoxPadX,
                               ipady=self.scObj.dims.photoBoxPadY)
        self.photoBoxBL.grid(row=1, column=0, sticky="nsew", ipadx=self.scObj.dims.photoBoxPadX,
                               ipady=self.scObj.dims.photoBoxPadY)
        self.photoBoxBR.grid(row=1, column=1, sticky="nsew", ipadx=self.scObj.dims.photoBoxPadX,
                               ipady=self.scObj.dims.photoBoxPadY)
        # Adds the frames to self.frames
        self.frames.append(self.photoBoxTL)
        self.frames.append(self.photoBoxTR)
        self.frames.append(self.photoBoxBL)
        self.frames.append(self.photoBoxBR)
        """

        # FRAMES WHICH ARE CHILDREN OF self.centerContent
        # Defines the individual control frames as rows within self.centerContent
        # These are not stored as directly-callable member variables but instead exist within their own list.
        #   This list, self.centerContents, is an even-more-specific list maintained IN ADDITION TO the other relevant
        #   lists like self.frames as opposed to being a replacement

        # Iterates through the number of rows and columns specified within dimension_container.py
        for r in range(self.scObj.dims.numControlRows):
            for c in range(self.scObj.dims.numControlColumns):
                # Initializes (and appends to self.widgets) a new Frame with self.centerContent as a parent
                # TODO: I BELIEVE that my appending to a member variable which was initialized in __init__, all of those
                #       Frame entities should continue to exist indefinitely. But if I run into problems, this very
                #       well could be the cause and I'll have to learn more about memory management in Python OOP
                self.widgets.append(tkinter.ttk.Frame(self.centerContent))
                # Appends the same Frame to self.frames and self.controlBoxFrames
                self.frames.append(self.widgets[-1])
                self.controlBoxFrames.append(self.widgets[-1])
                # Specifies that the relevant row and column of self.centerContent has equal priority for space-filling
                self.centerContent.grid_rowconfigure(r, weight=1)
                self.centerContent.grid_columnconfigure(c, weight=1)
                # Specifies that the newly initialized Frame is a member of the grid cell at (row, col) in centerContent
                self.widgets[-1].grid(row=r, column=c, sticky="nsew", ipadx=self.scObj.dims.controlBoxPadX,
                                      ipady=self.scObj.dims.controlBoxPadY)

    # Colors the frames defined in self.defineGrid()
    # NOTE: Currently based on random generation because I'm not concerned about this aspect of things
    def colorFrames(self):
        for f in range(len(self.frames)):
            self.frames[f].configure(style=self.scObj.frameStyles[f])

    # Fills the previously-defined GUI with label elements
    def fillGrid(self):
        # tempList is a temporary list used to store elements which will be appended to member variable lists which
        #   contain relevant ttk objects such as self.labels, self.imageLabels, self.buttons, etc.
        # This is being done as a best practice for code readability as things can get ugly when dealing with appends
        #   to more than just one of the member variable lists
        tempList = []

        # WIDGETS IN TOP TOOLBAR


        # WIDGETS IN MAIN CONTENT
        #  - WIDGETS IN LEFT CONTENT
        #    - WIDGETS IN PHOTO BOX FRAMES
        # Defines image Labels for each photoBox of leftContent
        for i in range(4):
            # Initializes (and appends to self.widgets) a new Label with the relevant self.photoBoxFrames elt as parent
            # TODO: I BELIEVE that my appending to a member variable which was initialized in __init__, all of those
            #       Frame entities should continue to exist indefinitely. But if I run into problems, this very
            #       well could be the cause and I'll have to learn more about memory management in Python OOP
            self.widgets.append(tkinter.ttk.Label(self.photoBoxFrames[i], image=self.img.tkImages[i]))
            # Appends the same Label to self.labels, self.imageLabels, and self.photoBoxImageLabels
            self.labels.append(self.widgets[-1])
            self.imageLabels.append(self.widgets[-1])
            self.photoBoxImageLabels.append(self.widgets[-1])
            # Places the Image Label within its frame
            self.widgets[-1].place(relx=self.scObj.dims.defaultPlaceRelX,
                                   rely=self.scObj.dims.defaultPlaceRelY,
                                   anchor=self.scObj.dims.defaultPlaceAnchor)

        #  - WIDGETS IN CENTER CONTENT
        #    - WIDGETS IN CONTROL BOX FRAMES
        # Defines buttons for each controlBox of centerContent (total number is rows multiplied by columns)
        for i in range(self.scObj.dims.numControlRows * self.scObj.dims.numControlColumns):
            # Initializes (and appends to self.widgets) a new Button with the relevant self.controlBoxFrames elt as parent
            # TODO: I BELIEVE that my appending to a member variable which was initialized in __init__, all of those
            #       Frame entities should continue to exist indefinitely. But if I run into problems, this very
            #       well could be the cause and I'll have to learn more about memory management in Python OOP
            self.widgets.append(tkinter.ttk.Button(self.controlBoxFrames[i]))
            # Appends the same Button to self.buttons, self.inputWidgets, and self.controlBoxImageLabels
            self.buttons.append(self.widgets[-1])
            self.inputWidgets.append(self.widgets[-1])
            self.controlBoxButtons.append(self.widgets[-1])
            # Places the Button within its frame
            self.widgets[-1].place(relx=self.scObj.dims.defaultPlaceRelX,
                                   rely=self.scObj.dims.defaultPlaceRelY,
                                   anchor=self.scObj.dims.defaultPlaceAnchor)
        # Configures the text for each of the newly created buttons
        # For the time being, if I want to set human-defined button text within the code I could create a list where
        #   each element is a string and the number of elements is equal to the number of buttons, etc.
        # TODO: Either use the variable below or get rid of it entirely
        self.controlBoxButtonStrings = []
        for i, b in enumerate(self.controlBoxButtons):
            self.controlBoxButtons[i].configure(text=("Button " + str(i)))
#
#
#
#
        self.buttonUndo = tkinter.ttk.Button(self.centerContent, text="Undo")
        self.buttonApply = tkinter.ttk.Button(self.centerContent, text="Apply")
        self.buttonSave = tkinter.ttk.Button(self.centerContent, text="Save")

        # Populates templist with the newly defined buttons
        tempList = [self.buttonUndo, self.buttonApply, self.buttonSave]
        # Iterates through the newly-defined tempList, appending all values to both self.labels and self.imageLabels
        # as well as carrying out the ttk.Label.place() method on each element
        for e in tempList:
            self.widgets.append(e)
            self.buttons.append(e)
            self.inputWidgets.append(e)

            # TODO: Remove this random placement, it's only present for testing
            import random
            xFac = random.randint(2, 8) / 10.0
            yFac = random.randint(2, 8) / 10.0
            e.place(relx=xFac, rely=yFac, anchor=self.scObj.dims.defaultPlaceAnchor)

        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []


        # WIDGETS IN BOTTOM TOOLBAR


        # WIDGETS IN BOTTOM INFOBAR


    # Sets the necessary style parameters for each ttk-specific widget
    def styleWidgets(self):
        print("PLACEHOLDER FOR CONTENT WITHIN THE HypnicGUI.styleWidgets() function")
