# TODO:
#  A. Placeholder

__name__ = "hypnic_wrapper"

# Local Inputs
import hypnic_gui

class HypnicWrapper():

    def __init__(self):
        self.gui = hypnic_gui.HypnicGUI(self)

def main():
    app = HypnicWrapper()
    app.gui.mainloop()

    # Post-run operations (garbage collection, etc.)
    del app.gui.img

main()
