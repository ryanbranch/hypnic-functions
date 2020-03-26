__name__ = "hypnic_wrapper"

import hypnic_gui

class HypnicWrapper():

    def __init__(self):
        self.gui = hypnic_gui.HypnicGUI(self)

def main():
    app = HypnicWrapper()
    app.gui.mainloop()

main()