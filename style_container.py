# TODO:
#  A. Placeholder

__name__ = "style_container"

import tkinter
from tkinter import CENTER, ttk

# Local Imports
import dimension_container
from hypnic_helpers import rgbTupleToHex

# G L O B A L   V A R I A B L E S
# DEFAULT STYLE PARAMETERS
DEFAULT_BG_COLOR = ""

class StyleContainer():

    def __init__(self):

        # This function accesses hypnic_gui's DimensionContainer object instance, "dims",
        # in order to access things like padding specification variables
        dimsRef_ = 0
        self.dimsRef = dimsRef_

        self.dims = dimension_container.DimensionContainer()

        self.ttkStyles = ttk.Style()

    def ttkStyleConfig(self):
        # This if/else is just a placeholder until I actually implement style configuration
        if True:
            print()
        else:
            # DEFAULT STYLES
            # TButton represents the default ttk Button (the class name for ttk::button is TButton)

            self.ttkStyles.configure("TButton", padding=self.dimsRef.internalPaddingButton)

            # SPECIFIC STYLES

            self.ttkStyles.map()