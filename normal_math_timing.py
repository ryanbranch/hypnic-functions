# TODO:
#  A. Read the following articles and resources:
#    1. https://medium.com/@ongchinhwee/accelerating-batch-processing-of-images-in-python-with-gsutil-numba-and-concurrent-futures-60ae0a99f68d
#      a. https://github.com/hweecat/numba-image-processing
#    2. https://github.com/numba/numba/blob/master/examples/gaussian-blur/gaussian-blur.py
#  B. Go through and remove any local variables that have become deprecated and are now unused

# Library Imports
from timeit import default_timer
import tkinter
import PIL
from PIL import Image, ImageTk
from pathlib import Path
import math
import numpy
import numba

# GLOBAL VARIABLES
# Path to the text document which lists the paths to all input images
INPUT_IMAGE_PATHS_FILE = "hypnic7/hypnic7_images.txt"  # FLAG: Hard-coded GUI parameter!


class NormalMathTiming():

    def __init__(self, gui_, tc_):

        # M E M B E R     V A R I A B L E S

        # INITIALIZATION TIMER
        # Timer beginning upon initialization of this object
        self.initTimer = default_timer()

        # GUI Reference
        self.gui = gui_
        # TimingContainer Reference
        self.tc = tc_

        # OTHER TIMERS
        # List of all timers, initialized as containing only self.initTimer
        self.timers = [self.initTimer]

        # index within pilImages of the image to manipulate
        self.currentImageIndex = -1
        # Defines the X and Y resolutions of this image
        self.xResCurrent = -1
        self.yResCurrent = -1

        # Holds a single PIL image (pixel Access object) at a time
        self.allPixels = []
        # Holds a PIL sequence object containing pixel values, for allDataList1D creation
        self.allData = None
        # Holds a single PIL image (standard python list of tuples, 1D array) at a time
        self.allDataList1D = []
        # Holds a single PIL image (standard python 2D list of lists of tuples, 2D array) at a time
        # Each inner list is a row of all pixels, of length equal to image width, and number of rows equal to height
        self.allDataList2D = []
        # Same as allDataList1D but a Numpy array
        self.allDataNumpyList1D = None
        # Same as allDataList2D but a 2D Numpy array
        self.allDataNumpyList2D = None



        # Holds a 2D list of 3-elt tuples with dimensions and positions matching f
        self.subImagePixels = []
        # self.subImageCoordinates is a list of 2 sub-lists which each contain 2 elements,
        #   referencing a [col, row] for top left and bottom right
        # [0][0] is the X (column) value for the top left vertex
        # [0][1] is the Y (row) value for the top left vertex
        # [1][0] is the X (column) value for the bottom right vertex
        # [1][1] is the Y (row) value for the bottom right vertex
        self.subImageCoordinates = [[], []]

    def defineCurrentImage(self):

        self.currentImageIndex = self.gui.controlBoxComboboxes[0].current()

        # Determines the X and Y resolutions of this image
        self.xResCurrent = self.gui.img.pilImages[self.currentImageIndex].size[0]
        self.yResCurrent = self.gui.img.pilImages[self.currentImageIndex].size[1]

        # Loads the image as a PIL PixelAccess object
        self.allPixels = self.gui.img.pilImages[self.currentImageIndex].load()
        # Loads the image as a PIL sequence object
        self.allData = self.gui.img.pilImages[self.currentImageIndex].getdata()
        # Loads the image as a standard 1D list
        self.allDataList1D = list(self.allData)
        [self.allDataList2D.append([self.allDataList1D[(r * self.xResCurrent) + i] for i in list(range(self.xResCurrent))]) for r in list(range(self.yResCurrent))]


    # Returns a (ROW, COLUMN) tuple representing the location of the n_th element  of a rectangular grid
    #   with a width of w_ and a height of h_
    # Element numbering is consecutive starting in the top left and moving from left-to-right across all columns of the row.
    #   When the last column is reached, this process repeats in the far-left column of the next row.
    # Element numbering is zero-indexed. As a result, an n_ value of 15 describes the 16th element in the grid
    # Row/Column numbering is zero-indexed. This means that a w_ value of 4 implies that the highest column index is 3
    # INVARIANT: n_ must be lower than the total number of cells
    # TODO: As described at the top of this file, consider going ALL-OUT with invariants when it comes to helper functions
    #       If doing so, would want to check input types for correctness (in this case, ensuring all are integers)
    # TODO: Consider prioritizing computational efficiency if I am ever calling this for grids with upwards of
    #       millions of elements, such as pixel coordinates within a photograph
    def getGridPos(n_, w_, h_):
        # Checks invariant
        # When this statement is entered then the invariant check has failed and we should likely quit as a result,
        # because the problem no longer has a defined solution and to return anything would likely break the program anyway
        if n_ >= ((w_ + 1) * (h_ + 1)):
            # Console output for user
            print("================================================================")
            print("Element index n_ exceeds maximum size allowed by grid dimensions w_ and h_.")
            print("The expected position of an element may differ from its actual location.")
            print("Relevant Python file:                           hypnic_helpers.py")
            print("Relevant function:                              getGridPos()")
            print("Value of n_:                                    " + str(n_))
            print("Value of w_:                                    " + str(w_))
            print("Value of h_:                                    " + str(h_))
            print()
            # Exits early
            exit(334)

        # Otherwise we can proceed normally!
        r = math.ceil((n_ + 1) / w_) - 1
        c = n_ % w_
        return (r, c)

    def sumColors(self, colorsIn):
        redResult = 0
        greenResult = 0
        blueResult = 0

    def multiplyColors(self, colorList):
        redResult = 0
        greenResult = 0
        blueResult = 0

    def createNewSubImage(self):
        self.subImagePixels = []
        # Returns a list of None values but also modifies self.subImagePixels as needed
        # Adds the necessary number of rows to self.subImagePixels as empty lists
        [self.subImagePixels.append([]) for r in list(range(self.subImageCoordinates[0][1], (self.subImageCoordinates[1][1] + 1)))]
        print(self.subImagePixels)

        # Returns a list of None values but also modifies self.subImagePixels as needed
        [self.subImagePixels[rowIndex].append(
            self.allPixels[c, r])
            for c in list(range(self.subImageCoordinates[0][0], (self.subImageCoordinates[1][0] + 1)))
            for rowIndex, r in enumerate(list(range(self.subImageCoordinates[0][1], (self.subImageCoordinates[1][1] + 1))))]

        print("RESULT FROM normalMathTiming.createNewSubImage():")
        print(self.subImagePixels)
        print("=======================================\n\n\n")



    # EXPLICITLY DESIGNED TO BE USED IN ITERATIVE OPERATIONS GOING ACROSS EACH PIXEL OF AN IMAGE
    # IF HOPPING AROUND TO A NON-CONSECUTIVE PIXEL (INCLUDING FROM END OF ROW x TO START OF ROW (x + 1)),
    #     MUST CALL self.createSubImage() INSTEAD
    #  - NOTE: It would be possible to sav the subimage from the beginning of the current row and use that to speed
    #          things up when calculating the subimage for the next row as well.
    #          TODO: Explore this possibility as a means of avoiding new self.createSubImage() calls for each row

    # All input parameters are 2-tuples of (col, row) coordinates
    # Different types of timing to test for modifySubImage:
    # A. Constructing an entirely new list based on subindices of the first list
    #   1. Would it be different using copy()?
    #   2. Would it be better to use tuples in this case?
    # B. Using pop() at the relevant indices (confirmed faster than remove())
    #   1. Necessitates the use of lists because tuples are immutable
    def modifySubImage(self, newTopLeft, newBottomRight):

        # TODO: Ensure that I picked the right coordinate indices
        # If the "ToRemove" variables are greater than zero, it implies that rows/columns are being removed
        #  - A value equal to 0 is also processed as removal, since list(range(0)) simply returns an empty list
        # If the "ToRemove" variables are less than zero, it implies that rows/columns are being added and not removed
        numColsToRemoveFront = newTopLeft[0] - self.subImageCoordinates[0][0]
        numColsToRemoveBack = self.subImageCoordinates[1][0] - newBottomRight[0]
        numRowsToRemoveFront = newTopLeft[1] - self.subImageCoordinates[0][1]
        numRowsToRemoveBack = self.subImageCoordinates[1][1] - newBottomRight[1]

        # front indices will count down starting from (prev top left - 1)
        # back indices will count up starting from (prev bottom right + 1)
        # ToAdd members are integer indices within the entire image being operated upon (whether row or col)
        colsToAddFront = []
        colsToAddBack = []
        rowsToAddFront = []
        rowsToAddBack = []
        if numColsToRemoveFront < 0:
            # numColsToRemoveFont is ADDED in the second range() argument because it is implicitly negative
            # range() has steps of -1 so that colsToAddFront counts DOWN for proper front-of-list insertion
            [colsToAddFront.append(i) for i in list(range(self.subImageCoordinates[0][0] - 1,
                                                          self.subImageCoordinates[0][0] + numColsToRemoveFront - 1,
                                                          -1))]

        if numColsToRemoveBack < 0:
            # numColsToRemoveBack is SUBTRACTED in the second range() argument because it is explicitly negative
            [colsToAddBack.append(i) for i in list(range(self.subImageCoordinates[1][0] + 1,
                                                         self.subImageCoordinates[1][0] - numColsToRemoveBack + 1))]

        if numRowsToRemoveFront < 0:
            # numRowsToRemoveFont is ADDED in the second range() argument because it is implicitly negative
            # range() has steps of -1 so that rowsToAddFront counts DOWN for proper front-of-list insertion
            [rowsToAddFront.append(i) for i in list(range(self.subImageCoordinates[0][1] - 1,
                                                          self.subImageCoordinates[0][1] + numRowsToRemoveFront - 1,
                                                          -1))]

        if numRowsToRemoveBack < 0:
            # numRowsToRemoveBack is SUBTRACTED in the second range() argument because it is explicitly negative
            [rowsToAddBack.append(i) for i in list(range(self.subImageCoordinates[1][1] + 1,
                                                         self.subImageCoordinates[1][1] - numRowsToRemoveBack + 1))]

        # Now that all row/column adding has been determined, remove rows and columns as needed
        # Removes rows from front of subimage
        [self.subImagePixels.pop(0) for i in list(range(numRowsToRemoveFront))]
        # Removes rows from back of subimage
        [self.subImagePixels.pop(-1) for i in list(range(numRowsToRemoveBack))]
        # Removes columns from front of subimage
        [self.subImagePixels[r].pop(0) for i in list(range(numColsToRemoveFront)) for r in list(range(len(self.subImagePixels)))]
        # Removes columns from back of subimage
        [self.subImagePixels[r].pop(-1) for i in list(range(numColsToRemoveBack)) for r in list(range(len(self.subImagePixels)))]


        # ADDING COLUMNS TO FRONT AND BACK OF EXISTING ROWS

        # If self.rowsToAddFront is empty, then we have removed 0 or more rows from the front so the index to use is new top edge (higher-valued, lower physically than the previous top edge)
        # If self.rowsToAddFront is not empty, then must add 1 or more rows to the top edge so the index to use is the previous top edge (higher valued, lower physically than the new top edge)
        lowestExistingRowIndex = max(newTopLeft[0], self.subImageCoordinates[0][0])

        # NOTE: References to rows within these column-related operations are valid as they simply bound the applicable rows
        # NOTE: Enumeration is initialized at lowestExistingRowIndex
        [r.insert(0, self.allPixels[c, n]) for c in colsToAddFront for n, r in enumerate(self.subImagePixels, lowestExistingRowIndex)]
        # NOTE: References to rows within these column-related operations are valid as they simply bound the applicable rows
        # NOTE: Enumeration is initialized at lowestExistingRowIndex
        # Adds cols to the back of the remaining rows
        # USES APPEND() AND NOT INSERT()
        [r.append(self.allPixels[c, n]) for c in colsToAddBack for n, r in enumerate(self.subImagePixels, lowestExistingRowIndex)]


        # NOTE: At and below this line, column indices and values are representative of the new subimage.
        #       This means that newTopLeft[0] and newBottomRight[0] are the inclusive bounds for subimage column span.
        subImageCols = list(range(newTopLeft[0], newBottomRight[0] + 1))
        # HOWEVER, rows are entirely missing from the top and bottom


        # Adds the necessary rows to the front (top) of the new subimage
        # ATTEMPT 3: (PRESUMED SUCCESS)
        [self.subImagePixels.insert(0, [self.allPixels[c, r] for c in subImageCols]) for r in rowsToAddFront]

        # Adds the necessary rows to the back (bottom) of the new subimage
        # USES APPEND() AND NOT INSERT()
        [self.subImagePixels.append([self.allPixels[c, r] for c in subImageCols]) for r in rowsToAddBack]


        # Updates self.subImageCoordinates to the newTopLeft and newBottomRight coordinates
        self.subImageCoordinates[0][0] = newTopLeft[0]
        self.subImageCoordinates[1][0] = newBottomRight[0]
        self.subImageCoordinates[0][1] = newTopLeft[1]
        self.subImageCoordinates[1][1] = newBottomRight[1]


        # TEMPORARY CONSOLE OUTPUT FOR DEBUGGING
        print("=================================================")
        print("self.subImagePixels:")
        print(self.subImagePixels)
        print("=================================================")



    # Sets all of the pixels in an image to black
    # i refers to the index of the image within self.gui.img.pilImages
    # This is version 1 of the function, which operates on the following algorithm:
    # 1. PLACEHOLDER
    # 3. PLACEHOLDER
    def setPixelsBlack1(self, i):
        timeStartSetPixelsBlack = default_timer()
        print()

    # Sets all of the pixels in an image to black
    # i refers to the index of the image within self.gui.img.pilImages
    # This is version 2 of the function, which operates on the following algorithm:
    # 1. PLACEHOLDER
    # 3. PLACEHOLDER
    def setPixelsBlack2(self, i):
        timeStartSetPixelsBlack = default_timer()
        print()

    def testFunc(self):
        return(1)
