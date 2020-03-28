# TODO:
#  A. Implement functionalities which result from changes in focus between frames
#  B. Add member variable arrays to HypnicGUI which store the grid, frame, label objects in a dictionary
#  C. Keys should be strings like "topToolbar", "imageFrameTR", etc.
#    1. Don't have to write code to support SOLELY managing the objects via list operations
#    2. But should still support it for keeping code clean and for using list operations WHERE REASONABLE.

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

        # Stores all of the ttk Frame objects that belong to the GUI
        # Any time a Frame is created, it should be placed in this list to support iteration
        self.frames = []
        # Stores all of the ttk Label objects that belong to the GUI
        # Any time a Label is created, it should be placed in this list to support iteration
        self.labels = []
        # Stores specifically the ttk IMAGE Label objects
        self.imageLabels = []
        # Stores specifically the ttk BUTTON Label objects
        self.buttonLabels = []
        # Stores specifically the ttk TEXT-RELATED Label objects
        self.textLabels = []
        # Stores specifically the ttk INPUT-RELATED Label objects.
        # NOTE: This *CAN* include button label objects for example, even though they have their own wider-scoped list
        self.inputLabels = []

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

        # Places widgets within the top toolbar

        # Places widgets within the bottom toolbar

        # Places widgets within the bottom infobar

        # Places images within each imageFrame of the imagesFrame
        self.imageLabelTL = tkinter.ttk.Label(self.imageFrameTL, image=self.img.tkImages[0])
        self.imageLabelTR = tkinter.ttk.Label(self.imageFrameTR, image=self.img.tkImages[1])
        self.imageLabelBL = tkinter.ttk.Label(self.imageFrameBL, image=self.img.tkImages[2])
        self.imageLabelBR = tkinter.ttk.Label(self.imageFrameBR, image=self.img.tkImages[3])
        self.imageLabelTL.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelTR.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelBL.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.imageLabelBR.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Adds the image labels to both the self.labels and self.imageLabels lists
        self.labels.append(self.imageLabelTL)
        self.labels.append(self.imageLabelTR)
        self.labels.append(self.imageLabelBL)
        self.labels.append(self.imageLabelBR)
        self.imageLabels.append(self.imageLabelTL)
        self.imageLabels.append(self.imageLabelTR)
        self.imageLabels.append(self.imageLabelBL)
        self.imageLabels.append(self.imageLabelBR)

        # Places widgets within the control frame

    # Sets the necessary style parameters for each ttk-specific widget
    def styleWidgets(self):
        print("PLACEHOLDER FOR CONTENT WITHIN THE HypnicGUI.styleWidgets() function")
