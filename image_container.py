# TODO:
#  ==============================================================================
#  S. self.getImages() currently breaks if hypnic_images.txt isn't long enough.
#    1. Fix this so that any unspecified lines will be filled with the image at STANDBY_IMAGE_PATH
#    2. IN DOING SO, ALSO ENSURE THAT EXTRA UNNECESSARY IMAGES (BEYOND ROWxCOL plus others out-of-frame) ARE EXCLUDED
#  ==============================================================================
#  A. Placeholder

__name__ = "image_container"

# Library Inputs
from timeit import default_timer
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

        # M E M B E R     V A R I A B L E S

        # INITIALIZATION TIMER
        # Timer beginning upon initialization of this object
        self.initTimer = default_timer()

        # OTHER TIMERS
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]

        # So that the StyleContainer instance can refer to the HypnicGUI instance
        self.gui = gui_

        # Member variables related to input
        self.imagesTxtPath = imagesTxtPath_
        self.inputImagePathStrings = []
        # Array of booleans where a value of True denotes that the associated string within self.inputImagePathStrings is invalid
        # For the same indices at which self.missingFiles contains a value of True, the corresponding element within
        #   associated lists (e.g. self.pilImages and self.tkImages) are based on the standby image (STANDBY_IMAGE_PATH)
        self.missingFiles = []

        # Member variables related to output
        # NOTE: The idea of this (FLAG) being hard-coded is temporary. TODO: Switch to a more user-friendly approach
        self.outputImagePathStrings = ["media/outputA",
                                       "media/outputB",
                                       "media/outputC",
                                       "media/outputD",
                                       "media/outputE",
                                       "media/outputF",
                                       "media/outputG",
                                       "media/outputH",
                                       "media/outputI"]
        self.outputImageExtension = ".jpg"
        # Stores the number of times that an output image has been generated for a given Photo Box
        self.outputImagePathCounts = [0] * len(self.outputImagePathStrings)

        # Object Storage
        # Array of PIL Image objects directly corresponding to the path strings in self.inputImagePathStrings
        self.pilImages = []
        # Array of PIL Tkinter PhotoImage objects directly corresponding to the path strings in self.inputImagePathStrings
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
                    # Ignoring blank lines, appends each specified path to the self.inputImagePathStrings list
                    if path:
                        self.inputImagePathStrings.append(path)
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
        if not self.inputImagePathStrings:
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
            for p in self.inputImagePathStrings:
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


    # Placeholder
    def copyImageLabel(self, i1, i2):
        print("Executing ImageContainer.loadImageLabel() with i1 = " + str(i1) + "; i2 = " + str(i2))


    # Placeholder
    def swapImageLabels(self, i1, i2):
        print("Executing ImageContainer.loadImageLabel() with i1 = " + str(i1) + "; i2 = " + str(i2))


    # (Re)Loads the image from the ith Photo Box, based on filenames present in the imagesTxtPath file at launch-time
    def loadImageLabel(self, i):
        print("Executing ImageContainer.loadImageLabel() with i = " + str(i))
        # Attempts to close any open image currently occupying slot i
        try:
            self.pilImages[i].close()
        # If the close() operation fails
        except:
            # Console output for user
            print("================================================================")
            print("System could not close a file within the ImageContainer's list of PIL Image objects.")
            print("This may be a bug where the list contains items of the wrong type, or a sign of a memory leak.")
            print("Relevant Python file:                           image_container.py")
            print("Relevant function:                              ImageContainer.loadImageLabel)")
            print("Relevant i value:                               " + str(i))
            print()

        # Creates a Path object instance based on the current p value
        fileObject = Path(self.inputImagePathStrings[i])
        # Makes the path absolute, and in doing so checks whether the file exists
        try:
            fileObject.resolve(strict=True)
        # If the file does not exist, a value of "True" is appended to self.missingFiles to denote this
        except FileNotFoundError:
            self.missingFiles[i] = True
            self.pilImages[i] = PIL.Image.open(STANDBY_IMAGE_PATH)
            self.tkImages[i] = PIL.ImageTk.PhotoImage(image=self.pilImages[i])
            # Reconfigures the relevant GUI image Label
            self.gui.photoBoxImageLabels[i].configure(image=self.tkImages[i])
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
            self.missingFiles[i] = False
            self.pilImages[i] = PIL.Image.open(str(fileObject))
            self.tkImages[i] = PIL.ImageTk.PhotoImage(image=self.pilImages[i])
            # Reconfigures the relevant GUI image Label
            self.gui.photoBoxImageLabels[i].configure(image=self.tkImages[i])


    # Performs all necessary operations to update the GUI to change a (displayed) image after it has been edited
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
