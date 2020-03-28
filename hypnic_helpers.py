# TODO:
#  A. Placeholder

# Library Imports
import random

__name__ = "hypnic_helpers"

# G L O B A L   V A R I A B L E S

# COLOR-RELATED
# The minimum value (integer from 0 to 255) for the high-value components when generating a random specific shade
MIN_HIGH_VAL = 191
MAX_LOW_VAL = 63
# The minimum value (integer from 0 to 255) for the low-value components when generating a random specific shade


# H E L P E R   F U N C T I O N S



# COLOR CONVERSION

# Takes a 3-element tuple as input
# Each value should be an integer between 0 and 255, representing the R, G, and B values for a color
# Returns the corresponding "hex code" as a string of format "#FFFFFF"
def rgbToHex(rgb):
    return '#%02x%02x%02x' % rgb

# Takes a color "hex code" as input, specifically a string of format "#FFFFFF"
# "hex" must be a 7-digit string consisting of a "#" character followed by 6 digits where each is between 0-9 or A-F
def hexToRGB(hex):
    # Credit to StackOverflow users "vallentin" and "John1024" for their elegant approach to this conversion
    # The answer can be viewed at https://stackoverflow.com/a/29643643
    # The manipulated value of hex is assigned to a second string to prevent unwanted interactions
    hexStripped = hex.lstrip("#")
    return tuple(int(hexStripped[i:i+2], 16) for i in (0, 2, 4))


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