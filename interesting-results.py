# _________________________________________________
# INTERESTING IMAGE FILTERS FOR RGBFUNC
# This file will contain subjectively interesting results I've found through experimentation,
#     as well as a description of those results to the best of my ability
# The goal of this endeavor is to help me determine the "usefulness" of different pixel modification functions, and
#     from that information make decisions about changes to make and new modification functions to implement
#
# Perhaps someone else will find it useful at some point if they're ever playing around with this code.
# _________________________________________________

# NUMBER 001
# Creates a vertical rainbow gradient
"""
elif manip_index == 3:
    rgbResult = self.modHueShift(rgbResult, self.currentY)
"""

# NUMBER 002
# Creates a horizontal rainbow gradient
"""
elif manip_index == 4:
    rgbResult = self.modHueShift(rgbResult, self.currentX)
"""

# NUMBER 003
# Brightens images significantly
"""
elif manip_index == 7:
    rgbResult = self.modValueShift(rgbResult, 0.3)
"""

# NUMBER 004
# Has weird effects on extremely deepening/limiting colors. Not sure how else to describe it but it's worth saving.
"""
elif manip_index == 8:
    rgbResult = self.modSaturationShift(rgbResult, -0.3)
"""

# NUMBER 005
# This single manipulation creates a series of triangle-shaped rainbow gradients,
#     increasing in angle as Y increases
"""
if manip_index == 1:
    rgbResult = self.modHueShift(rgbResult, ((self.currentX + 1) % (self.currentY + 1)) % 360)
"""

# NUMBER 006
# This single manipulation creates a look similar to an old overexposed silver nitrate image from the 19th century
"""
if manip_index == 6:
    rgbResult = (self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 19, 0, 32, 1),
                 self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 39, 0, 32, 1),
                 self.calcFromCustomDomainRGB(rgbResult[2], 127, 128, 29, 0, 32, 1))
"""