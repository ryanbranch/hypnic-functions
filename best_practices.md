

# Best Practices

The goal of this file is to define the practices that should be used in both **development** and **usage** of this program. 
<br>
<br>
# Development

## Abstraction

In order to not only maintain readability but also to facilitate easier code navigation and higher productivity during development, it is important to keep things highly abstracted. By building many custom classes within their own files, we can separate functionalities of the program in a rational and meaningful way. The list below outlines the classes (and beyond) that exist and clarifies potential confusion as to what types of data and functionalities each class should be responsible for handling.
- **HypnicLauncher**
	- Not yet developed into a class
	- Will exist within **hypnic_launcher.py**
	- Will likely be a member of **HypnicWrapper**, although the reverse may end up being true
	- Planned functionality of opening a "pre-GUI" popup window upon launch, in which a user can specify various inputs useful to know before starting the main GUI
- **HypnicWrapper**
	- Solely exists to initialize a **HypnicGUI** instance and call its **mainloop()** method
- **HypnicGUI**
	- It is of type **tkinter.<span></span>Tk**
	- All **"Container"** class instances belong to the **HypnicGUI** instance, either directly or through children
	- ***Very likely should be further abstracted*** via the creation of additional container classes related to the initialization, storage, and configuration of ***ttk variables***

      The planned approach for this is:
		 - Allow **Container Classes** to handle the initialization and default configuration of widgets, before placement
		   ### EVERY class member variable should either be initialized within \_\_init\_\_() or "above" it.
		 - Allow **HypnicGUI** to handle the actual placement of widgets
			 - whether through the **tkinter.place()** or **tkinter.grid()** methods
		 - Allow **HypnicGUI** to handle all post-initialization operations on widgets, *potentially through member functions of the Container classes*, when possible and reasonable
		
- **StyleContainer**
	- Exclusively related to **ttk**'s *theme* and *style* aspects
	- Holds the **ttk.Style()** instance
	- Holds the **DimensionContainer** instance, although this isn't necessarily ideal and ownership may be transferred to **HypnicGUI** in the future
- **DimensionContainer**
	- Describes dimensions of GUI elements in terms of a pixel count or a relative size
	- Initializes and stores any default hard-coded dimensions
	- Initializes and calculates any variable dimensions
- **ImageContainer**
	- Handles the loading and unloading of images from RAM
	- Handles import, export, and any related operations including file type modification
	- Holds **all** instances of **PIL.Image** and **PIL.ImageTk.PhotoImage** objects
	- Currently handles the loading of a text file which tells the program which images to load into RAM, although this will become obsolete once defined via runtime user input
- **hypnic_helpers.py**
	- Not even defined within a class, no need to instance
	- A suite of functions, usually very low level, to perform operations which may be repeatedly called at a variety of points during operation.
	 If a function:
		- takes straightforward inputs
		- provides straightforward outputs
		- does not require access to any class member variables

      Then it is likely a good candidate for **hypnic_helpers.py**
	  
## Naming

- **Radiobutton** is one word and the "b" should not be capitalized unless absolutely necessary
- **Checkbutton** is one word and the "b" should not be capitalized unless absolutely necessary

## GUI

### Appearance and Styles
- Wherever possible, the arguments given upon initialization of widget elements should be defined using class member variables as opposed to hard-coded variables
	- For example, the ***internalPaddingButton*** and ***defaultInternalPaddingGrid*** member variables of the ***DimensionContainer*** class
 - All elements should use internal padding instead of external padding wherever possible, unless deemed inappropriate on a per-widget basis
 - Where possible, elements should not use padding and instead rely on proper placement with **Tkinter**'s place() method

### Functionality
- Care should be taken to ensure that the GUI is usable in all resolutions above ***1280 x 720*** and aspect ratios between ***4:3*** and ***2:1***
- A cohesive and user-friendly layout should be guaranteed for resolutions between **1280 x 720** and **1920 x 1080** and aspect ratios between ***4:3*** and ***2:1***

 
## Images and Manipulation

