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
        norm = normal_math_timing.NormalMathTiming(self.gui, self)
        numb = numba_math_timing.NumbaMathTiming(self.gui, self)

        # End-of-Function calls

        norm.defineCurrentImage(0)  # F FLAG: Hard-coded parameter

        # Subimage-Related
        norm.subImageCoordinates = [[100, 100], [110, 110]]
        norm.createNewSubImage()
        norm.modifySubImage((102, 97), (115, 106))
        norm.modifySubImage((103, 98), (114, 105))
        norm.modifySubImage((102, 97), (115, 106))
