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

    def __init__(self):

        # M E M B E R     V A R I A B L E S

        # TIMERS
        # Timer beginning upon initialization of ni object
        self.initTimer = default_timer()
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]
