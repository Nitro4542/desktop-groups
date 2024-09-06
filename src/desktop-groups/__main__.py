from . import gui
import argparse


if __name__ == "__main__":
    # Initialize argparse
    parser = argparse.ArgumentParser(prog='DesktopGroups', description='Organizes your desktop')
    parser.add_argument('filename')
    args = parser.parse_args()

    # Open GUI
    app = gui.App(args.filename)
    app.mainloop()