# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. Placeholder

__name__ = "command_container"

# Library Imports
import random
import tkinter
from tkinter import ttk

# Local Imports
import dimension_container
import hypnic_helpers

# G L O B A L   V A R I A B L E S
# DEFAULT STYLE PARAMETERS
DEFAULT_BG_COLOR = ""


class CommandContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    def __init__(self, gui_):

        # So that the CommandContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        # TODO: Consider creating a dictionary which pairs each command name to (an) associated lambda/partial value(s)

        # A list of the names of all command functions (excluding parenthesis and arguments)
        self.commandNames = []
        # A list of the names of commands which are associated with any button(s)
        self.buttonCommandNames = []
        # A list of the names of commands which are exclusive to one specific button
        # TODO: This is part of what makes me think that dicts with lambdas/partials make more sense
        #  EXAMPLE SCENARIO:
        #      A "save image" command exists, but the saved image depends on a parameter passed in
        #       - IF there are two discrete buttons like "Save Image 1", "Save Image 2") then each of these has a 1:1
        #         relationship w/ a specific function call (INCLUDING PARAMETERS), but not w/ the function name alone
        self.exclButtonCommandNames = []


    # Populates the commandNames lists
    def initializeCommandNames(self):
        print("Executing CommandContainer.initializeCommandNames()")
        return self.commandNames


    # COMMAND FUNCTIONS
    # Functions beginning with "cmd" are designated for use in the "command" parameter of applicable ttk objects

    # Test function used during development to ensure that commands are working
    # Has a parameter variable, inVar, which can be specified by the widget with this command using partial()
    def cmdDefault(self, inVar = None):
        print("Executing CommandContainer.cmdDefault() with inVar:  " + str(inVar))
        return inVar

    # Called when the "Undo" button is pressed
    def cmdButtonUndo(self):
        print("Executing CommandContainer.cmdButtonUndo()")
        self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[1].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[2].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[3].configure(image=self.gui.img.tkImages[0])
        return 1

    # Called when the "Apply" button is pressed
    def cmdButtonApply(self):
        print("Executing CommandContainer.cmdButtonApply()")
        self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[2])
        self.gui.photoBoxImageLabels[1].configure(image=self.gui.img.tkImages[2])
        self.gui.photoBoxImageLabels[2].configure(image=self.gui.img.tkImages[2])
        self.gui.photoBoxImageLabels[3].configure(image=self.gui.img.tkImages[2])
        return 2

    # Called when the "Save" button is pressed
    def cmdButtonSave(self):
        print("Executing CommandContainer.cmdButtonSave()")
        return 3