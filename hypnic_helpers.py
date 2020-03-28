# TODO:
#  A. Placeholder

__name__ = "hypnic_helpers"

# G L O B A L   V A R I A B L E S

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
    return (tuple(int(hexStripped[i:i+2], 16) for i in (0, 2, 4)))