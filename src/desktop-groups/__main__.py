from . import gui
import argparse


parser = argparse.ArgumentParser(
                    prog='DesktopGroups',
                    description='Organizes your desktop')
parser.add_argument('filename')
args = parser.parse_args()

app = gui.App(args.filename)
app.mainloop()