# TODO:
#  A. Implement functionalities which result from changes in focus between frames
#  B. Add member variable arrays to HypnicGUI which store the grid, frame, label objects in a dictionary
#  C. Keys should be strings like "topToolbar", "imageFrameTR", etc.
#    1. Don't have to write code to support SOLELY managing the objects via list operations
#    2. But should still support it for keeping code clean and for using list operations WHERE REASONABLE.
#  D. Consider creating a new widget_container.py file
#    1. Not immediately necessary, but the GUI is gonna become more and more complicated so it may make more sense
#       to handle initialization-related aspects of the program within a class
#    2. A WidgetContainer object would likely hold the StyleContainer instance (which itself holds a DimensionContainer)

__name__ = "hypnic_gui"

# Library Inputs
import tkinter
from tkinter import CENTER, ttk

# Local Inputs
import dimension_container
import image_container
import style_container

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
        # Stores all of the ttk Frame objects that belong to the GUI
        # Any time a Frame is created, it should be placed in this list to support iteration
        self.frames = []
        # Stores all of the ttk Label objects that belong to the GUI
        # Any time a Label is created, it should be placed in this list to support iteration
        self.labels = []
        # Stores specifically the ttk Label objects which have an assigned image property
        # NOTE: If a Label doe not contain an image but is developed for the ability to contain one, include it in here
        self.imageLabels = []
        # Stores specifically the ttk Label objects which have some assigned text property
        # NOTE: If a Label doe not inherently/immediately contain text but is developed to contain it, include it
        # TODO: Determine whether textvariable Label objects should also be included within the array for text Labels,
        #       and/or vice versa, or kept mutually exclusive from one another
        self.textLabels = []
        # Stores specifically the ttk Label objects which have some assigned textvariable property
        # NOTE: If a Label doe not contain a textvariable but is developed to potentially contain it, include it
        self.textvariableLabels = []
        # Stores specifically the ttk BUTTON objects
        self.buttonWidgets = []
        # Stores specifically the ttk INPUT-RELATED widget instances.
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

        # self.img should be the ONLY ImageContainer instance!
        # TODO: Replace INPUT_IMAGE_PATHS_FILE with runtime user input, the entire reason it's passed in by the GUI
        self.img = image_container.ImageContainer(INPUT_IMAGE_PATHS_FILE)



        self.iconbitmap(default='media/hficon.ico')
        self.wm_title("hypnic-functions GUI Client")
        #self.minsize(width=self.scObj.dims.windowWidth, height=self.scObj.dims.windowHeight)
        self.maxsize(width=self.scObj.dims.windowWidth, height=self.scObj.dims.windowHeight)
        self.state('zoomed')


        self.defineGrid()
        self.colorFrames()
        self.fillGrid()
        self.styleWidgets()

    # Defines the GUI layout using tkinter's grid() and Frame() modules
    def defineGrid(self):

        # Defines the main 4 containers: Top Toolbar, Main Content, Bottom Toolbar, and Bottom Infobar
        self.topToolbar = tkinter.ttk.Frame(self, height=self.scObj.dims.topToolbarHeight)
        self.mainContent = tkinter.ttk.Frame(self)
        self.bottomToolbar = tkinter.ttk.Frame(self, height=self.scObj.dims.bottomToolbarHeight)
        self.bottomInfobar = tkinter.ttk.Frame(self, height=self.scObj.dims.bottomInfobarHeight)
        # Specifies that row 1 (Main Content) and column 0 (the only column) have priority for space-filling
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Arranges the 4 main containers
        self.topToolbar.grid(row=0, sticky="nsew", ipadx=self.scObj.dims.topToolbarPadX, ipady=self.scObj.dims.topToolbarPadY)
        self.mainContent.grid(row=1, sticky="nsew", ipadx=self.scObj.dims.mainContentPadX, ipady=self.scObj.dims.mainContentPadY)
        self.bottomToolbar.grid(row=2, sticky="nsew", ipadx=self.scObj.dims.bottomToolbarPadX,
                                ipady=self.scObj.dims.bottomToolbarPadY)
        self.bottomInfobar.grid(row=3, sticky="nsew", ipadx=self.scObj.dims.bottomInfobarPadX,
                                ipady=self.scObj.dims.bottomInfobarPadY)
        # Adds the frames to self.frames
        self.frames.append(self.topToolbar)
        self.frames.append(self.mainContent)
        self.frames.append(self.bottomToolbar)
        self.frames.append(self.bottomInfobar)



        # Defines the 2 containers within Main Content: Images Frame and Control Frame
        self.imagesFrame = tkinter.ttk.Frame(self.mainContent, width=self.scObj.dims.imagesFrameWidth)
        self.controlFrame = tkinter.ttk.Frame(self.mainContent)
        # Specifies that mainContent's row 0 (the only row) and column 1 (Control Frame) have priority for space-filling
        self.mainContent.grid_rowconfigure(0, weight=1)
        self.mainContent.grid_columnconfigure(1, weight=1)
        # Arranges the Images Frame and Control Frame
        self.imagesFrame.grid(row=0, column=0, sticky="nsew", ipadx=self.scObj.dims.imagesFramePadX,
                              ipady=self.scObj.dims.imagesFramePadY)
        self.controlFrame.grid(row=0, column=1, sticky="nsew", ipadx=self.scObj.dims.controlFramePadX,
                               ipady=self.scObj.dims.controlFramePadY)
        # Adds the frames to self.frames
        self.frames.append(self.imagesFrame)
        self.frames.append(self.controlFrame)



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
        # Arranges the individual image display frames
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
        tempList = [self.imageLabelTL, self.imageLabelTR, self.imageLabelBL, self.imageLabelBR]
        # Iterates through the newly-defined tempList, appending all values to the relevant widget lists
        # as well as carrying out the ttk.Label.place() method on each element
        for e in tempList:
            self.widgets.append(e)
            self.labels.append(e)
            self.imageLabels.append(e)
            e.place(relx=0.5, rely=0.5, anchor=CENTER)
        # NOTE: Clearing tempList just in case!
        # TODO: If clearing IS important, consider using
        #           del tempList[:]
        #       But don't jump to conclusions on doing so. Don't want to accidentally call any destructors for ttk
        #       objects and such since many will be referenced by two or more lists
        tempList = []

        # Old manual non-array method being stored here temporarily
        # I don't think either will be used in the future but want to save both
        """
        self.imageLabelTL.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelTR.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelBL.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelBR.place(relx=0.5, rely=0.5, anchor=CENTER)
        """



        # Places widgets within the control frame
        # BUTTONS:
        self.buttonManipulate = tkinter.ttk.Button(self.controlFrame, text="Manipulate")
        self.buttonRevert = tkinter.ttk.Button(self.controlFrame, text="Revert")
        self.buttonApply = tkinter.ttk.Button(self.controlFrame, text="Apply")
        self.buttonAdvance = tkinter.ttk.Button(self.controlFrame, text="Advance")
        tempList = [self.buttonManipulate, self.buttonRevert, self.buttonApply, self.buttonAdvance]
        # Iterates through the newly-defined tempList, appending all values to both self.labels and self.imageLabels
        # as well as carrying out the ttk.Label.place() method on each element
        for e in tempList:
            self.widgets.append(e)
            self.buttonWidgets.append(e)
            self.inputWidgets.append(e)

            import random
            xFac = random.randint(2,8) / 10.0
            yFac = random.randint(2,8) / 10.0
            e.place(relx=xFac, rely=yFac, anchor=CENTER)
        # NOTE: Clearing tempList just in case!
        # TODO: If clearing IS important, consider using
        #           del tempList[:]
        #       But don't jump to conclusions on doing so. Don't want to accidentally call any destructors for ttk
        #       objects and such since many will be referenced by two or more lists
        tempList = []



        self.imageLabelTL.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.imageLabelTR.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.imageLabelBL.place(relx=0.4, rely=0.6, anchor=CENTER)
        self.imageLabelBR.place(relx=0.6, rely=0.6, anchor=CENTER)

    # Sets the necessary style parameters for each ttk-specific widget
    def styleWidgets(self):
        print("PLACEHOLDER FOR CONTENT WITHIN THE HypnicGUI.styleWidgets() function")
