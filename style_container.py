# TODO:
#  A. Placeholder

__name__ = "style_container"

# Library Imports
import random
import tkinter
from tkinter import ttk

# Local Imports
import dimension_container
from hypnic_helpers import *

# G L O B A L   V A R I A B L E S
# DEFAULT STYLE PARAMETERS
DEFAULT_BG_COLOR = ""


class StyleContainer():

    def __init__(self):
        # This class holds the DimensionContainer object instance, "dims",
        # in order to access things like padding specification variables. It is initialized here
        self.dims = dimension_container.DimensionContainer()

        # This class also holds the ttk Style object, which can be referenced from the HypnicGUI instance if needed
        self.ttkStyleObj = ttk.Style()
        # Sets the ttk theme
        # TODO: Change this, I'm only making it Win-XP because I think that'll make it stand out whether it's having an effect
        #print(self.ttkStyleObj.theme_names())
        #print(self.ttkStyleObj.theme_use())
        self.ttkStyleObj.theme_use("xpnative")

        # A list of strings which are the names of custom styles
        # Any time a custom style is defined with the ttk.style.map() method, it should be stored
        self.styles = []
        # A list of strings which specifically refer to ttk Frame-related styles
        self.frameStyles = []
        # A list of strings which specifically refer to ttk Label-related styles
        self.labelStyles = []
        # A list of strings which specifically refer to styles for ttk IMAGE Labels
        self.imageLabelStyles = []
        # A list of strings which specifically refer to styles for ttk BUTTON Labels
        self.buttonWidgetStyles = []
        # A list of strings which specifically refer to styles for ttk TEXT Labels
        self.textLabelStyles = []
        # A list of strings which specifically refer to styles for the ttk INPUT-RELATED Label styles
        # NOTE: This *CAN* include styles for things like Button Label objects,
        #       despite the fact that Button styles have their own wider-scoped list
        self.inputWidgetStyles = []

        # Defines and configures the GUI's ttk styles
        self.ttkStyleConfig()

    def ttkStyleConfig(self):
        # DEFAULT STYLES
        # These styles will apply to all relevant ttk widgets which are not given a custom style
        # TButton represents the default ttk Button (the class name for ttk::button is TButton)
        self.ttkStyleObj.configure("TButton",
                                   padding=self.dims.internalPaddingButton,
                                   relief="flat",
                                   background="#555")
        # TFrame : ttk.Frame
        self.ttkStyleObj.configure("TFrame",
                                   background="#16B")
        # TLabelFrame : ttk.labelFrame
        self.ttkStyleObj.configure("TLabelFrame",
                                   background="#5AF")
        # TLabel : ttk.label
        self.ttkStyleObj.configure("TLabel",
                                   background="#9D3")

        # CUSTOM STYLES
        # Button Styles
        self.ttkStyleObj.configure("c.TButton",
                             foreground=[('pressed', 'red'), ('active', 'blue')],
                             background=[('pressed', '!disabled', 'black'), ('active', 'white')])

        # Frame Styles
        # Number of random ttk Frame styles to generate
        # TODO: Define this elsewhere, even better if based on parameters (hard-coded or user input)
        #  instead of being hard-coded in itself
        numFrameStyles = 20
        for i in range(numFrameStyles):
            # styleName values are "fs0.TFrame", "fs1.TFrame", etc
            styleName = ("fs" + str(i) + ".TFrame")
            # Configures a style object, with key styleName, using random RGB values for each color
            self.ttkStyleObj.configure(styleName, background=rgbToHex(getRandomBlue()))

            # Adds styleName to self.frameStyles for future reference
            self.frameStyles.append(styleName)
            print(styleName)

    # SET / GET METHODS
    # Good practice for use when modifying StyleContainer variables from externally (like from the HypnicGUI instance)
    # Also good for clarity when pulling/calculating values from here to the GUI instance
    # TODO: It's not great practice that I'm calling len() to find the number of elements in an array instead of
    #  tracking the length in a member variable. As long as I only call len() once per function below I'm not too
    #  concerned about it, however in the future it would be good to change how I'm handling this

    #frame, label, buttonlabel, imagelabel, inputlabel

    # Returns a random element from self.styles
    def getRandomStyle(self):
        return self.styles[random.randrange(0, len(self.styles))]

    # Returns a random element from self.frameStyles
    def getRandomFrameStyle(self):
        return self.frameStyles[random.randrange(0, len(self.frameStyles))]

    # Returns a random element from self.labelStyles
    def getRandomLabelStyle(self):
        return self.labelStyles[random.randrange(0, len(self.labelStyles))]

    # Returns a random element from self.buttonWidgetStyles
    def getRandomButtonWidgetStyle(self):
        return self.buttonWidgetStyles[random.randrange(0, len(self.buttonWidgetStyles))]

    # Returns a random element from self.imageLabelStyles
    def getRandomButtonWidgetStyle(self):
        return self.imageLabelStyles[random.randrange(0, len(self.imageLabelStyles))]

    # Returns a random element from self.buttonWidgetStyles
    def getRandomButtonWidgetStyle(self):
        return self.inputWidgetStyles[random.randrange(0, len(self.inputWidgetStyles))]

