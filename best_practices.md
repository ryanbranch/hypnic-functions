# Best Practices

The goal of this file is to define the practices that should be used in development and usage of this program. 

# Development

Since I'm developing this alone I won't be defining things like syntax practices, but I do think storing information about things like GUI properties in one central location could be useful as opposed to having to crawl through many sections of many files.

## GUI

### Appearance and Styles
- Wherever possible, the arguments given upon initialization of widget elements should be defined using class member variables as opposed to hard-coded variables
	- For example, the ***internalPaddingButton*** and ***defaultInternalPaddingGrid*** member variables of the ***DimensionContainer*** class
 - All elements should use internal padding instead of external padding wherever possible, unless deemed inappropriate on a per-widget basis
 - Where possible, elements should not use padding and instead rely on proper placement with Tkinter's place() method

### Functionality
- Care should be taken to ensure that the GUI is usable in all resolutions above ***1280 x 720*** and aspect ratios between ***4:3*** and ***2:1***
- A cohesive and user-friendly layout should be guaranteed for resolutions between 1280 x 720 and 1920 x 1080 and aspect ratios between ***4:3*** and ***2:1***

 
## Images and Manipulation

- [At least above some currently undefined minimum resolution,] If at any point it becomes apparent that an image is not explicitly needed in the near future then its PIL Image object should be closed via the PIL.Image.close() method

  The following prerequisites must or should be met before unloading an image:
	- References to the image (such as those within the ImageContainer.tkImages list) should be dealt with appropriately and then removed from the list

      Appropriate handling implies element removal as opposed to things like setting the missingFiles element to ***True*** or the tkImages element to ***None***

  The following operations must or should be performed after the PIL.Image.close() method is called:
   - No post-close operations are required to my knowledge, but I would need to give this more thought before stating that as a face


## User Input

- In cases where the required format or syntax of a user-defined parameter is not common or obvious, an explanation or example should be provided in the GUI
<br>
<br>
<br>
<br>
<br>
# Usage

Following these guidelines while running the program will keep things running smoothly and avoid errors/crashes.

## GUI

- The main GUI window can be resized to any dimension for your convenience, however it is not guaranteed to be usable on monitors with a resolution below 1280 x 720
- Though the GUI window only displays a fraction of high-resolution images, it still must load and process the entirety of each image. This may cause the program to slow down or lag
 
## Images and Manipulation

 File formats tested and verified to be supported for input images:
 - .JPG 

In theory, the program should support all file formats that the PIL Python library supports for input. This includes, but is not limited to:
 - .BMP
 - .JPG
 - .PNG
 - .ICO
 - .TIFF
 - .GIF

Support is not currently developed or guaranteed for image formats which can contain multiple frames within a single file (such as .TIFF and .GIF)

## User Input
 - The program may crash if you define an output directory in which the program does not have write permissions
 - Many user-defined parameters are strictly designed to accept correct inputs
	 - For example if you are asked to provide an integer but give a string instead, this will likely result in unexpected behavior
	 - Error handling for such issues is considered low priority compared to the development of actual program functionality, and may never be implemented