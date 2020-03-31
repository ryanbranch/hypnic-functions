# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. Placeholder

__name__ = "state_container"

class StateContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    def __init__(self, gui_):

        # So that the StyleContainer instance can refer to the HypnicGUI instance
        self.gui = gui_
