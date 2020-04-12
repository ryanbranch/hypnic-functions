# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
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

    def __init__(self):

        # M E M B E R     V A R I A B L E S

        # TIMERS
        # Timer beginning upon initialization of ni object
        self.initTimer = default_timer()
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]

        # Timing Test Objects
        norm = normal_math_timing.NormalMathTiming()
        numb = numba_math_timing.NumbaMathTiming()

        # End-of-Function calls

        norm.defineCurrentImage(0)  # F FLAG: Hard-coded parameter

        # Subimage-Related
        norm.subImageCoordinates = [[100, 100], [110, 110]]
        norm.createNewSubImage()
        norm.modifySubImage((102, 97), (115, 106))
        norm.modifySubImage((103, 98), (114, 105))
        norm.modifySubImage((102, 97), (115, 106))
