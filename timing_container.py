# TODO:
#  ==============================================================================
#  S. Immediately after adding initialization timers to all of the major classes in this project, I noticed a change
#     in load times. I can't tell whether the overall time from launch to END of GUI display has been affected,
#     but there is noticeable increase in lag time between launch and when the GUI window first appears
#  ==============================================================================
#  A. PLACEHOLDER

__name__ = "timing_container"

# Library Imports
from timeit import default_timer
import math

# Local Imports
import normal_math_timing
import numba_math_timing

class TimingContainer():

    def __init__(self, gui_):

        # M E M B E R     V A R I A B L E S

        # INITIALIZATION TIMER
        # Timer beginning upon initialization of this object
        self.initTimer = default_timer()

        # GUI Reference
        self.gui = gui_

        # OTHER TIMERS
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]

        # Timing Test Objects
        self.norm = normal_math_timing.NormalMathTiming(self.gui, self)
        self.numb = numba_math_timing.NumbaMathTiming(self.gui, self)

        # End-of-Function calls

        self.norm.defineCurrentImage()  # F FLAG: Hard-coded parameter

        # Subimage-Related
        self.norm.subImageCoordinates = [[1, 1], [8, 8]]
        self.norm.createNewSubImage()
        self.norm.modifySubImage((0, 0), (9, 9))
        self.norm.modifySubImage((4, 4), (4, 4))
        self.norm.modifySubImage((1, 4), (6, 4))
