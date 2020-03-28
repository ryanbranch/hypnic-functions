# hypnic-functions

hypnic-functions is a collection of code that I've written to facilitate the manipulation of images using customizable batch operations. The project started from a conversation I had with a friend (nickname "hypnic") who was creating digital glitch-art; it led me to wonder what would result if the colors of every pixel in an image were modified as a function of pixel position. My curiosity continued from there and I have since added more and more capabilities. This code has a wide range of applications, but the specific focus in development is to explore and define "interesting" mathematical operations for the creation of digital art. 

# A Note

hypnic-functions began in late 2019 as a single-file program with zero runtime user input and no plan of ever making things easier on the user. As my ideas have become more complex I've decided to develop a GUI for keeping things comprehensible and supporting more advanced visualizations. I don't have any sort of "end goal" or defined feature list with this work, it's more of a pet project that I work on whenever I'm inclined. I do hope to stray from more "standard" techniques that are widely supported within established image editing softwares, and instead focus on novel operations that are difficult or impossible without writing custom code.

## Getting Started

As of writing, the program hasn't seen much work in terms of user-friendliness. I hope to change this in the future, but current usage of the code requires a lot of manual editing.

hypnic_wrapper.py launches the code

hypnic_images.txt specifies a list of strings representing file paths to images which are loaded at the beginning of runtime

## Built With

* [pip](https://pip.pypa.io/en/stable/) - To install various Python packages for the project
* [Pillow](https://python-pillow.org/) - For manipulating image files within Python
* [Matplotlib](https://matplotlib.org/) - To visualize numerical data during image manipulation
* [Tkinter](https://wiki.python.org/moin/TkInter) - To build the GUI

## Contributing

I started this project as a personal endeavor and given the lack of real direction or structure, I don't plan to collaborate with others on it. That being said, if you're intrigued by this sort of thing and interested in contributing then please feel free to reach out.

## Acknowledgments

This project has been and continues to be a major learning experience for me, and I've relied heavily on others in that learning. The following people provided significant help in terms of sample code and answers to questions posted online:

* Sentdex, via the tutorials from his website [PythonProgramming.net](https://pythonprogramming.net/), especially the ["GUIs with Tkinter (intermediate)"](https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk) tutorial series
* Bryan Oakley ([GitHub](https://github.com/boakley)) for a number of incredible answers on StackExchange
* GitHub user [PurpleBooth](https://github.com/PurpleBooth) for the [template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) that I used in creating this README

I'm also thankful to the following specific resources which were referenced significantly during development

* [This document](http://coecsl.ece.illinois.edu/ge423/spring05/group8/finalproject/hsv_writeup.pdf) from The University of Illinois College of Engineering's GE 423 course, circa 2005
* RapidTables' [tool](https://www.rapidtables.com/convert/color/hsv-to-rgb.html) for HSV-to-RGB conversion
* The [kite.com](https://kite.com/python/docs/) Python documentation search
