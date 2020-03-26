# TODO:
#  A. Implement array-based image referencing
#    1. An associated text file for defining a list of input images would be great

__name__ = "image_container"

import PIL
from PIL import Image, ImageTk
import os
from pathlib import Path
import copy

# G L O B A L   V A R I A B L E S
# Path to an image which is used by default when a desired image fails to load
STANDBY_IMAGE_PATH = "media/standby.jpg"

class ImageContainer():

    def __init__(self, imagesTxtPath_):

        self.imagesTxtPath = imagesTxtPath_
        self.inputPaths = []
        # Array of booleans where a value of True denotes that the associated string within self.inputPaths is invalid
    #   # For the same indices at which self.missingFiles contains a value of True, the corresponding element within
        #   associated lists (e.g. self.pilImages and self.tkImages) are based on the standby image (STANDBY_IMAGE_PATH)
        self.missingFiles = []
        self.pilImages = []
        self.tkImages = []

        self.getImages()

        # NOTE: The code below comes from before input image files were specified within a text document
        # I'm leaving part of the code as a reference for now, and will remove it later when I know it's not needed
        """
        self.pathToImage1 = "media/image1.jpg"
        self.pathToImage2 = "media/image2.jpg"
        self.pilImage1 = PIL.Image.open(self.pathToImage1)
        self.pilImage2 = PIL.Image.open(self.pathToImage2)
        self.tkImage1 = PIL.ImageTk.PhotoImage(image=self.pilImage1)
        self.tkImage2 = PIL.ImageTk.PhotoImage(image=self.pilImage2)
        """

    # Returns true if char is a "/" or "\" character
    def isSlash(self, char):
        if (char == "/") or (char == "\\"):
            return True
        else:
            return False

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

        # NOTE: Saving this code for later, just in case
        # This large block of code is left over from an attempt to do a more in-depth parsing of the text document
        # It became too complicated and I deemed it unnecessary but I'm including this commit so that the work is saved
        #   for future use. Will remove immediately in the following commit.
        """
        # Iterates through each file path defined within self.imagesTxtPath
        for path in paths:
            # Prepends a forward-slash character in order to ensure that Path objects initialize properly
            print(path)
            print(20)
            path.insert(0, "/")
            print(path)
            print(100)
            self.inputPaths.append(path)
            print(100)
            print(self.inputPaths)

        print(paths)
        pathString = f.read()
        print(pathString)
        # Iterates through f line-by-line until either the file ends or a blank line is reached
        while pathString != "":
            pathEdit = pathString
            # Post-processing on pathString to ensure that it parses folders correctly
            # Specifically, if pathString contains a "/" or "\" character then the path itself contains a folder
            #   and as a result, a "/" character must be present in position 0 of the string
            # Finds the indices, within pathstring, of the first "/" and "\" characters
            firstForward = pathEdit.find("/")
            print(5)
            firstBack = pathEdit.find("\\")
            print(6)
            # If both calls return -1, then the path can be assumed to not contain any folder names
            #   and so pathString does not need to be modified before the append operation
            # But if either is non-negative, then there is a slash present somewhere
            if (firstForward != -1) or (firstBack != -1):
                print(7)
                firstSlash = min(firstForward, firstBack)
                print(8)
                # If the first "/" or "\" character appears at index 0, then the path is already valid
                # If not, we simply insert a "/" character at index 0
                if firstSlash != 0:
                    print(9)
                    print(pathEdit)
                    pathEdit.insert(0,"/")
                    print(11)
            # Appends the resulting string to self.inputPaths
            print(10)
            self.inputPaths.append(pathEdit)
            print(pathEdit)
            print(pathString)
            # Grabs a new line for the next iteration
            pathString = f.read()
        """

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

        # NOTE: The code below comes from before input image files were specified within a text document
        # I'm leaving part of the code as a reference for now, and will remove it later when I know it's not needed
        """
        self.pilImage1.close()
        self.pilImage2.close()
        """

        # For each PIL Image: Closes the file pointer, destroys the image core and releases its memory
        for p in self.pilImages:
            # Attempts to close
            try:
                p.close()
            # If the close() operation fails
            except:
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
