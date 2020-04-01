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

        # Temporary variables being used for test purposes TODO: REMOVE THESE (Everything in this block until END TODO)
        self.raIntVar0 = tkinter.IntVar()
        self.raIntVar1 = tkinter.IntVar()
        self.raIntVar2 = tkinter.IntVar()
        self.raIntVar3 = tkinter.IntVar()
        self.raIntVar4 = tkinter.IntVar()
        self.raIntVar5 = tkinter.IntVar()
        self.raIntVar6 = tkinter.IntVar()
        self.raIntVar7 = tkinter.IntVar()
        self.raIntVar8 = tkinter.IntVar()
        self.raIntVar9 = tkinter.IntVar()

        self.raIntVars = []
        self.raIntVars = [self.raIntVar0,
                          self.raIntVar1,
                          self.raIntVar2,
                          self.raIntVar3,
                          self.raIntVar4,
                          self.raIntVar5,
                          self.raIntVar6,
                          self.raIntVar7,
                          self.raIntVar8,
                          self.raIntVar9]
        for i, v in enumerate(self.raIntVars):
            v.set(i)
        # END TODO: Above this is the content that needs to be removed



        # Variables with actual planned functionality (anything below this line)
        self.raOutputImage = tkinter.IntVar()
        self.raOutputImage.set(0)
        self.raPrimaryInputImage = tkinter.IntVar()
        self.raPrimaryInputImage.set(0)
        self.raSecondaryInputImage = tkinter.IntVar()
        self.raSecondaryInputImage.set(1)
        self.raManipType = tkinter.StringVar()
        self.raManipType.set("randomizePixelColors")
        self.chTest = tkinter.IntVar()
        self.chTest.set(0)

