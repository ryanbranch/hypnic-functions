# TODO:
#  A. Implement array-based image referencing
#    1. An associated text file for defining a list of input images would be great

__name__ = "image_container"

import PIL
from PIL import Image, ImageTk

class ImageContainer():

    def __init__(self, imagesTxtPath_):
        self.imagesTxtPath = imagesTxtPath_
        self.inputPaths = []
        self.missingFiles = []
        self.pilImages = []
        self.tkImages = []
        self.getImages()
        self.pathToImage1 = "media/image1.jpg"
        self.pathToImage2 = "media/image2.jpg"
        self.pathToImage3 = "media/image3.jpg"
        self.pathToImage4 = "media/image4.jpg"
        self.pilImage1 = PIL.Image.open(self.pathToImage1)
        self.pilImage2 = PIL.Image.open(self.pathToImage2)
        self.pilImage3 = PIL.Image.open(self.pathToImage3)
        self.pilImage4 = PIL.Image.open(self.pathToImage4)
        self.tkImage1 = PIL.ImageTk.PhotoImage(image=self.pilImage1)
        self.tkImage2 = PIL.ImageTk.PhotoImage(image=self.pilImage2)
        self.tkImage3 = PIL.ImageTk.PhotoImage(image=self.pilImage3)
        self.tkImage4 = PIL.ImageTk.PhotoImage(image=self.pilImage4)

    # Builds the relevant lists of image objects and related data, based on a text file
    # Text file is defined by INPUT_IMAGE_PATHS_FILE, a global variable in hypnic_gui.py
    #   A low priority but easy TODO: remove the global and allow this to be user-defined at runtime
    #
    def getImages(self):

        # Opens the text file containing a list of images
        filePath = self.imagesTxtPath
        # Exception handling ensures that the text file actually exists and can be opened
        try:
            with open(filePath) as f:
                print()
        except:
            print("Failed to open text file list of input images.")
            print("Relevant Python file:                           image_container.py")
            print("Relevant function:                              ImageContainer.getImages()")
            print("Value of filePath variable:                     " + str(filePath))
            print("Value of ImageContainer.imagesTxtPath variable: " + str(self.imagesTxtPath))
            exit("memomo")


    # Destructor for ImageContainer, called upon deletion
    def __del__(self):
        # For each PIL Image: Closes the file pointer, destroys the image core and releases its memory
        self.pilImage1.close()
        self.pilImage2.close()
        self.pilImage3.close()
        self.pilImage4.close()
        print("Successfully released all PIL images from memory.")