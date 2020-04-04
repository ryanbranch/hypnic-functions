# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. Read the following: "Control variables: the values behind the widgets"
#    1. Link: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/control-variables.html

# Library Imports
import tkinter
from tkinter import ttk

__name__ = "state_container"

class StateContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    def __init__(self, gui_):

        # So that the StyleContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        # Initializes (and sets default values, if applicable) for tkinter control variables
        # Variables beginning with "ra" signify a variable controlled by radiobuttons
        # Variables beginning with "ch" signify a variable controlled by a checkbox
        # Variables beginning with "co" signify a variable controlled by a combobox

        # Temporary variables being used for test purposes TODO: REMOVE THESE (Everything in this block until END TODO)
        self.chIntVar0 = tkinter.IntVar()
        self.chIntVar1 = tkinter.IntVar()
        self.chIntVar2 = tkinter.IntVar()
        self.chIntVar3 = tkinter.IntVar()
        self.chIntVar4 = tkinter.IntVar()
        self.chIntVar5 = tkinter.IntVar()
        self.chIntVar6 = tkinter.IntVar()
        self.chIntVar7 = tkinter.IntVar()
        self.chIntVar8 = tkinter.IntVar()
        self.chIntVar9 = tkinter.IntVar()

        self.chIntVars = []
        self.numChIntVars = 30  # FLAG: Hard-coded GUI parameter!
        for i in range(self.numChIntVars):
            self.chIntVars.append(tkinter.IntVar())
            self.chIntVars[-1].set(i)

        # END TODO: Above this is the content that needs to be removed



        # Variables with actual planned functionality (anything below this line)
        self.raOutputImage = tkinter.IntVar()
        self.raOutputImage.set(0)
        self.raPrimaryInputImage = tkinter.IntVar()
        self.raPrimaryInputImage.set(0)
        self.raSecondaryInputImage = tkinter.IntVar()
        self.raSecondaryInputImage.set(1)
        self.raTertiaryInputImage = tkinter.IntVar()
        self.raTertiaryInputImage.set(2)
        self.raManipType = tkinter.IntVar()
        self.raManipType.set(-1)
        self.chWrapColors = tkinter.IntVar()
        self.chWrapColors.set(1)
        self.chRedChannel = tkinter.IntVar()
        self.chRedChannel.set(1)
        self.chGreenChannel = tkinter.IntVar()
        self.chGreenChannel.set(1)
        self.chBlueChannel = tkinter.IntVar()
        self.chBlueChannel.set(1)
        self.coPrimaryOutputImage = tkinter.IntVar()
        self.coPrimaryOutputImage.set(0)
        self.coPrimaryInputImage = tkinter.IntVar()
        self.coPrimaryInputImage.set(0)
        self.coSecondaryInputImage = tkinter.IntVar()
        self.coSecondaryInputImage.set(0)
        self.coTertiaryInputImage = tkinter.IntVar()
        self.coTertiaryInputImage.set(0)

        self.chTest = tkinter.IntVar()
        self.chTest.set(0)
