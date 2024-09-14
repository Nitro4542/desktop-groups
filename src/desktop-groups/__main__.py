"""
Main part of desktop-groups module
"""
import argparse
from . import gui


if __name__ == '__main__':
    # Initialize argparse and add arguments
    parser = argparse.ArgumentParser(prog='DesktopGroups', description='Organizes your desktop')
    parser.add_argument('filename', type=str, help='Path to desktopgroup file')
    parser.add_argument('--theme', type=str, help='Path to a theme file (optional)')
    args = parser.parse_args()

    # Open GUI
    app = gui.App(args.filename, args.theme)
    app.mainloop()
