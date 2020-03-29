# TODO:
#  0. CHANGE NAMING CONVENTIONS RELATED TO TTK OBJECTS (and lists of them)
#    1. Really need to maintain readability from here on out. This should be done SOONER rather than LATER.
#    2. This element was added on 2020-03-29 at 5:59 AM, for future reference

# TODO: ================================( LINE TO EMPHASIZE THE ABOVE CONTENT )================================

# TODO:
#  A. Implement functionalities which result from changes in focus between frames
#  B. Add member variable arrays to HypnicGUI which store the grid, frame, label objects in a dictionary
#  C. Keys should be strings like "topToolbar", "imageFrameTR", etc.
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
from hypnic_helpers import *

# G L O B A L   V A R I A B L E S
# Path to the text document which lists the paths to all input images
# TODO: Remove this global and define it from user input at runtime
INPUT_IMAGE_PATHS_FILE = "hypnic_images.txt"


class HypnicGUI(tkinter.Tk):

    def __init__(self, wrapper_, *args, **kwargs):

        # TODO: Consider using dicts instead of lists, for storing the ttk widgets and such


        # Stores all of the ttk widgets that belong to the GUI
        # Widgets include but are not limited to instances of Frame, Label, Button, etc.
        self.widgets = []


        # GENERAL FRAME LIST

        # Stores all of the ttk Frame objects that belong to the GUI
        # Any time a Frame is created, it should be placed in this list to support iteration
        self.frames = []


        # SPECIFIC FRAME LISTS (storing frames which do not have their own individual member variables)

        # self.imageFrameFrames stores each of the 4 frames held within self.imageFrame
        #   NOTE: self.imagesFrame is currently not defined until self.defineGrid()
        #         This may change if something like a WidgetContainer/TtkContainer class is written for the purpose
        #           of ensuring that all member variables can be initialized within some class' __init__() function
        # TODO: I really don't feel great about this naming convention and should at least consider changing it
        #  Perhaps "imageFrame" is a horrible name, since both "image" and "frame" will be incredibly common generic
        #  terms appearing within variable names
        #  Frame names like "mainContent", "topToolbar" etc. are pretty good
        #    Might be even better with the word "Frame" at the end to denote this!
        self.imageFrameFrames = []

        # self.controlFrameFrames stores each frame from each row within self.controlFrame
        #   NOTE: self.controlFrame is currently not defined until self.defineGrid()
        #         This may change if something like a WidgetContainer/TtkContainer class is written for the purpose
        #           of ensuring that all member variables can be initialized within some class' __init__() function
        self.controlFrameFrames = []


        # GENERAL LABEL LIST
        # Stores all of the ttk Label objects that belong to the GUI
        # Any time a Label is created, it should be placed in this list to support iteration
        self.labels = []
        # SPECIFIC LABEL LISTS (storing labels which do not have their own individual member variables)
        #   NOTE: There is no need to create a "SPECIFIC IMAGE LABEL LISTS" section, or anything of the sort
        #         Instead, it's enough to have a "Specific __ List" for each widget type (Frame, Label, etc.)
        # self.imageFrameImageLabels stores each of the 4 Labels which hold each of the 4 "imageFrame" images
        self.imageFrameImageLabels = []

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
        # Stores  the ttk BUTTON objects
        self.buttonWidgets = []
        # Stores  the ttk INPUT-RELATED widget instances.
        # NOTE: This *CAN* include ttk Butotn objects for example, even though they have their own wider-scoped list
        self.inputWidgets = []


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
        self.iconbitmap(default='media/hficon.ico')
        self.wm_title("hypnic-functions GUI Client")
        # NOTE: The line below can be uncommented in order to force a specific set of window dimensions
        #self.minsize(width=self.scObj.dims.windowWidth, height=self.scObj.dims.windowHeight)
        self.maxsize(width=self.scObj.dims.windowWidth, height=self.scObj.dims.windowHeight)
        self.state('zoomed')


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
        self.topToolbar.grid(row=0, sticky="nsew", ipadx=self.scObj.dims.topToolbarPadX, ipady=self.scObj.dims.topToolbarPadY)
        self.mainContent.grid(row=1, sticky="nsew", ipadx=self.scObj.dims.mainContentPadX, ipady=self.scObj.dims.mainContentPadY)
        self.bottomToolbar.grid(row=2, sticky="nsew", ipadx=self.scObj.dims.bottomToolbarPadX,
                                ipady=self.scObj.dims.bottomToolbarPadY)
        self.bottomInfobar.grid(row=3, sticky="nsew", ipadx=self.scObj.dims.bottomInfobarPadX,
                                ipady=self.scObj.dims.bottomInfobarPadY)
        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []


        # FRAMES WHICH ARE CHILDREN OF self.mainContent
        # Defines the 3 container frames within Main Content: Images Frame, Controls Frame, and Right Frame
        # TODO: Rename Right Frame to something more meaningful
        self.imagesFrame = tkinter.ttk.Frame(self.mainContent, width=self.scObj.dims.imagesFrameWidth)
        self.controlsFrame = tkinter.ttk.Frame(self.mainContent)
        # NOTE: Instead of hard-coding the width of rightFrame, can set it relative to controlsFrame by removing the
        #       explicit width definition and calling grid_columnconfigure() for BOTH columns 1 AND 2
        # TODO: Consider implementing the above NOTE
        self.rightFrame = tkinter.ttk.Frame(self.mainContent, width=self.scObj.dims.rightFrameWidth)

        # Specifies that mainContent's row 0 (the only row) and column 1 (Controls Frame) have priority for space-filling
        self.mainContent.grid_rowconfigure(0, weight=1)
        self.mainContent.grid_columnconfigure(1, weight=1)

        # Populates templist with the newly defined frames
        tempList = [self.imagesFrame, self.controlsFrame, self.rightFrame]
        # Iterates through the newly-defined tempList, appending all values to the relevant widget lists
        for e in tempList:
            self.widgets.append(e)
            self.frames.append(e)

        # In this case because each element has separate values for padding, the current DimensionContainer framework
        # does not support iteratively calling the ttk.Frame.grid() method for the newly created frames
        # So we arrange each of the three column containers manually
        self.imagesFrame.grid(row=0, column=0, sticky="nsew", ipadx=self.scObj.dims.imagesFramePadX,
                              ipady=self.scObj.dims.imagesFramePadY)
        self.controlsFrame.grid(row=0, column=1, sticky="nsew", ipadx=self.scObj.dims.controlsFramePadX,
                               ipady=self.scObj.dims.controlsFramePadY)
        self.rightFrame.grid(row=0, column=2, sticky="nsw", ipadx=self.scObj.dims.rightFramePadX,
                             ipady=self.scObj.dims.rightFramePadY)

        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []


        # FRAMES WHICH ARE CHILDREN OF self.imagesFrame
        # Defines the individual image display frames within the Images Frame
        self.imageFrameTL = tkinter.ttk.Frame(self.imagesFrame, width=self.scObj.dims.imageFrameWidth,
                                          height=self.scObj.dims.imageFrameHeight)
        self.imageFrameTR = tkinter.ttk.Frame(self.imagesFrame, width=self.scObj.dims.imageFrameWidth,
                                          height=self.scObj.dims.imageFrameHeight)
        self.imageFrameBL = tkinter.ttk.Frame(self.imagesFrame, width=self.scObj.dims.imageFrameWidth,
                                          height=self.scObj.dims.imageFrameHeight)
        self.imageFrameBR = tkinter.ttk.Frame(self.imagesFrame, width=self.scObj.dims.imageFrameWidth,
                                          height=self.scObj.dims.imageFrameHeight)

        # Specifies that each row and column within the Images Frame has equal priority for space-filling
        self.imagesFrame.grid_rowconfigure(0, weight=1)
        self.imagesFrame.grid_columnconfigure(0, weight=1)
        self.imagesFrame.grid_rowconfigure(1, weight=1)
        self.imagesFrame.grid_columnconfigure(1, weight=1)

        # Populates templist with the newly defined frames
        tempList = [self.imageFrameTL, self.imageFrameTR, self.imageFrameBL, self.imageFrameBR]
        # Iterates through the newly-defined tempList, appending all values to the relevant widget lists
        # THIS INCLUDES self.imagesFrameFrames and it's important to keep this in mind!
        # Also arranges the grid elements, making use of getGridPos() from hypnic_helpers.py
        # e is the Frame object within tempList and i is the index of that object
        for i, e in enumerate(tempList):
            self.widgets.append(e)
            self.frames.append(e)
            # imagesFrame has 2 rows and 2 columns
            pos = getGridPos(i, 2, 2)
            e.grid(row=pos[0], column=pos[1], sticky="nsew", ipadx=self.scObj.dims.imageFramePadX,
                   ipady=self.scObj.dims.imageFramePadY)

        # In this case because each element has separate values for row/column, I originally wrote the grid arrangement
        #   code in a non-iterative fashion. Keeping this down here just in case.
        """
        # TODO: Remove eventually, as it's now being done iteratively
        self.imageFrameTL.grid(row=0, column=0, sticky="nsew", ipadx=self.scObj.dims.imageFramePadX,
                               ipady=self.scObj.dims.imageFramePadY)
        self.imageFrameTR.grid(row=0, column=1, sticky="nsew", ipadx=self.scObj.dims.imageFramePadX,
                               ipady=self.scObj.dims.imageFramePadY)
        self.imageFrameBL.grid(row=1, column=0, sticky="nsew", ipadx=self.scObj.dims.imageFramePadX,
                               ipady=self.scObj.dims.imageFramePadY)
        self.imageFrameBR.grid(row=1, column=1, sticky="nsew", ipadx=self.scObj.dims.imageFramePadX,
                               ipady=self.scObj.dims.imageFramePadY)
        # Adds the frames to self.frames
        self.frames.append(self.imageFrameTL)
        self.frames.append(self.imageFrameTR)
        self.frames.append(self.imageFrameBL)
        self.frames.append(self.imageFrameBR)
        """


        # FRAMES WHICH ARE CHILDREN OF self.controlsFrame
        # Defines the individual control frames as rows within self.controlsFrame
        # These are not stored as directly-callable member variables but instead exist within their own list.
        #   This list, self.controlsFrames, is an even-more-specific list maintained IN ADDITION TO the other relevant
        #   lists like self.frames as opposed to being a replacement


    # Colors the frames defined in self.defineGrid()
    def colorFrames(self):
        for f in range(len(self.frames)):
            self.frames[f].configure(style=self.scObj.frameStyles[f])


    # Fills the previously-defined GUI with label elements
    def fillGrid(self):
        # tempList is a temporary list used to store elements which will be appended to member variable lists which
        #   contain relevant ttk objects such as self.labels, self.imageLabels, self.buttonWidgets, etc.
        # This is being done as a best practice for code readability as things can get ugly when dealing with appends
        #   to more than just one of the member variable lists
        tempList = []

        # Places widgets within the top toolbar

        # Places widgets within the bottom toolbar

        # Places widgets within the bottom infobar

        # Defines image Labels for each imageFrame of the imagesFrame
        self.imageLabelTL = tkinter.ttk.Label(self.imageFrameTL, image=self.img.tkImages[0])
        self.imageLabelTR = tkinter.ttk.Label(self.imageFrameTR, image=self.img.tkImages[1])
        self.imageLabelBL = tkinter.ttk.Label(self.imageFrameBL, image=self.img.tkImages[2])
        self.imageLabelBR = tkinter.ttk.Label(self.imageFrameBR, image=self.img.tkImages[3])
        # Populates templist with the newly defined labels
        tempList = [self.imageLabelTL, self.imageLabelTR, self.imageLabelBL, self.imageLabelBR]
        # Iterates through the newly-defined tempList, appending all values to the relevant widget lists
        # as well as carrying out the ttk.Label.place() method on each element
        for e in tempList:
            self.widgets.append(e)
            self.labels.append(e)
            self.imageLabels.append(e)
            e.place(relx=0.5, rely=0.5, anchor=CENTER)
        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []

        # Old manual non-array method being stored here temporarily
        # I don't think either will be used in the future but want to save both
        """
        self.imageLabelTL.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelTR.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelBL.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelBR.place(relx=0.5, rely=0.5, anchor=CENTER)
        """



        # Places widgets within the controls frame
        # BUTTONS:
        self.buttonUndo = tkinter.ttk.Button(self.controlsFrame, text="Undo")
        self.buttonApply = tkinter.ttk.Button(self.controlsFrame, text="Apply")
        self.buttonSave = tkinter.ttk.Button(self.controlsFrame, text="Save")
        # Populates templist with the newly defined buttons
        tempList = [self.buttonUndo, self.buttonApply, self.buttonSave]
        # Iterates through the newly-defined tempList, appending all values to both self.labels and self.imageLabels
        # as well as carrying out the ttk.Label.place() method on each element
        for e in tempList:
            self.widgets.append(e)
            self.buttonWidgets.append(e)
            self.inputWidgets.append(e)

            # TODO: Remove this random placement, it's only present for testing
            import random
            xFac = random.randint(2,8) / 10.0
            yFac = random.randint(2,8) / 10.0
            e.place(relx=xFac, rely=yFac, anchor=CENTER)

        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []

        # TODO: Remove the 4 lines below, they're only here for testing purposes
        self.imageLabelTL.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.imageLabelTR.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.imageLabelBL.place(relx=0.4, rely=0.6, anchor=CENTER)
        self.imageLabelBR.place(relx=0.6, rely=0.6, anchor=CENTER)

    # Sets the necessary style parameters for each ttk-specific widget
    def styleWidgets(self):
        print("PLACEHOLDER FOR CONTENT WITHIN THE HypnicGUI.styleWidgets() function")
