# TODO:
#  A. Although I'm not worrying too much about invariant handling in this project, I think it would be a good idea to
#     specifically document and handle it for any and all of these helper functions
#    1. I can even make additional helper functions used for invariant checking
#    2. Some of these can be called for so many different reasons that I think it's important to build my own system
#       for catching any errors and sending relevant info to the console

# Library Imports
import random
import math

__name__ = "hypnic_helpers"

# G L O B A L   V A R I A B L E S

# COLOR-RELATED
# TODO: Really doesn't make sense to define these here... Probably best to do it within each function not only for
#       comprehensibility but to get better results
# The minimum value (integer from 0 to 255) for the high-value components when generating a random specific shade
MIN_HIGH_VAL = 191 # FLAG: Hard-coded GUI parameter!
MAX_LOW_VAL = 63 # FLAG: Hard-coded GUI parameter!
# The minimum value (integer from 0 to 255) for the low-value components when generating a random specific shade



# H E L P E R   F U N C T I O N S

# GENERAL MATH

# Returns True if n_ is an even number, or False if it is an odd number
def isEven(n_):
    return (n_ % 2) == 0

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

# Returns the nearest integer to the distance between two X/Y coordinate pairs
def calcDist(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2))

# Defines an algebraic function on the cartesian plane
# Takes an X value as input and returns the Y value at X on that algebraic function
# NOTE: Currently returns an error if slope is too negative or y intercept is too low
#       NEED TO INVESTIGATE WHY THIS HAPPENS
def calcCartesianFunc(xIn, slope, yIntercept):
    yOut = round(xIn * slope + yIntercept)
    return yOut



# COLOR CONVERSION AND MATH

# Takes a 3-element tuple as input
# Each value should be an integer between 0 and 255, representing the R, G, and B values for a color
# Returns the corresponding "hex code" as a string of format "#FFFFFF"
def rgbToHex(rgb_):
    return '#%02x%02x%02x' % rgb_

# Takes a color "hex code" as input, specifically a string of format "#FFFFFF"
# hex_ must be a 7-digit string consisting of a "#" character followed by 6 digits where each is between 0-9 or A-F
def hexToRGB(hex_):
    # Credit to StackOverflow users "vallentin" and "John1024" for their elegant approach to this conversion
    # The answer can be viewed at https://stackoverflow.com/a/29643643
    # The manipulated value of hex is assigned to a second string to prevent unwanted interactions
    hexStripped = hex_.lstrip("#")
    return tuple(int(hexStripped[i:i+2], 16) for i in (0, 2, 4))

# Converts an RGB color value to an HSV color value
# Based on algorithm (with modified domain) from:
#     http://coecsl.ece.illinois.edu/ge423/spring05/group8/finalproject/hsv_writeup.pdf
# R, G, and B are integers from 0 to 255 inclusive
# H, S, and V are each measured on a continuous scale
# H, conceptually, is measured in degrees and ranges from 0 <= H < 360
# S is measured from 0 to 1 inclusive
#   The lower S is, the more gray is present, causing it to appear faded
# V is measured from 0 to 1 inclusive
#   V represents brightness, where 0 is fully dark and 1 is fully bright
#   If V is 0, then the color is always black, regardless of H or S
def fromRGBtoHSV(rgb):

    minRGB = float(min(rgb))
    maxRGB = float(max(rgb))
    deltaRGB = maxRGB - minRGB
    h = 0
    s = 0
    v = maxRGB / 255
    # r == g == b == 0
    if maxRGB == 0:
        return (h, s, v)
    else:
        s = deltaRGB / maxRGB

    # Hue is null
    if deltaRGB == 0:
        return (h, s, v)
    # Hue is non-null
    else:
        # Hue is between yellow and magenta
        if rgb[0] == maxRGB:
            h = round(60 * ((rgb[1] - rgb[2]) / (deltaRGB)))
        # Hue is between cyan and yellow
        elif rgb[1] == maxRGB:
            h = round(60 * (2 + ((rgb[2] - rgb[0]) / (deltaRGB))))
        # Hue is between magenta and cyan
        else:
            h = round(60 * (4 + ((rgb[0] - rgb[1]) / (deltaRGB))))
        # Ensure that Hue is in the 0 <= H < 360 range
        h %= 360

    return (h, s, v)

