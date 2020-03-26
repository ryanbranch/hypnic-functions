__name__ = "image_container"

import PIL
from PIL import Image, ImageTk

class ImageContainer():

    def __init__(self):
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

    # Destructor for ImageContainer, called upon deletion
    def __del__(self):
        # For each PIL Image: Closes the file pointer, destroys the image core and releases its memory
        self.pilImage1.close()
        self.pilImage2.close()
        self.pilImage3.close()
        self.pilImage4.close()
        print("Successfully released all PIL images from memory.")