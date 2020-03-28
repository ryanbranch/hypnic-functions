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

        # This function holds the DimensionContainer object instance, "dims",
        # in order to access things like padding specification variables
        self.dims = dimension_container.DimensionContainer()
        # This function also
        self.ttkStyles = ttk.Style()

        self.ttkStyleConfig()

    def ttkStyleConfig(self):

        # DEFAULT STYLES
        # TButton represents the default ttk Button (the class name for ttk::button is TButton)
        self.ttkStyles.configure("TButton",
                                 padding=self.dims.internalPaddingButton,
                                 relief="flat",
                                 background="#555")

        self.ttkStyles.configure("TFrame",
                                    background="#115")
        self.ttkStyles.configure("TLabelFrame",
                                    background="#ccc")
        self.ttkStyles.configure("TLabel",
                                    background="#ccc")

        # SPECIFIC STYLES
        # C.TButton represents a colored ttk Button
        self.ttkStyles.map("C.TButton",
                           foreground=[('pressed', 'red'), ('active', 'blue')],
                           background=[('pressed', '!disabled', 'black'), ('active', 'white')])