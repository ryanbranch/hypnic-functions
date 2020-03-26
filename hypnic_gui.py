__name__ = "hypnic_gui"

import tkinter
from tkinter import ttk

import dimension_container

class HypnicGUI(tkinter.Tk):

    def __init__(self, wrapperRef, *args, **kwargs):
        # Begins by running the initialization function for the basic instance of tkinter.Tk
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.dims = dimension_container.DimensionContainer()
        self.wrapper = wrapperRef

        self.iconbitmap(default='media/hficon.ico')
        self.wm_title("hypnic-functions GUI Client")
        self.minsize(width=self.dims.windowWidth, height=self.dims.windowHeight)
        self.maxsize(width=self.dims.windowWidth, height=self.dims.windowHeight)
        self.state('zoomed')

        self.defineGrid()

    def defineGrid(self):
        # create all of the main containers
        topToolbar = tkinter.Frame(self, bg='cyan', height=self.dims.topToolbarHeight)
        mainContent = tkinter.Frame(self, bg='purple')
        bottomToolbar = tkinter.Frame(self, bg='white', height=self.dims.bottomToolbarHeight)
        bottomInfobar = tkinter.Frame(self, bg='lavender', height=self.dims.bottomInfobarHeight)
        # TODO: Remove the line below
        print(self.dims.topToolbarHeight)

        # layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        topToolbar.grid(row=0, sticky="nsew", ipadx=self.dims.topToolbarPadX, ipady=self.dims.topToolbarPadY)
        mainContent.grid(row=1, sticky="nsew", ipadx=self.dims.mainContentPadX, ipady=self.dims.mainContentPadY)
        bottomToolbar.grid(row=2, sticky="nsew", ipadx=self.dims.bottomToolbarPadX, ipady=self.dims.bottomToolbarPadY)
        bottomInfobar.grid(row=3, sticky="nsew", ipadx=self.dims.bottomInfobarPadX, ipady=self.dims.bottomInfobarPadY)

        """
        # create the widgets for the top frame
        model_label = Label(topToolbar, text='Model Dimensions')
        width_label = Label(topToolbar, text='Width:')
        length_label = Label(topToolbar, text='Length:')
        entry_W = Entry(topToolbar, background="pink")
        entry_L = Entry(topToolbar, background="orange")

        # layout the widgets in the top frame
        model_label.grid(row=0, columnspan=3)
        width_label.grid(row=1, column=0)
        length_label.grid(row=1, column=2)
        entry_W.grid(row=1, column=1)
        entry_L.grid(row=1, column=3)
        """

        # create the center widgets
        mainContent.grid_rowconfigure(0, weight=1)
        mainContent.grid_columnconfigure(1, weight=1)

        imagesFrame = tkinter.Frame(mainContent, bg='blue', width=self.dims.imagesFrameWidth)
        # TODO: Remove this line below
        print(self.dims.imagesFrameWidth)
        controlFrame = tkinter.Frame(mainContent, bg='green')

        imagesFrame.grid(row=0, column=0, sticky="ns", ipadx=self.dims.imagesFramePadX, ipady=self.dims.imagesFramePadY)
        controlFrame.grid(row=0, column=1, sticky="nsew", ipadx=self.dims.controlFramePadX,
                          ipady=self.dims.controlFramePadY)

        # create the photo display widgets within imagesFrame
        imagesFrame.grid_rowconfigure(0, weight=1)
        imagesFrame.grid_columnconfigure(0, weight=1)
        imagesFrame.grid_rowconfigure(1, weight=1)
        imagesFrame.grid_columnconfigure(1, weight=1)

        imageFrameTL = tkinter.Frame(imagesFrame, bg='red', width=self.dims.imageFrameWidth,
                                     height=self.dims.imageFrameHeight)
        imageFrameTR = tkinter.Frame(imagesFrame, bg='pink', width=self.dims.imageFrameWidth,
                                     height=self.dims.imageFrameHeight)
        imageFrameBL = tkinter.Frame(imagesFrame, bg='orange', width=self.dims.imageFrameWidth,
                                     height=self.dims.imageFrameHeight)
        imageFrameBR = tkinter.Frame(imagesFrame, bg='yellow', width=self.dims.imageFrameWidth,
                                     height=self.dims.imageFrameHeight)

        imageFrameTL.grid(row=0, column=0, sticky="ns", ipadx=self.dims.imageFramePadX, ipady=self.dims.imageFramePadY)
        imageFrameTR.grid(row=0, column=1, sticky="ns", ipadx=self.dims.imageFramePadX, ipady=self.dims.imageFramePadY)
        imageFrameBL.grid(row=1, column=0, sticky="ns", ipadx=self.dims.imageFramePadX, ipady=self.dims.imageFramePadY)
        imageFrameBR.grid(row=1, column=1, sticky="ns", ipadx=self.dims.imageFramePadX, ipady=self.dims.imageFramePadY)
