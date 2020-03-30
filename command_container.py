# TODO:
#  ==============================================================================
#  S. When it comes to image manipulation operations, determine the most streamlined way of doing things that
#       prioritizes a low number of file read/write operations and a low number of object __init__()/__del__() calls
#  ==============================================================================
#  A. Placeholder

__name__ = "command_container"

# Library Imports
import random
import PIL
from pathlib import Path

# Local Imports
import hypnic_helpers

# G L O B A L   V A R I A B L E S
# DEFAULT STYLE PARAMETERS
DEFAULT_BG_COLOR = ""


class CommandContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    def __init__(self, gui_):

        # So that the CommandContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        # TODO: Consider creating a dictionary which pairs each command name to (an) associated lambda/partial value(s)

        # A list of the names of all command functions (excluding parenthesis and arguments)
        self.commandNames = []
        # A list of the names of commands which are associated with any button(s)
        self.buttonCommandNames = []
        # A list of the names of commands which are exclusive to one specific button
        # TODO: This is part of what makes me think that dicts with lambdas/partials make more sense
        #  EXAMPLE SCENARIO:
        #      A "save image" command exists, but the saved image depends on a parameter passed in
        #       - IF there are two discrete buttons like "Save Image 1", "Save Image 2") then each of these has a 1:1
        #         relationship w/ a specific function call (INCLUDING PARAMETERS), but not w/ the function name alone
        self.exclButtonCommandNames = []


    # Populates the commandNames lists
    def initializeCommandNames(self):
        print("Executing CommandContainer.initializeCommandNames()")
        return self.commandNames


    # C O M M A N D     F U N C T I O N S
    # Functions beginning with "cmd" are designated for use in the "command" parameter of applicable ttk objects
    #   COMMAND FUNCTION REFERENCE
    #    - To update an image (tk Image) after editing the associated image (PIL Image)
    #    -   NOTE: MUST BE DONE BEFORE CONFIGURING THIS TK IMAGE TO BE UPDATED/ASSIGNED ON A GIVEN GUI LABEL
    #        CODE: self.gui.img.tkImages[index] = PIL.ImageTk.PhotoImage(image=self.gui.img.pilImages[0])
    #    - To change the image (tk Image) assigned to a given GUI label:
    #    -   NOTE: AFTER EDITING A PIL IMAGE, MUST UPDATE THE tkIMAGE BEFORE CONFIGURING LABEL CONTENTS
    #        CODE: self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[0])
    #    - To place an image Label (ttk Label w/ image)
    #        - If place() has already been called on the object before, empty parameters will preserve existing values
    #        CODE: self.gui.photoBoxImageLabels[0].place(relx=0.5, rely=0.5, anchor=self.gui.dims.defaultPlaceAnchor)
    #    - To save an image (PIL Image) to a file
    #        CODE: self.gui.img.pilImages[0].save(Path("string_representing/path_including/folders_and/file.extension"))

    # Test function used during development to ensure that commands are working
    # Has a parameter variable, inVar, which can be specified by the widget with this command using partial()
    def cmdDefault(self, inVar = None):
        print("Executing CommandContainer.cmdDefault() with inVar:  " + str(inVar))
        return inVar

    # Called when the "Undo" button is pressed
    def cmdButtonUndo(self):
        print("Executing CommandContainer.cmdButtonUndo()")
        self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[1].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[2].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[3].configure(image=self.gui.img.tkImages[0])
        return 1

    # Called when the "Apply" button is pressed
    def cmdButtonApply(self):
        print("Executing CommandContainer.cmdButtonApply()")
        self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[2])
        self.gui.photoBoxImageLabels[1].configure(image=self.gui.img.tkImages[2])
        self.gui.photoBoxImageLabels[2].configure(image=self.gui.img.tkImages[2])
        self.gui.photoBoxImageLabels[3].configure(image=self.gui.img.tkImages[2])
        return 2

    # Called when the "Save" button is pressed
    def cmdButtonSave(self):
        print("Executing CommandContainer.cmdButtonSave()")

        # Iterates through each image within the pilImages list of the ImageContainer class
        # NOTE: Currently all of this code is based on the fact that the only images in this program are the 4 images
        #       displayed in the photoBox Frames. Loading more images in ImageContainer may temporarily break this.
        for index, pilImage in enumerate(self.gui.img.pilImages):
            print("IMAGE " + str(index))
            # Loads the PIL Image for editing
            # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
            pixels = pilImage.load()

            # The X and Y resolutions of the current element within ImageContainer.pilImages
            xRes = pilImage.size[0]
            yRes = pilImage.size[1]
            # Iterates through each row and column of the image, manipulating pixels accordingly
            for row in range(yRes):
                for col in range(xRes):
                    if random.randint(0, 3) == 1:
                        pixels[col, row] = hypnic_helpers.getRandomRGB()
            # Updates the relevant ImageTk PhotoImage
            # TODO: Consider shifting responsibility to ImageContainer so that we can avoid
            #         using PIL for anything in the CommandComtainer class
            self.gui.img.tkImages[index] = PIL.ImageTk.PhotoImage(image=pilImage)
            # Reconfigures the relevant image Label
            self.gui.photoBoxImageLabels[index].configure(image=self.gui.img.tkImages[index])

        return 3