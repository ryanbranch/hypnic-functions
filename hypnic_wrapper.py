# TODO:
#  A. Placeholder

__name__ = "hypnic_wrapper"

# Library Inputs
import random

# Local Inputs
import hypnic_gui

class HypnicWrapper():

    def __init__(self):
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