- [At least above some currently undefined minimum resolution,] If at any point it becomes apparent that an image is not explicitly needed in the near future then its PIL Image object should be closed via the **PIL.Image.close()** method

  The following prerequisites must or should be met before unloading an image:
	- References to the image (such as those within the **ImageContainer.tkImages** list) should be dealt with appropriately and then removed from the list

      Appropriate handling implies element removal as opposed to things like setting the **missingFiles** element to ***True*** or the **tkImages** element to ***None***

  The following operations must or should be performed after the **PIL.Image.close()** method is called:
   - No post-close operations are required to my knowledge, but I would need to give this more thought before stating that as a face


## User Input

- In cases where the required format or syntax of a user-defined parameter is not common or obvious, an explanation or example should be provided in the GUI
<br>
<br>
<br>
# Usage


## GUI

- The main GUI window can be resized to any dimension for your convenience, however it is not guaranteed to be usable on monitors with a resolution below **1280 x 720**
- Though the GUI window only displays a fraction of high-resolution images, it still must load and process the entirety of each image. This may cause the program to slow down or lag
 
## Images and Manipulation

 File formats tested and verified to be supported for input images:
 - **.JPG**

In theory, the program should support all file formats that the PIL Python library supports for input. This includes, but is not limited to:
 - *.BMP*
 - *.JPG*
 - *.PNG*
 - *.ICO*
 - *.TIFF*
 - *.GIF*

Support is not currently developed or guaranteed for image formats which can contain multiple frames within a single file (such as .TIFF and .GIF)

## User Input
 - The program may crash if you define an output directory in which the program does not have write permissions
 - Many user-defined parameters are strictly designed to accept correct inputs
	 - For example if you are asked to provide an integer but give a string instead, this will likely result in unexpected behavior
	 - Error handling for such issues is considered low priority compared to the development of actual program functionality, and may never be implemented
<br>
<br>
<br>
# TODO:

Many **TODO**s are already documented throughout my code, but I'd like to also keep track of those specific ones which inform or affect my own practices in writing and using this program. 

 - Improve efficiency, especially in regards to image manipulation operations and associated function calls
	- "Numba" and its "stencil" package may be useful for this
		- [Gaussian Blur Example](https://github.com/numba/numba/blob/master/examples/gaussian-blur/gaussian-blur-pa.py) with Numba and PIL
 - Increase the amount of abstraction to keep **hypnic_gui.py** shorter and more comprehensible
	- One consideration was to make a WidgetContainer class
	- Now actually considering a separate class for each widget type depending on how they're handled
		- Classes could include (non-exhaustive)
			- *FrameContainer*
			- *LabelContainer*
			- *ButtonContainer*
			- *CheckbuttonContainer*
			- *MenubuttonContainer*
			- *RadiobuttonContainer*
		- Given the large number of ttk widget classes directly related to user input, it could even make sense to have an InputContainer or InputWidgetContainer class
		- For example, **Buttons** have their own class and all **Labels** (regardless of text/image properties) have their own as well
	- I currently think that they should be member variables of the **HypnicGUI** instance
		- This goes against the fact that the **DimensionContainer** instance belongs to the **StyleContainer** instance
			- That was done in the first place for code readability reasons, but in hindsight it was poor from an overall organization perspective
 - Create an official naming convention to be followed for naming member variables of my own custom classes
 	- This is especially important for higher level objects such as **ttk Frames** and **Labels**
	- The convention should attempt to be consistent between all files such that all names imply a clear function without needing to know to the class to which the variable belongs
	- I consider it crucial that type can be discerned solely from name for the following types:
		- **ttk.Frame** objects
		- **lists** of **ttk.Frame** objects
		- **ttk.Label** objects
		- **lists** of **ttk.Label** objects
		- **ttk.Button** objects
		- **lists** of **ttk.Button** objects
		- lists of names of custom-defined **ttk** styles
- Define that naming convention (and any others) within this document
	- Should consider defining conventions for [file/class/function/etc] names as well, but I see no current reason why this should be a priority
- Go through and add ***return*** statements at the end (and elsewhere) of my functions, based on standard Python conventions
