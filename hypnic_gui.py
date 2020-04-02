# TODO:
#  ==============================================================================
#  S. STRONGLY CONSIDER instance vs. class member variables and improve abstraction (as currently in D.)
#     Explanation: https://dev.to/ogwurujohnson/distinguishing-instance-variables-from-class-variables-in-python-81
#  ==============================================================================
#  A. Consider creating a new widget_container.py file (or some other name with similar meaning)
#    1. Not immediately necessary, but the GUI is gonna become more and more complicated so it may make more sense
#       to handle initialization-related aspects of the program within a class
#  B. It's REALLY not great practice that I'm initializing member variables like frames outside of __init__()
#    1. Would be better to, at that point within defineGrid(), initialize a WidgetContainer() instance which holds
#         those widgets as member variables AND defines them within its __init__ function
#  C. If clearing IS important, consider using
#             del tempList[:]
#         But don't jump to conclusions on doing so
#    1. Don't want to accidentally call any destructors for ttk objects and such,
#       since many will be referenced by two or more lists
#  D. Create a TXT or CSV input system for defining all of the GUI parameters that are currently hard-coded
#    1. Not at all concerned with this until I actually care about making things pretty beyond functionality

__name__ = "hypnic_gui"

# Library Inputs
import tkinter
from tkinter import CENTER, ttk
# The partial() module can be used to allow widgets like Buttons to pass arguments along with their commands
# It is specifically useful where lambda can't be applied, like when such a parameter is being periodically changed
#   throughout some sort of iterative process, such as configuring commands within the controlBox Frames
# Credit to StackOverflow users "Dologan" and "Klamer Schutte" for their answer and associated comments on its use
# The answer can be viewed at https://stackoverflow.com/a/22290388
from functools import partial

# Local Inputs
import dimension_container
import state_container
import image_container
import style_container
import edit_container
import command_container
import hypnic_helpers

# G L O B A L   V A R I A B L E S
# Path to the text document which lists the paths to all input images
# TODO: Remove this global and define it from user input at runtime
INPUT_IMAGE_PATHS_FILE = "hypnic_images.txt"  # FLAG: Hard-coded GUI parameter!


