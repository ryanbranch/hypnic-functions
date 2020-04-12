# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. PLACEHOLDER

__name__ = "numba_math_timing"

# Library Imports
import numba
from timeit import default_timer
import tkinter
import PIL
from PIL import Image, ImageTk
from pathlib import Path
import math

class NumbaMathTiming():

    def __init__(self, gui_, tc_):

        # M E M B E R     V A R I A B L E S

        # INITIALIZATION TIMER
        # Timer beginning upon initialization of this object
        self.initTimer = default_timer()

        # GUI Reference
        self.gui = gui_
        # TimingContainer Reference
        self.tc = tc_

        # OTHER TIMERS
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]
