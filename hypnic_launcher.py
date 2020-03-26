# TODO:
#  A. Build a GUI launcher which allows the user to specify the following variables before launch:
#    1. GUI window dimensions
#      a. Will require changes to dimension_container.py (no longer initialize there, but potentially still store there)
#    2. CHOICE: [Shrink Images] xor [Display Fractions of Images]
#    3. File path to input image
#    4. File path at which to save output images
#      a. Maybe not, might be better to leave this until output time
#      b. A potential compromise would be for the user to define a default file path
#      c. Could also include a check box for [en/dis]abling a dialog which asks, individually, for each file saved
#   B. Launcher should be imported to and called from hypnic_wrapper.py

def main():
    print()

main()