__name__ = "hypnic_gui"

import tkinter
from tkinter import ttk

import dimension_container
import image_container


class HypnicGUI(tkinter.Tk):

    def __init__(self, wrapperRef, *args, **kwargs):
        # Begins by running the initialization function for the basic instance of tkinter.Tk
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.dims = dimension_container.DimensionContainer()
        self.img = image_container.ImageContainer()
        self.wrapper = wrapperRef

        self.iconbitmap(default='media/hficon.ico')
        self.wm_title("hypnic-functions GUI Client")
        self.minsize(width=self.dims.windowWidth, height=self.dims.windowHeight)
        self.maxsize(width=self.dims.windowWidth, height=self.dims.windowHeight)
        self.state('zoomed')

        self.defineGrid()
        self.fillGrid()

    # Defines the GUI layout using tkinter's grid() and Frame() modules
    def defineGrid(self):
        # Defines the main 4 containers: Top Toolbar, Main Content, Bottom Toolbar, and Bottom Infobar
        self.topToolbar = tkinter.Frame(self, bg='cyan', height=self.dims.topToolbarHeight)
        self.mainContent = tkinter.Frame(self, bg='purple')
        self.bottomToolbar = tkinter.Frame(self, bg='white', height=self.dims.bottomToolbarHeight)
        self.bottomInfobar = tkinter.Frame(self, bg='lavender', height=self.dims.bottomInfobarHeight)
        # Specifies that row 1 (Main Content) and column 0 (the only column) have priority for space-filling
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Arranges the 4 main containers
        self.topToolbar.grid(row=0, sticky="nsew", ipadx=self.dims.topToolbarPadX, ipady=self.dims.topToolbarPadY)
        self.mainContent.grid(row=1, sticky="nsew", ipadx=self.dims.mainContentPadX, ipady=self.dims.mainContentPadY)
        self.bottomToolbar.grid(row=2, sticky="nsew", ipadx=self.dims.bottomToolbarPadX,
                                ipady=self.dims.bottomToolbarPadY)
        self.bottomInfobar.grid(row=3, sticky="nsew", ipadx=self.dims.bottomInfobarPadX,
                                ipady=self.dims.bottomInfobarPadY)

        # Defines the 2 containers within Main Content: Images Frame and Control Frame
        self.imagesFrame = tkinter.Frame(self.mainContent, bg='blue', width=self.dims.imagesFrameWidth)
        self.controlFrame = tkinter.Frame(self.mainContent, bg='green')
        # Specifies that mainContent's row 0 (the only row) and column 1 (Control Frame) have priority for space-filling
        self.mainContent.grid_rowconfigure(0, weight=1)
        self.mainContent.grid_columnconfigure(1, weight=1)
        # Arranges the Images Frame and Control Frame
        self.imagesFrame.grid(row=0, column=0, sticky="nsew", ipadx=self.dims.imagesFramePadX,
                              ipady=self.dims.imagesFramePadY)
        self.controlFrame.grid(row=0, column=1, sticky="nsew", ipadx=self.dims.controlFramePadX,
                               ipady=self.dims.controlFramePadY)

        # Defines the individual image display frames within the Images Frame
        self.imageFrameTL = tkinter.Frame(self.imagesFrame, bg='red', width=self.dims.imageFrameWidth,
                                          height=self.dims.imageFrameHeight)
        self.imageFrameTR = tkinter.Frame(self.imagesFrame, bg='pink', width=self.dims.imageFrameWidth,
                                          height=self.dims.imageFrameHeight)
        self.imageFrameBL = tkinter.Frame(self.imagesFrame, bg='orange', width=self.dims.imageFrameWidth,
                                          height=self.dims.imageFrameHeight)
        self.imageFrameBR = tkinter.Frame(self.imagesFrame, bg='yellow', width=self.dims.imageFrameWidth,
                                          height=self.dims.imageFrameHeight)
        # Specifies that each row and column within the Images Frame has equal priority for space-filling
        self.imagesFrame.grid_rowconfigure(0, weight=1)
        self.imagesFrame.grid_columnconfigure(0, weight=1)
        self.imagesFrame.grid_rowconfigure(1, weight=1)
        self.imagesFrame.grid_columnconfigure(1, weight=1)
        # Ensures that the individual image display frames do not shrink, in either dimension, to fit their images
        # NOTE: THIS DOESN'T SEEM TO HELP
        # TODO: FIX THIS!
        self.imageFrameTL.grid_propagate(False)
        self.imageFrameTR.grid_propagate(False)
        self.imageFrameBL.grid_propagate(False)
        self.imageFrameBR.grid_propagate(False)
        self.grid_propagate(0)
        # Arranges the individual image display frames
        self.imageFrameTL.grid(row=0, column=0, sticky="nsew", ipadx=self.dims.imageFramePadX,
                               ipady=self.dims.imageFramePadY)
        self.imageFrameTR.grid(row=0, column=1, sticky="nsew", ipadx=self.dims.imageFramePadX,
                               ipady=self.dims.imageFramePadY)
        self.imageFrameBL.grid(row=1, column=0, sticky="nsew", ipadx=self.dims.imageFramePadX,
                               ipady=self.dims.imageFramePadY)
        self.imageFrameBR.grid(row=1, column=1, sticky="nsew", ipadx=self.dims.imageFramePadX,
                               ipady=self.dims.imageFramePadY)

    # Fills the previously-defined GUI with label elements
    def fillGrid(self):
        self.imageLabelTL = tkinter.Label(self.imageFrameTL, image=self.img.tkImage1)
        self.imageLabelTR = tkinter.Label(self.imageFrameTR, image=self.img.tkImage2)
        self.imageLabelBL = tkinter.Label(self.imageFrameBL, image=self.img.tkImage3)
        self.imageLabelBR = tkinter.Label(self.imageFrameBR, image=self.img.tkImage4)
        self.imageLabelTL.pack()
        self.imageLabelTR.pack()
        self.imageLabelBL.pack()
        self.imageLabelBR.pack()
