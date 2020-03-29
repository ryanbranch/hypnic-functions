
# hypnic-functions

**hypnic-functions** code that I've written for the manipulation of images using custom user-defined operations. The project started from a conversation I had with a friend who creates digital glitch-art; being familiar with Python's PIL library it led me to wonder about the ways that I could manipulate an image's pixels programmatically. This code has a wide range of applications, but the specific focus in development is to simply explore and define "interesting" approaches for the creation of digital art. 

# A Note

**hypnic-functions** began in late 2019 as a single file with zero runtime user input. As my ideas have become more complex I've decided to develop a GUI for keeping things comprehensible and supporting more advanced visualizations. I don't have any sort of "end goal" or defined feature list with this work, it's more of a pet project that I work on whenever I'm inclined. I do hope to stray from more "standard" techniques that are widely supported within established image editing softwares, and instead focus on novel operations that are difficult or impossible without writing custom code. 

## Getting Started

As of writing, the program hasn't seen much work in terms of user-friendliness. I hope to change this in the future, but current usage of the code requires a lot of manual editing. As I create and continue to extend the capabilities of the GUI, this will facilitate the writing of more complicated manipulation functions as well as a suite of additional tools to provide additional context and control to the user.

* **hypnic_wrapper.py** launches the code

* **hypnic_images.txt** specifies a list of strings representing file paths to images which are loaded at the beginning of runtime

## Built With

* [**pip**](https://pip.pypa.io/en/stable/) - To install various Python packages for the project
* [**Pillow**](https://python-pillow.org/) - For manipulating image files within Python
* [**Matplotlib**](https://matplotlib.org/) - To visualize numerical data during image manipulation
* [**Tkinter**](https://wiki.python.org/moin/TkInter) - To build the GUI

## Contributing

I started this project as a personal endeavor and given the lack of direction or structure, I don't plan to collaborate with others on it. Regardless, feel free to reach out if you have an interest in contributing

## Acknowledgments

This project has been and continues to be a learning experience for me, and I've relied heavily on others in that learning. The following people provided help in terms of things like sample code and answers to questions posted online:

* **Sentdex**, via the tutorials from his website [PythonProgramming.net](https://pythonprogramming.net/), especially the ["GUIs with Tkinter (intermediate)"](https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk) tutorial series
* **Bryan Oakley** ([GitHub](https://github.com/boakley)) for a number of incredible answers on StackExchange
* **GitHub user** [**PurpleBooth**](https://github.com/PurpleBooth) for the [template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) that I used in creating this README
* **John W. Shipman** (contact unknown) for authoring the Tkinter 8.5 reference from the New Mexico Tech Computer Center, referenced in the list of resources acknowledged below

I'm also thankful to the following specific resources which were referenced during development

* [**This document**](http://coecsl.ece.illinois.edu/ge423/spring05/group8/finalproject/hsv_writeup.pdf) about the mathematical relationship between RGB and HSV color representations, from The University of Illinois College of Engineering's GE 423 course (circa 2005)
* RapidTables' [**tool**](https://www.rapidtables.com/convert/color/hsv-to-rgb.html) for HSV-to-RGB conversion
* The [**kite.com**](https://kite.com/python/docs/) Python documentation search
* The [**Tk Commands Documentation**](https://www.tcl.tk/man/tcl8.6/TkCmd/contents.htm) from tcl.tk
* **The Tkinter 8.5 reference** written by John W. Shipman
  The document appears to have been originally hosted by NMT at [this broken link](http://infohost.nmt.edu/tcc/help/pubs/tkinter/index.html) but a [**cached version**](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html) is hosted on GitHub Pages by user [anzeljg](https://github.com/anzeljg)
    It was also originally distributed in PDF form, and a [download](http://reu.cct.lsu.edu/documents/Python_Course/tkinter.pdf) is available from Louisiana State University
  
