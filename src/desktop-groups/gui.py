"""
Desktop group GUI
"""
import subprocess
import sys
from tkinter import IntVar, font

from PIL import Image
import customtkinter
from . import group


class GroupItemsScrollableFrame(customtkinter.CTkScrollableFrame):
    """
    Displays all the items in the items list
    """
    def __init__(self, master, items: list, scale: float, base_font: customtkinter.CTkFont, **kwargs):
        """
        :param master: Root frame
        :param items: List containing all items
        """
        super().__init__(master, **kwargs)

        self.item_list = items

        # Configure grid
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Prepare radio buttons
        self.radio_var = IntVar(value=0)

        # Add buttons to frame
        for index, list_item in enumerate(self.item_list):
            if list_item.get('icon'):
                img = customtkinter.CTkImage(light_image=Image.open(list_item.get('icon')),
                                             size=((int(24 * scale)), int((24 * scale))))
                icon = customtkinter.CTkLabel(self, text="", image=img)
                icon.grid(row=index, column=0, padx=10, pady=10)
            radio_button = customtkinter.CTkRadioButton(self, text=list_item.get('name'), font=base_font,
                                                        variable=self.radio_var, value=index)
            radio_button.grid(row=index, column=1, padx=10, pady=10, sticky="ew")

    def get_command(self):
        """Returns the command of the selected radio button"""
        return self.item_list[self.radio_var.get()].get('command')


class GroupInfoFrame(customtkinter.CTkFrame):
    """
    Displays logo and text of a group
    """
    def __init__(self, master, icon: str, text: str, scale: float, title_font: customtkinter.CTkFont, **kwargs):
        """
        :param master: Root frame
        :param icon: Path to icon
        :param text: Name of group
        :param scale: Window scaling
        """
        super().__init__(master, **kwargs)

        # Configure grid
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Configure and spawn text
        self.gi_title = customtkinter.CTkLabel(self, text=text.upper(), font=title_font)
        self.gi_title.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Configure icon
        self.img = customtkinter.CTkImage(light_image=Image.open(icon), size=((int(32 * scale)), int((32 * scale))))

        # Spawn icon
        self.gi_icon = customtkinter.CTkLabel(self, text="", image=self.img)
        self.gi_icon.grid(row=0, column=0, padx=10, pady=10, sticky="w")

class ButtonFrame(customtkinter.CTkFrame):
    """
    Displays the 'Continue' and 'Cancel' button
    """
    def __init__(self, master, group_items_frame: GroupItemsScrollableFrame, base_font: customtkinter.CTkFont, **kwargs):
        """
        :param master: Root frame
        """
        super().__init__(master, **kwargs)

        self.group_items_frame = group_items_frame

        # Configure grid
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Configure and place buttons
        self.continue_button = customtkinter.CTkButton(self, text="Continue", font=base_font,
                                                       command=lambda: self.continue_button_command())
        self.continue_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", font=base_font,
                                                     command=lambda: self.cancel_button_command())
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def cancel_button_command(self):
        """Closes the app when the cancel button gets pressed"""
        sys.exit(0)

    def continue_button_command(self):
        """Opens the desired command selected by the radio buttons"""
        subprocess.Popen(self.group_items_frame.get_command(), shell=False)
        sys.exit(0)


class App(customtkinter.CTk, group.DGFileGroup):
    """
    Main window for opening a .desktopgroup file
    """
    def __init__(self, dg_file: str):
        """
        :param dg_file: .desktopgroup file
        """
        # Initialize CustomTkinter
        customtkinter.CTk.__init__(self)

        # Initialize DGFileGroup
        group.DGFileGroup.__init__(self, dg_file)

        # Configure window
        self._configure_window()

        # Build layout
        self._build_layout()

    def _build_layout(self):
        """Builds app layout"""

        # Spawn GroupInfoFrame
        self.group_info_frame = GroupInfoFrame(self, self.icon, self.name, self.scale_factor, self.title_font)
        self.group_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Spawn GroupItemsFrame
        self.group_items_frame = GroupItemsScrollableFrame(self, self.items, self.scale_factor, self.base_font)
        self.group_items_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Spawn ButtonFrame
        self.button_frame = ButtonFrame(self, self.group_items_frame, self.base_font)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def _configure_window(self):
        """Configures window"""

        # Set window properties
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # Set properties from group file
        self._set_group_properties()

        # Define window dimensions
        self.window_width = 500
        self.window_height = 800
        self.scale_factor = self._get_window_scaling()

        # Configure grid
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        self.columnconfigure(0, weight=1)

        # Set window geometry
        self._set_geometry()

        # Create font objects
        self._create_font_objects()


    def _set_geometry(self):
        """Sets window geometry and centers window on screen"""

        # Get screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Calculate window position
        self.window_x, self.window_y = self._calculate_window_position()

        # Set window geometry
        self.geometry(self._window_geometry())

    def _calculate_window_position(self):
        """Calculates window position"""
        win_x = int(((self.screen_width / 2) - (self.window_width / 2)) * self.scale_factor)
        win_y = (int(((self.screen_height / 2) - (self.window_height / 1.5)) * self.scale_factor) +
                 (80 * self.scale_factor))
        return win_x, win_y

    def _window_geometry(self):
        """Creates geometry string"""
        return f'{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}'

    def _set_group_properties(self):
        """Renders the group properties"""
        self.title(self.name)

        if self.icon:
            self.iconbitmap(self.icon)

    def _create_font_objects(self):
        """Creates objects for different font types"""

        # Get system font
        default_font = font.nametofont("TkDefaultFont")

        # Create objects
        self.base_font = customtkinter.CTkFont(default_font.cget('family'))
        self.title_font = customtkinter.CTkFont(default_font.cget('family'), 22, "bold")
