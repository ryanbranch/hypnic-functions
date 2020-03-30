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
        # A list of booleans describing whether each image (within the 4 Photo Box labels) is a candidate for a "Redo"
        # Initialized as all False, because a Redo can't be performed if an Undo has not yet been performed
        self.canRedo = [False, False, False, False]  # FLAG: Hard-coded GUI parameter!


    # Populates the commandNames lists
    def initializeCommandNames(self):
        print("Executing CommandContainer.initializeCommandNames()")
        return self.commandNames


    # C O M M A N D     F U N C T I O N S
    # COMMAND FUNCTION NOTES
    #  - Functions beginning with "cmd" are designated for use in the "command" parameter of applicable ttk objects
    #  - First parameter for relevant cmd functions should be an integer, "i", representing Photo Box index
    #      - This should be given a default value of 0 in the function definition, in case the call doesn't provide one
    # COMMAND FUNCTION REFERENCE
    #  - To update an image (tk Image) after editing the associated image (PIL Image)
    #  -   NOTE: MUST BE DONE BEFORE CONFIGURING THIS TK IMAGE TO BE UPDATED/ASSIGNED ON A GIVEN GUI LABEL
    #      CODE: self.gui.img.tkImages[index] = PIL.ImageTk.PhotoImage(image=self.gui.img.pilImages[0])
    #  - To change the image (tk Image) assigned to a given GUI label:
    #  -   NOTE: AFTER EDITING A PIL IMAGE, MUST UPDATE THE tkIMAGE BEFORE CONFIGURING LABEL CONTENTS
    #      CODE: self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[0])
    #  - To place an image Label (ttk Label w/ image)
    #      - If place() has already been called on the object before, empty parameters will preserve existing values
    #      CODE: self.gui.photoBoxImageLabels[0].place(relx=0.5, rely=0.5, anchor=self.gui.dims.defaultPlaceAnchor)
    #  - To save an image (PIL Image) to a file
    #      CODE: self.gui.img.pilImages[0].save(Path("string_representing/path_including/folders_and/file.extension"))

    # Test function used during development to ensure that commands are working
    def cmdDefault(self, i=0):
        print("Executing CommandContainer.cmdDefault() with i = " + str(i))
        return i


    # Called when the "Load" button is pressed
    def cmdButtonLoad(self, i=0):
        print("Executing CommandContainer.cmdButtonLoad() with i = " + str(i))
        return i

    # Called when the "Save" button is pressed
    def cmdButtonSave(self, i=0):
        print("Executing CommandContainer.cmdButtonSave() with i = " + str(i))
        return i

    # Called when the "Undo" button is pressed
    # FOR NOW, Undo will simply revert to the most recent image saved
    # TODO: allow undo to revert back through a chain of previously saved images
    def cmdButtonUndo(self, i=0):
        print("Executing CommandContainer.cmdButtonUndo() with i = " + str(i))
        # TODO: Remove this old content which is being temporarily saved in the block comment below
        """
        self.gui.photoBoxImageLabels[0].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[1].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[2].configure(image=self.gui.img.tkImages[0])
        self.gui.photoBoxImageLabels[3].configure(image=self.gui.img.tkImages[0])
        """
        return i

    # Called when the "Redo" button is pressed
    # FOR NOW, Redo will switch back to whatever was shown right before the last "Undo" call for that image
    # TODO: allow redo to revert back through chains longer than a single Undo operation
    def cmdButtonRedo(self, i=0):
        print("Executing CommandContainer.cmdButtonRedo() with i = " + str(i))
        return i

    # Called when the "Apply" button is pressed
    def cmdButtonApply(self, i=0):
        print("Executing CommandContainer.cmdButtonApply() with i = " + str(i))
        # Loads the PIL Image for editing
        # TODO: Look into PIL Image methods like load() and close(), test whether file saving+loading is needed, etc
        pixels = self.gui.img.pilImages[i].load()
        # The X and Y resolutions of the current element within ImageContainer.pilImages
        xRes = self.gui.img.pilImages[i].size[0]
        yRes = self.gui.img.pilImages[i].size[1]
        # Iterates through each row and column of the image, manipulating pixels accordingly
        for row in range(yRes):
            for col in range(xRes):
                if random.randint(0, 3) == 1:
                    pixels[col, row] = hypnic_helpers.getRandomRGB()
        # Updates the relevant ImageTk PhotoImage
        # TODO: Consider shifting responsibility to ImageContainer so that we can avoid
        #         using PIL for anything in the CommandComtainer class
        self.gui.img.tkImages[i] = PIL.ImageTk.PhotoImage(image=self.gui.img.pilImages[i])
        # Reconfigures the relevant image Label
        self.gui.photoBoxImageLabels[i].configure(image=self.gui.img.tkImages[i])