# Converts an HSV color value to an RGB color value
# Based on algorithm (with modified domain) from:
#     https://www.rapidtables.com/convert/color/hsv-to-rgb.html
# R, G, and B are integers from 0 to 255 inclusive
# H, S, and V are each measured on a continuous scale
# H is measured in degrees on the domain of 0 <= H < 360
# S and V range from 0 to 1 inclusive
def fromHSVtoRGB(hsv):

    c = hsv[1] * hsv[2]
    x = c * (1 - abs((hsv[0] / 60.0) % 2 - 1))
    m = hsv[2] - c

    if hsv[0] < 180:
        if hsv[0] < 120:
            # 0 <= H < 60
            if hsv[0] < 60:
                rgb = [c, x, 0]
            # 60 <= H < 120
            else:
                rgb = [x, c, 0]
        # 120 <= H < 180
        else:
            rgb = [0, c, x]
    else:
        # 180 <= H < 240
        if hsv[0] < 240:
            rgb = [0, x, c]
        else:

            # 240 <= H < 300
            if hsv[0] < 300:
                rgb = [x, 0, c]
            # 300 <= H < 360
            else:
                rgb = [c, 0, x]

    rgb[0] = int(round(255 * (rgb[0] + m)))
    rgb[1] = int(round(255 * (rgb[1] + m)))
    rgb[2] = int(round(255 * (rgb[2] + m)))
    return tuple(rgb)

# Takes a 3-element RGB tuple as input and returns the luminosity, which also has a magnitude of 0 to 255
# Luminosity is usually considered the best approach for turning images to grayscale
# Based on the explanation from https://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/
def getLuminosity(rgb):
    return math.floor((0.21 * rgb[0]) + (0.72 * rgb[1]) + (0.07 * rgb[2]))



# COLOR GENERATION

# NOTE: For ease of readability and avoiding extraneous code, if writing a large number of highly specific functions,
#       (e.g. to get a random shade of blue, green, yellow, orange, etc.) I will only write RGB versions,
#       and simply pass their output into self.rgbToHex when necessary.
#       This is NOT a good practice, and if I'm calling these functions millions/billions of times per minute I should
#       absolutely rewrite them to be as time-efficient as possible.
#       TODO: Address the above in the future, if/when things become so slow that any of the functions are a problem

# Returns a 3-element tuple where each element is a random integer between 0 and 255
def getRandomRGB():
    return (random.randrange(0,256), random.randrange(0,256), random.randrange(0,256))

# Returns a 7-digit string consisting of a "#" character followed a random 6-digit hexadecimal number
def getRandomHex():
    # Credit to StackOverflow user "Eneko Alonso" for this method of generating random 6-digit hex strings
    # It can be viewed at https://stackoverflow.com/a/18035471
    # TODO: Switch this back to a single line, currently printing return value in order to debug
    x = ("#" + ("%06x" % random.randint(0, 0xFFFFFF)))
    print(x[0])
    return x

# Returns a shade of red as an RGB tuple
def getRandomRed():
    return (random.randrange(0,MIN_HIGH_VAL), random.randrange(0,MAX_LOW_VAL), random.randrange(0,MAX_LOW_VAL))

# Returns a shade of yellow as an RGB tuple
def getRandomYellow():
    return (random.randrange(0,MIN_HIGH_VAL), random.randrange(0,MIN_HIGH_VAL), random.randrange(0,MAX_LOW_VAL))

# Returns a shade of green as an RGB tuple
def getRandomGreen():
    return (random.randrange(0,MAX_LOW_VAL), random.randrange(0,MIN_HIGH_VAL), random.randrange(0,MAX_LOW_VAL))

# Returns a shade of Blue-Green as an RGB tuple
def getRandomBluegreen():
    return (random.randrange(0,MAX_LOW_VAL), random.randrange(0,MIN_HIGH_VAL), random.randrange(0,MIN_HIGH_VAL))

# Returns a shade of blue as an RGB tuple
def getRandomBlue():
    return (random.randrange(0,MAX_LOW_VAL), random.randrange(0,MAX_LOW_VAL), random.randrange(0,MIN_HIGH_VAL))

# Returns a shade of purple as an RGB tuple
def getRandomPurple():
    return (random.randrange(0,MIN_HIGH_VAL), random.randrange(0,MAX_LOW_VAL), random.randrange(0,MIN_HIGH_VAL))

# Returns a shade of gray as an RGB tuple
def getRandomGray():
    brightness = random.randrange(0,255)
    return (brightness, brightness, brightness)



# COLOR MANIPULATION

# Takes a 3-element RGB tuple as input
def rgbToHex(rgb_):
    return '#%02x%02x%02x' % rgb_
