# TODO:
#  A. Placeholder

__name__ = "hypnic_helpers"

# G L O B A L   V A R I A B L E S

# Takes a 3-element tuple as input
# Each value should be an integer between 0 and 255, representing the R, G, and B values for a color
def rgbTupleToHex(rgb):
    return '#%02x%02x%02x' % rgb