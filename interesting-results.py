# _________________________________________________
# INTERESTING IMAGE FILTERS FOR RGBFUNC
# This file will contain subjectively interesting results I've found through experimentation,
#     as well as a description of those results to the best of my ability
# The goal of this endeavor is to help me determine the "usefulness" of different pixel modification functions, and
#     from that information make decisions about changes to make and new modification functions to implement
# _________________________________________________

# NUMBER 001
# This single manipulation creates a series of triangle-shaped rainbow gradients,
#     increasing in angle as Y increases
"""
    if manip_index == 1:
        rgbResult = self.modHueShift(rgbResult, ((self.currentX + 1) % (self.currentY + 1)) % 360)
"""

# NUMBER 002
# This single manipulation creates a look similar to an old overexposed silver nitrate image from the 19th century
"""
rgbResult = self.pixelsIn[self.currentX, self.currentY]
if manip_index == 1:
    rgbResult = (self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 19, 0, 32, 1),
                 self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 39, 0, 32, 1),
                 self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 29, 0, 32, 1))
"""

