# TODO:
#  A. Placeholder

__name__ = "hypnic_wrapper"

# Library Inputs
from timeit import default_timer
import random

# Local Inputs
import hypnic_gui

class HypnicWrapper():

    def __init__(self):

        # M E M B E R     V A R I A B L E S

        # INITIALIZATION TIMER
        # Timer beginning upon initialization of this object
        self.initTimer = default_timer()

        # OTHER TIMERS
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]

        self.gui = hypnic_gui.HypnicGUI(self)

def main():

    # Seeds the random number generator
    random.seed(333)

    # Creates and launches the GUI instance
    app = HypnicWrapper()
    app.gui.mainloop()

    # Post-run operations (garbage collection, etc.)
    del app.gui.img

main()
