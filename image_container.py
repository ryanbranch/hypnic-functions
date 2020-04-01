# TODO:
#  ==============================================================================
#  S. Placeholder for the MOST IMPORTANT/URGENT TASK
#  ==============================================================================
#  A. Placeholder

__name__ = "image_container"

# Library Inputs
import PIL
from PIL import Image, ImageTk
from pathlib import Path

# G L O B A L   V A R I A B L E S
# Path to an image which is used by default when a desired image fails to load
STANDBY_IMAGE_PATH = "media/standby.jpg"

class ImageContainer():

    # Constructor has a gui_ parameter which is saved in self.gui in order to access the HypnicGUI members
    # Also has an imagesTxtPath parameter. Replacing this with runtime user input is a TODO with low priority
    def __init__(self, gui_, imagesTxtPath_):

        # So that the StyleContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        # Member variables related to input
        self.imagesTxtPath = imagesTxtPath_
        self.inputPaths = []
        # Array of booleans where a value of True denotes that the associated string within self.inputPaths is invalid
        # For the same indices at which self.missingFiles contains a value of True, the corresponding element within
        #   associated lists (e.g. self.pilImages and self.tkImages) are based on the standby image (STANDBY_IMAGE_PATH)
        self.missingFiles = []

        # Member variables related to output
        # NOTE: The idea of this (FLAG) being hard-coded is temporary. TODO: Switch to a more user-friendly approach
        self.outputImagePathStrings = ["media/output0.jpg",
                                       "media/output1.jpg",
                                       "media/output2.jpg",
                                       "media/output3.jpg"]
        # TODO: store the file extension (".jpg") part in a separate variable so that a "count suffix" can be appended

        # Object Storage
        # Array of PIL Image objects directly corresponding to the path strings in self.inputPaths
        self.pilImages = []
        # Array of PIL Tkinter PhotoImage objects directly corresponding to the path strings in self.inputPaths
        self.tkImages = []

        # PIL Image object used to temporarily hold a copy of an existing PIL image for editing
        self.pilImagesTemp = []

        # Loads images into memory
        self.getImages()


    # Builds the relevant lists of image objects and related data, based on a text file
    # Text file is defined by INPUT_IMAGE_PATHS_FILE, a global variable in hypnic_gui.py
    #   A low priority but easy TODO: remove the global and allow this to be user-defined at runtime
    # The formatting for the input text file is straightforward and its entire implementation is temporary, so I'm
    #   unworried about making this function too rigorous. However, file-parsing functionality will likely be useful in
    #   the future so I'm ensuring that the function can handle simple formatting discrepancies
    def getImages(self):
        # Exception handling ensures that the text file actually exists and can be opened
        try:
            # Opens the text file containing a list of images
            with open(self.imagesTxtPath) as f:
                # Creates and iterates through a list of strings (lines) from the document at self.imagesTxtPath
                for path in f.read().splitlines():
                    # Ignoring blank lines, appends each specified path to the self.inputPaths list
                    if path:
                        self.inputPaths.append(path)
        # Triggers when the open() operation fails
        except:
            # Console output for user
            print("================================================================")
            print("Failed to open text file list of input images.")
            print("Relevant Python file:                           image_container.py")
            print("Relevant function:                              ImageContainer.getImages()")
            print("Value of ImageContainer.imagesTxtPath variable: " + str(self.imagesTxtPath))
            print()
            # NOTE: This is currently an error bad enough to close the program, but shouldn't be in the future once I
            #       can allow users to specify input images at runtime
            exit(333)

        # Triggers if the file has been closed and no images were obtained
        # Not inherently a catastrophic error, but should raise red flags to the user
        if not self.inputPaths:
            # Console output for user
            print("================================================================")
            print("System could not parse any file paths from the image path definition text document.")
            print("Please ensure that the text document contains one file path per line.")
            print("Relevant Python file:                           image_container.py")
            print("Relevant function:                              ImageContainer.getImages()")
            print("Value of ImageContainer.imagesTxtPath variable: " + str(self.imagesTxtPath))
            print()

        # Otherwise, can proceed normally and populate the relevant lists
        else:
            # Iterates through all file paths identified from the image path definition text document
            for p in self.inputPaths:
                # Creates a Path object instance based on the current p value
                fileObject = Path(p)
                # Makes the path absolute, and in doing so checks whether the file exists
                try:
                    fileObject.resolve(strict=True)
                # If the file does not exist, a value of "True" is appended to self.missingFiles to denote this
                except FileNotFoundError:
                    self.missingFiles.append(True)
                    self.pilImages.append(PIL.Image.open(STANDBY_IMAGE_PATH))
                    self.tkImages.append(PIL.ImageTk.PhotoImage(image=self.pilImages[-1]))
                    # Console output for user
                    print("================================================================")
                    print("System could not open a file specified within the image path definition text document.")
                    print("The path shown below may point to a file which does not actually exist.")
                    print("Relevant Python file:                           image_container.py")
                    print("Relevant function:                              ImageContainer.getImages()")
                    print("Value of fileObject variable:                   " + str(fileObject))
                    print()
                # Otherwise, the file can be treated normally
                else:
                    self.missingFiles.append(False)
                    self.pilImages.append(PIL.Image.open(str(fileObject)))
                    self.tkImages.append(PIL.ImageTk.PhotoImage(image=self.pilImages[-1]))

    # Destructor for ImageContainer, called upon deletion
    def __del__(self):

        # For each PIL Image: Closes the file pointer, destroys the image core and releases its memory
        for p in self.pilImages:
            # Attempts to close
            try:
                p.close()
            # If the close() operation fails
            except:
                # TODO: Update this output to be smarter and list relevant values one after another, instead of calling
                #       all 7 of these print statements for each relevant value of ImageContainer.pilImages
                # Console output for user
                print("================================================================")
                print("System could not close a file within the ImageContainer's list of PIL Image objects.")
                print("This may be a bug where the list contains items of the wrong type, or a sign of a memory leak.")
                print("Relevant Python file:                           image_container.py")
                print("Relevant function:                              ImageContainer.__del__(self)")
                print("Relevant ImageContainer.pilImages value:        " + str(p))
                print()

        # Console output for user
        print("All PIL images have been released from memory.")


    # Performs all necessary operations to update the GUI to display this changed image
    # i is the index of the newly changed image within self.img.pilImages
    #     The actual image to be written to index i is based on self.pilImagesTemp
    # When clearTemp is True (True by default) the pilImagesTemp list will be cleared at the end of the function
    # NOTE: This function should be called every time a PIL image has been changed
    def updateImageLabel(self, i, clearTemp=True):
        print("Executing ImageContainer.updateImageLabel() with i = " + str(i))
        # TODO: The line below using an index of 0 is based on the fact that pilImagesTemp is currently assumed to only
        #         ever hold 1 element when functioning properly. This may change in the future, and in order to support
        #         that I should allow this index to be supplied as a function input parameter as well
        self.pilImages[i] = self.pilImagesTemp[0].copy()
        self.tkImages[i] = PIL.ImageTk.PhotoImage(image=self.pilImages[i])
        # Reconfigures the relevant GUI image Label
        self.gui.photoBoxImageLabels[i].configure(image=self.tkImages[i])

        # Clears pilImagesTemp if necessary
        if clearTemp:
            for i, image in enumerate(self.gui.img.pilImagesTemp):
                try:
                    image.close()
                # If the close() operation fails
                except:
                    # Console output for user
                    print("================================================================")
                    print("System could not close a file within the ImageContainer's list of TEMP PIL Image objects.")
                    print(
                        "This may imply a memory leak, or the close() method has already been called on this Image.")
                    print("Relevant Python file:                           image_container.py")
                    print("Relevant function:                              ImageContainer.updateImageLabel()")
                    print("Relevant index within pilImagesTemp:            " + str(i))
                    print()
            # Clears the list now that each list element has been close()d
            self.gui.img.pilImagesTemp = []