class HypnicGUI(tkinter.Tk):

    # Constructor has a wrapper_ argument for the program's HypnicWrapper instance
    def __init__(self, wrapper_, *args, **kwargs):

        # The HypnicGUI instance can refer to the HypnicWrapper instance
        # TODO: Since I'm writing all of these classes for use as single instances, it amy make the most
        #       sense to transition such member variables to "above" the __init__()
        self.wrapper = wrapper_

        # Begins by running the initialization function for the basic instance of tkinter.Tk
        tkinter.Tk.__init__(self, *args, **kwargs)

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
        self.frames = []

        # CUSTOM FRAME LISTS (mainly for storing frames which do not have their own individual member variables)
        #     - Also potentially useful for keeping narrow-scope groups of similar frames together
        # self.photoBoxFrames stores each of the 4 frames held within self.photoBox
        self.photoBoxFrames = []

        # self.controlBoxFrames stores each frame from each row within self.controlBox
        self.controlBoxFrames = []

        # I N I T I A L I Z A T I O N     O F     L A B E L - R E L A T E D     V A R I A B L E S
        # GENERAL LABEL LIST
        # Stores all of the ttk Label objects that belong to the GUI
        self.labels = []

        # SPECIFIC LABEL LISTS
        # Divides labels into separate lists based on whether or not they contain associated images or text

        # Stores  the ttk Label objects which have an assigned image property
        self.imageLabels = []
        # Stores  the ttk Label objects which have some assigned text property
        # TODO: Determine whether textvariable Label objects should also be included within the array for text Labels,
        #       and/or vice versa, or kept mutually exclusive from one another
        self.textLabels = []
        # Stores  the ttk Label objects which have some assigned textvariable property
        self.textvariableLabels = []

        # CUSTOM LABEL LISTS
        # self.photoBoxImageLabels stores each of the 4 Labels which hold images for each of the 4 "photoBox*" frames
        self.photoBoxImageLabels = []

        # I N I T I A L I Z A T I O N     O F     B U T T O N - R E L A T E D     V A R I A B L E S
        # GENERAL BUTTON LIST
        # Stores all of the ttk Button objects that belong to the GUI
        self.buttons = []

        # CUSTOM BUTTON LISTS
        # Stores each of the buttons that fall within any of the Control Box frames in CenterContent
        self.controlBoxButtons = []

        # I N I T I A L I Z A T I O N     O F    R A D I O B U T T O N - R E L A T E D     V A R I A B L E S
        # GENERAL RADIOBUTTON LIST
        # Stores all of the ttk Radiobutton objects that belong to the GUI
        self.radiobuttons = []

        # CUSTOM RADIOBUTTON LISTS
        # Stores each of the Radiobuttons that fall within any of the Control Box frames in CenterContent
        self.controlBoxRadiobuttons = []

        # I N I T I A L I Z A T I O N     O F    C H E C K B U T T O N - R E L A T E D     V A R I A B L E S
        # GENERAL CHECKBUTTON LIST
        # Stores all of the ttk Checkbutton objects that belong to the GUI
        self.checkbuttons = []

        # CUSTOM CHECKBUTTON LISTS
        # Stores each of the Checkbuttons that fall within any of the Control Box frames in CenterContent
        self.controlBoxCheckbuttons = []



        # C O N T A I N E R     C L A S S     I N I T I A L I Z A T I O N
        # NOTE: THIS SHOULD ONLY BE DONE AFTER DEFINING THE EMPTY LISTS ABOVE, JUST IN CASE A CONSTRUCTOR NEEDS ACCESS

        # StyleContainer.__init__() depends on self.dims so we must define self.dims before self.styleObj!
        self.dims = dimension_container.DimensionContainer(self)
        self.stateObj = state_container.StateContainer(self)
        # StyleContainer.__init__() depends on self.dims so self.dims MUST be initialized already!
        self.styleObj = style_container.StyleContainer(self)
        self.edit = edit_container.EditContainer(self)
        # TODO: Replace INPUT_IMAGE_PATHS_FILE with runtime user input, the entire reason it's passed in by the GUI
        self.img = image_container.ImageContainer(self, INPUT_IMAGE_PATHS_FILE)
        # Depends on a variety of things having already been defined, including dimensions and images
        #  - For this reason, it's probably best to keep CommandContainer last in the instantiation order
        self.cmd = command_container.CommandContainer(self)


        # C O N F I G U R I N G     A D D I T I O N A L     G U I     P R O P E R T I E S

        # It's completely fine for these to be hard-coded as it's not anything the user should have or need control over
        self.iconbitmap(default='media/hficon.ico')
        self.wm_title("hypnic-functions GUI Client")
        # NOTE: The line below can be uncommented in order to force a specific set of window dimensions
        # self.minsize(width=self.dims.windowWidth, height=self.dims.windowHeight)
        self.maxsize(width=self.dims.windowWidth, height=self.dims.windowHeight)
        self.state('zoomed')

        # Calls functions related to constructing the GUI and initializes associated values
        # The following must be done before calling defineGrid():
        self.defineGrid()
        # The following must be done before calling colorFrames():
        self.colorFrames()
        # The following must be done before calling fillGrid():
        self.fillGrid()
        # The following must be done before calling styleWidgets():
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
        self.topToolbar = tkinter.ttk.Frame(self, height=self.dims.topToolbarHeight)
        self.mainContent = tkinter.ttk.Frame(self)
        self.bottomToolbar = tkinter.ttk.Frame(self, height=self.dims.bottomToolbarHeight)
        self.bottomInfobar = tkinter.ttk.Frame(self, height=self.dims.bottomInfobarHeight)

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
        self.topToolbar.grid(row=0, sticky="nsew", ipadx=self.dims.topToolbarPadX,
                             ipady=self.dims.topToolbarPadY)
        self.mainContent.grid(row=1, sticky="nsew", ipadx=self.dims.mainContentPadX,
                              ipady=self.dims.mainContentPadY)
        self.bottomToolbar.grid(row=2, sticky="nsew", ipadx=self.dims.bottomToolbarPadX,
                                ipady=self.dims.bottomToolbarPadY)
        self.bottomInfobar.grid(row=3, sticky="nsew", ipadx=self.dims.bottomInfobarPadX,
                                ipady=self.dims.bottomInfobarPadY)
        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []


        # FRAMES WHICH ARE CHILDREN OF self.mainContent
        # Defines the 3 container frames within Main Content: Left Content, Center Content, and Right Content
        self.leftContent = tkinter.ttk.Frame(self.mainContent, width=self.dims.leftContentWidth)
        self.centerContent = tkinter.ttk.Frame(self.mainContent)
        # NOTE: Instead of hard-coding the width of rightContent, can set it relative to centerContent by removing the
        #       explicit width definition and calling grid_columnconfigure() for BOTH columns 1 AND 2
        # TODO: Consider implementing the above NOTE
        self.rightContent = tkinter.ttk.Frame(self.mainContent, width=self.dims.rightContentWidth)

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
        self.leftContent.grid(row=0, column=0, sticky="nsew", ipadx=self.dims.leftContentPadX,
                              ipady=self.dims.leftContentPadY)
        self.centerContent.grid(row=0, column=1, sticky="nsew", ipadx=self.dims.centerContentPadX,
                                ipady=self.dims.centerContentPadY)
        self.rightContent.grid(row=0, column=2, sticky="nsw", ipadx=self.dims.rightContentPadX,
                               ipady=self.dims.rightContentPadY)

        # NOTE: Clearing tempList just in case!
        # TODO: See note at top of file about clearing tempList
        tempList = []


        # FRAMES WHICH ARE CHILDREN OF self.leftContent
        # Defines the individual image display frames within the Left Content
        self.photoBoxTL = tkinter.ttk.Frame(self.leftContent, width=self.dims.photoBoxWidth,
                                            height=self.dims.photoBoxHeight)
        self.photoBoxTR = tkinter.ttk.Frame(self.leftContent, width=self.dims.photoBoxWidth,
                                            height=self.dims.photoBoxHeight)
        self.photoBoxBL = tkinter.ttk.Frame(self.leftContent, width=self.dims.photoBoxWidth,
                                            height=self.dims.photoBoxHeight)
        self.photoBoxBR = tkinter.ttk.Frame(self.leftContent, width=self.dims.photoBoxWidth,
                                            height=self.dims.photoBoxHeight)

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
            e.grid(row=pos[0], column=pos[1], sticky="nsew", ipadx=self.dims.photoBoxPadX,
                   ipady=self.dims.photoBoxPadY)


        # FRAMES WHICH ARE CHILDREN OF self.centerContent
        # Defines the individual control frames as rows within self.centerContent
        # These are not stored as directly-callable member variables but instead exist within their own list.
        #   This list, self.centerContents, is an even-more-specific list maintained IN ADDITION TO the other relevant
        #   lists like self.frames as opposed to being a replacement

        # Iterates through the number of rows and columns specified within dimension_container.py
        for r in range(self.dims.numControlBoxRows):
            for c in range(self.dims.numControlBoxCols):
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
                self.widgets[-1].grid(row=r, column=c, sticky="nsew", ipadx=self.dims.controlBoxPadX,
                                      ipady=self.dims.controlBoxPadY)


    # Colors the frames defined in self.defineGrid()
    # NOTE: Currently based on random generation because I'm not concerned about this aspect of things
    def colorFrames(self):
        for f in range(len(self.frames)):
            self.frames[f].configure(style=self.styleObj.frameStyles[f])

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
        self.fillPhotoBoxImages()
        #  - WIDGETS IN CENTER CONTENT
        #    - WIDGETS IN CONTROL BOX FRAMES
        self.fillControlBoxButtons()
        self.fillControlBoxRadiobuttons()
        self.fillControlBoxCheckbuttons()


    # Defines images for each of the 4 Photo Box Frames within leftContent
    def fillPhotoBoxImages(self):
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
            self.widgets[-1].place(relx=self.dims.defaultLabelPlaceRelX,
                                   rely=self.dims.defaultLabelPlaceRelY,
                                   anchor=self.dims.defaultLabelPlaceAnchor)


    # Defines buttons for each controlBox within centerContent
    def fillControlBoxButtons(self):

        # iterates from zero stopping before (number of rows multiplied by number of columns)
        for i in range(self.dims.numControlBoxRows * self.dims.numControlBoxCols):
            # Number of buttons created is defined by DimensionContainer.numControlBoxButtons
            buttonCount = self.dims.defaultControlBoxButtonCount
            if i < len(self.dims.controlBoxButtonCounts):
                buttonCount = self.dims.controlBoxButtonCounts[i]
            for n in range(buttonCount):
                # Initializes (and appends to self.widgets) a new Button with the relevant self.controlBoxFrames elt as parent
                # TODO: I BELIEVE that my appending to a member variable which was initialized in __init__, all of those
                #       Frame entities should continue to exist indefinitely. But if I run into problems, this very
                #       well could be the cause and I'll have to learn more about memory management in Python OOP
                self.widgets.append(tkinter.ttk.Button(self.controlBoxFrames[i]))
                # Appends the same Button to self.buttons, self.inputWidgets, and self.controlBoxButtons
                self.buttons.append(self.widgets[-1])
                self.inputWidgets.append(self.widgets[-1])
                self.controlBoxButtons.append(self.widgets[-1])
                self.widgets[-1].grid(row=n, column=0, sticky="nsew", ipadx=self.dims.controlBoxPadX,
                   ipady=self.dims.controlBoxPadY)

                """
                # Places the Button within its frame
                self.widgets[-1].place(relx=self.dims.controlBoxButtonPlaceRelX,
                                       rely=((n + 1) / (buttonCount + 1)),
                                       anchor=self.dims.controlBoxButtonPlaceAnchor)
                """


        # CONFIGURING TEXT for each BUTTON in self.controlBoxButtons
        # Multiple properties can be changed with a single call of configure(), but I'm often
        #   keeping things separate because this content is later going to be split up between many functions
        # For the time being, if I want to set human-defined button text within the code I could create a list where
        #   each element is a string and the number of elements is equal to the number of buttons, etc.
        # TODO: Either use the variable below or get rid of it entirely
        # TODO: Actually consider making wider-scoped "buttonStrings"-type of list variables
        # Initialized as a list of empty strings, where length is equal to the number of cells in centerContent
        self.controlBoxButtonStrings = [""] * len(self.controlBoxButtons)
        # Manual definition of button text
        # NOTE: Doesn't really belong in this file at all, let alone here
        # TODO: Remedy the above note by storing button text information in a new file, likely another custom class
        self.controlBoxButtonStrings[0] = "Load A"
        self.controlBoxButtonStrings[1] = "Load B"
        self.controlBoxButtonStrings[2] = "Load C"
        self.controlBoxButtonStrings[3] = "Load D"

        self.controlBoxButtonStrings[4] = "Save A"
        self.controlBoxButtonStrings[5] = "Save B"
        self.controlBoxButtonStrings[6] = "Save C"
        self.controlBoxButtonStrings[7] = "Save D"

        self.controlBoxButtonStrings[8] = "Undo A"
        self.controlBoxButtonStrings[9] = "Undo B"
        self.controlBoxButtonStrings[10] = "Undo C"
        self.controlBoxButtonStrings[11] = "Undo D"

        self.controlBoxButtonStrings[12] = "Redo A"
        self.controlBoxButtonStrings[13] = "Redo B"
        self.controlBoxButtonStrings[14] = "Redo C"
        self.controlBoxButtonStrings[15] = "Redo D"

        self.controlBoxButtonStrings[16] = "Scale A"
        self.controlBoxButtonStrings[17] = "Scale B"
        self.controlBoxButtonStrings[18] = "Scale C"
        self.controlBoxButtonStrings[19] = "Scale D"

        self.controlBoxButtonStrings[20] = "Apply A"
        self.controlBoxButtonStrings[21] = "Apply B"
        self.controlBoxButtonStrings[22] = "Apply C"
        self.controlBoxButtonStrings[23] = "Apply D"


        # Sets any still-undefined strings to "Button [N]" where [N] is the current value of i
        # s is the string and i is the index of that string within self.controlBoxButtonStrings
        for i, s in enumerate(self.controlBoxButtonStrings):
            if s == "":
                self.controlBoxButtonStrings[i] = "Button " + str(i)

        # Uses the newly-completed list of strings to configure each item in self.controlBoxButtons
        for i, b in enumerate(self.controlBoxButtons):
            self.controlBoxButtons[i].configure(text=self.controlBoxButtonStrings[i])


        # CONFIGURING COMMANDS for each BUTTON in self.controlBoxButtons
        for i, b in enumerate(self.controlBoxButtons):
            b.configure(command=partial(self.cmd.cmdButtonDefault, i))

        # Overwrites with some custom commands
        self.controlBoxButtons[0].configure(command=partial(self.cmd.cmdButtonLoad, 0))
        self.controlBoxButtons[1].configure(command=partial(self.cmd.cmdButtonLoad, 1))
        self.controlBoxButtons[2].configure(command=partial(self.cmd.cmdButtonLoad, 2))
        self.controlBoxButtons[3].configure(command=partial(self.cmd.cmdButtonLoad, 3))
        self.controlBoxButtons[4].configure(command=partial(self.cmd.cmdButtonSave, 0))
        self.controlBoxButtons[5].configure(command=partial(self.cmd.cmdButtonSave, 1))
        self.controlBoxButtons[6].configure(command=partial(self.cmd.cmdButtonSave, 2))
        self.controlBoxButtons[7].configure(command=partial(self.cmd.cmdButtonSave, 3))
        self.controlBoxButtons[8].configure(command=partial(self.cmd.cmdButtonUndo, 0))
        self.controlBoxButtons[9].configure(command=partial(self.cmd.cmdButtonUndo, 1))
        self.controlBoxButtons[10].configure(command=partial(self.cmd.cmdButtonUndo, 2))
        self.controlBoxButtons[11].configure(command=partial(self.cmd.cmdButtonUndo, 3))
        self.controlBoxButtons[12].configure(command=partial(self.cmd.cmdButtonRedo, 0))
        self.controlBoxButtons[13].configure(command=partial(self.cmd.cmdButtonRedo, 1))
        self.controlBoxButtons[14].configure(command=partial(self.cmd.cmdButtonRedo, 2))
        self.controlBoxButtons[15].configure(command=partial(self.cmd.cmdButtonRedo, 3))
        self.controlBoxButtons[16].configure(command=partial(self.cmd.cmdButtonScale, 0))
        self.controlBoxButtons[17].configure(command=partial(self.cmd.cmdButtonScale, 1))
        self.controlBoxButtons[18].configure(command=partial(self.cmd.cmdButtonScale, 2))
        self.controlBoxButtons[19].configure(command=partial(self.cmd.cmdButtonScale, 3))
        # TODO: Update these so that the second argument isn't necessarily equal to the first
        #        - NOTE: This may involve reducing the number of arguments to cmdButtonApply() and instead specifying
        #                things like primary/secondary input image indices through radiobuttons
        self.controlBoxButtons[20].configure(command=partial(self.cmd.cmdButtonApply, 0))
        self.controlBoxButtons[21].configure(command=partial(self.cmd.cmdButtonApply, 1))
        self.controlBoxButtons[22].configure(command=partial(self.cmd.cmdButtonApply, 2))
        self.controlBoxButtons[23].configure(command=partial(self.cmd.cmdButtonApply, 3))


    # Defines Radiobuttons for each controlBox within centerContent
    def fillControlBoxRadiobuttons(self):

        # iterates from zero stopping before (number of rows multiplied by number of columns)
        for i in range(self.dims.numControlBoxRows * self.dims.numControlBoxCols):
            # Number of radiobuttons created is defined by DimensionContainer.numControlBoxRadiobuttons
            radiobuttonCount = self.dims.defaultControlBoxRadiobuttonCount
            if i < len(self.dims.controlBoxRadiobuttonCounts):
                radiobuttonCount = self.dims.controlBoxRadiobuttonCounts[i]
            for n in range(radiobuttonCount):
                # Initializes (and appends to self.widgets) a new Radiobutton with the relevant Frame as the parent
                self.widgets.append(tkinter.ttk.Radiobutton(self.controlBoxFrames[i]))
                # Appends the same Radiobutton to self.radiobuttons, self.inputWidgets, and self.controlBoxImageLabels
                self.radiobuttons.append(self.widgets[-1])
                self.inputWidgets.append(self.widgets[-1])
                self.controlBoxRadiobuttons.append(self.widgets[-1])
                # NOTE: A column value of 1 is used for Radiobuttons, as opposed to the 0 used for Buttons
                self.widgets[-1].grid(row=n, column=1, sticky="nsew", ipadx=self.dims.controlBoxPadX,
                                      ipady=self.dims.controlBoxPadY)

        # CONFIGURING TEXT for each RADIOBUTTON in self.controlBoxRadiobuttons
        # Initialized as a list of empty strings, where length is equal to the number of cells in centerContent
        self.controlBoxRadiobuttonStrings = [""] * len(self.controlBoxRadiobuttons)
        # Manual definition of radiobutton text
        # NOTE: Doesn't really belong in this file at all, let alone here
        # TODO: Remedy the above note by storing radiobutton text information in a new file, likely another custom class
        self.controlBoxRadiobuttonStrings[:10] = ["Snow",
                                                  "Grayscale",
                                                  "Add",
                                                  "Subtract",
                                                  "Function E",
                                                  "Function F",
                                                  "Function G",
                                                  "Function H",
                                                  "Function I",
                                                  "Function J"]
        self.controlBoxRadiobuttonStrings[10:14] = ["Primary A",
                                                    "Primary B",
                                                    "Primary C",
                                                    "Primary D",]
        self.controlBoxRadiobuttonStrings[14:18] = ["Secondary A",
                                                    "Secondary B",
                                                    "Secondary C",
                                                    "Secondary D", ]

        # Sets any still-undefined strings to "Radio [N]" where [N] is the current value of i
        # s is the string and i is the index of that string within self.controlBoxRadiobuttonStrings
        for i, s in enumerate(self.controlBoxRadiobuttonStrings):
            if s == "":
                self.controlBoxRadiobuttonStrings[i] = "Radio " + str(i)

        # Uses the newly-completed list of strings to configure each item in self.controlBoxRadiobuttons
        for i, b in enumerate(self.controlBoxRadiobuttons):
            b.configure(text=self.controlBoxRadiobuttonStrings[i])

        # CONFIGURING COMMANDS for each RADIOBUTTON in self.controlBoxRadiobuttons
        for i, b in enumerate(self.controlBoxRadiobuttons[:10]):
            b.configure(command=partial(self.cmd.cmdRadiobuttonSetManipType, i))

        # Configures state variables for some of the radiobuttons
        # Also attaches the variables to the widget reference objects, as described in the following reference:
        # http://effbot.org/tkinterbook/checkbutton.htm
        for i in range(10):
            self.controlBoxRadiobuttons[i].configure(variable=self.stateObj.raManipType, value=i)
            self.controlBoxRadiobuttons[i].var = self.stateObj.raManipType
        for i in range(10, 14):
            # NOTE: (i - 10) is inherently based on this hard-coded stuff. TODO: Clean up eventually
            self.controlBoxRadiobuttons[i].configure(variable=self.stateObj.raPrimaryInputImage, value=(i - 10))
            self.controlBoxRadiobuttons[i].var = self.stateObj.raPrimaryInputImage
        for i in range(14, 18):
            # NOTE: (i - 14) is inherently based on this hard-coded stuff. TODO: Clean up eventually
            self.controlBoxRadiobuttons[i].configure(variable=self.stateObj.raSecondaryInputImage, value=(i - 14))
            self.controlBoxRadiobuttons[i].var = self.stateObj.raSecondaryInputImage


    # Defines Checkbuttons for each controlBox within centerContent
    def fillControlBoxCheckbuttons(self):

        # iterates from zero stopping before (number of rows multiplied by number of columns)
        for i in range(self.dims.numControlBoxRows * self.dims.numControlBoxCols):
            # Number of checkbuttons created is defined by DimensionContainer.numControlBoxCheckbuttons
            checkbuttonCount = self.dims.defaultControlBoxCheckbuttonCount
            if i < len(self.dims.controlBoxCheckbuttonCounts):
                checkbuttonCount = self.dims.controlBoxCheckbuttonCounts[i]
            for n in range(checkbuttonCount):
                # Initializes (and appends to self.widgets) a new Checkbutton with the relevant Frame as the parent
                self.widgets.append(tkinter.ttk.Checkbutton(self.controlBoxFrames[i]))
                # Appends the same Checkbutton to self.checkbuttons, self.inputWidgets, and self.controlBoxImageLabels
                self.checkbuttons.append(self.widgets[-1])
                self.inputWidgets.append(self.widgets[-1])
                self.controlBoxCheckbuttons.append(self.widgets[-1])
                # NOTE: A column value of 2 is used for Checkbuttons, as opposed to the 1/0 used by Radio/Buttons
                self.widgets[-1].grid(row=n, column=2, sticky="nsew", ipadx=self.dims.controlBoxPadX,
                                      ipady=self.dims.controlBoxPadY)

        # CONFIGURING TEXT for each CHECKBUTTON in self.controlBoxCheckbuttons
        # Initialized as a list of empty strings, where length is equal to the number of cells in centerContent
        self.controlBoxCheckbuttonStrings = [""] * len(self.controlBoxCheckbuttons)
        # Manual definition of checkbutton text
        # NOTE: Doesn't really belong in this file at all, let alone here
        # TODO: Remedy the above note by storing checkbutton text information in a new file, likely another custom class
        for i in range(10):
            self.controlBoxCheckbuttonStrings[i] = "Check " + chr(65 + i)

        # Sets any still-undefined strings to "Check [N]" where [N] is the current value of i
        # s is the string and i is the index of that string within self.controlBoxCheckbuttonStrings
        for i, s in enumerate(self.controlBoxCheckbuttonStrings):
            if s == "":
                self.controlBoxCheckbuttonStrings[i] = "Check " + str(i)

        # Custom Checkbutton String definitions
        self.controlBoxCheckbuttonStrings[0] = "Wrap Colors"

        # Uses the newly-completed list of strings to configure text for each item in self.controlBoxCheckbuttons
        for i, b in enumerate(self.controlBoxCheckbuttons):
            b.configure(text=self.controlBoxCheckbuttonStrings[i])

        # Configures state variables for some of the checkbuttons
        # Also attaches the variables to the widget reference objects, as described in the following reference:
        # http://effbot.org/tkinterbook/checkbutton.htm
        #     NOTE: Be sure to use the get() method
        for i in range(10):
            self.controlBoxCheckbuttons[i].configure(variable=self.stateObj.chIntVars[i], onvalue=(2 ** i), offvalue=0)
            self.controlBoxCheckbuttons[i].var = self.stateObj.chIntVars[i]

        # CONFIGURING COMMANDS for each CHECKBUTTON in self.controlBoxCheckbuttons
        for i, b in enumerate(self.controlBoxCheckbuttons):
            b.configure(command=partial(self.cmd.cmdCheckbuttonDefault, i))

        # Custom Checkbutton Configurations
        self.controlBoxCheckbuttons[0].configure(variable=self.stateObj.chWrapColors, onvalue=1, offvalue=0)
        self.controlBoxCheckbuttons[0].var = self.stateObj.chWrapColors
        b.configure(command=partial(self.cmd.cmdCheckbuttonWrapColors, i))


    # Sets the necessary style parameters for each ttk-specific widget
    def styleWidgets(self):
        print("PLACEHOLDER FOR CONTENT WITHIN THE HypnicGUI.styleWidgets() function")
