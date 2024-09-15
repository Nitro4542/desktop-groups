"""
Desktop group GUI
"""
import importlib.resources
import json
import locale
import os
import subprocess
import sys
import tempfile
from tkinter import IntVar, font

from PIL import Image
from icoextract import IconExtractor, IconExtractorError
import customtkinter
from desktop_groups import group
from desktop_groups import assets

def _open_icon(icon: str):
    """Opens an icon and prepares it for PIL

    :return: Icon
    """

    if icon.endswith('.exe'):
        try:
            # Load icon
            extractor = IconExtractor(icon)

            # Read icon
            data = extractor.get_icon(num=0)

            return data

        except IconExtractorError:
            return None
    else:
        return icon


class GroupItemsScrollableFrame(customtkinter.CTkScrollableFrame):
    """
    Displays all the items in the items list
    """
    def __init__(self, master, items: list, scale: float, base_font: customtkinter.CTkFont, **kwargs):
        """
        :param master: Root frame or parent widget
        :param items: List of dictionaries, each containing an item with at least 'name' and optionally 'icon' and 'command'.
        :param scale: Scaling factor for icon size
        :param base_font: Base font to be used for the radio button text
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
                img = customtkinter.CTkImage(light_image=Image.open(_open_icon(list_item.get('icon'))),
                                             size=((int(24 * scale)), int((24 * scale)))) if list_item.get('icon') else None
                icon = customtkinter.CTkLabel(self, text='', image=img)
                icon.grid(row=index, column=0, padx=10, pady=10)
            radio_button = customtkinter.CTkRadioButton(self, text=list_item.get('name'), font=base_font,
                                                        variable=self.radio_var, value=index)
            radio_button.grid(row=index, column=1, padx=10, pady=10, sticky='ew')

    def get_command(self):
        """Returns the command associated with the selected radio button.

        :return: The command string of the selected item
        """

        return self.item_list[self.radio_var.get()].get('command')

class GroupInfoFrame(customtkinter.CTkFrame):
    """
    Displays the logo and text of a group
    """
    def __init__(self, master, icon: str, text: str, scale: float, title_font: customtkinter.CTkFont, **kwargs):
        """
        :param master: Root frame or parent widget
        :param icon: Path to the icon image file
        :param text: The name of the group to be displayed
        :param scale: Scaling factor for icon size
        :param title_font: Font to be used for the group title text
        """

        super().__init__(master, **kwargs)

        # Configure grid
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Configure and spawn text
        self.gi_title = customtkinter.CTkLabel(self, text=text.upper(), font=title_font)
        self.gi_title.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Configure icon
        self.img = customtkinter.CTkImage(light_image=Image.open(_open_icon(icon)),
                                          size=((int(32 * scale)), int((32 * scale)))) if icon else None

        # Spawn icon
        self.gi_icon = customtkinter.CTkLabel(self, text='', image=self.img)
        self.gi_icon.grid(row=0, column=0, padx=10, pady=10, sticky='w')


class ButtonFrame(customtkinter.CTkFrame):
    """
    Displays the 'Continue' and 'Cancel' button
    """
    def __init__(self, master, group_items_frame: GroupItemsScrollableFrame, base_font: customtkinter.CTkFont, lang_data: dict, **kwargs):
        """
        :param master: Root frame or parent widget
        :param group_items_frame: Instance of `GroupItemsScrollableFrame` used to get the selected command
        :param base_font: Font to be used for the button text
        :param lang_data: Langauge file JSON data
        """

        super().__init__(master, **kwargs)

        self.group_items_frame = group_items_frame
        self.lang_data = lang_data

        # Configure grid
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Configure and place buttons
        self.continue_button = customtkinter.CTkButton(self, text=self._get_continue_button_text(), font=base_font,
                                                       command=lambda: self.continue_button_command())
        self.continue_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.cancel_button = customtkinter.CTkButton(self, text=self._get_cancel_button_text(), font=base_font,
                                                     command=lambda: self.cancel_button_command())
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    def cancel_button_command(self):
        """Exits the application when the cancel button is pressed"""

        sys.exit(0)

    def continue_button_command(self):
        """Executes the command associated with the selected radio button and then exits the application"""
        subprocess.Popen(self.group_items_frame.get_command(), shell=False)
        sys.exit(0)

    def _get_continue_button_text(self):
        """Sets the continue button text according to the system language

        :return: 'Continue' in selected language
        """

        return self.lang_data.get('gui.continue')

    def _get_cancel_button_text(self):
        """Sets the cancel button text according to the system language

        :return: 'Continue' in selected language
        """

        return self.lang_data.get('gui.cancel')

class App(customtkinter.CTk, group.DGFileGroup):
    """
    Main window for opening a desktop group file
    """
    def __init__(self, dg_file: str, theme: str = None):
        """
        :param dg_file: Path to the desktop group file containing the group data
        :param theme: Optional path to a theme file to be used for styling the application
        """

        # Initialize CustomTkinter
        customtkinter.CTk.__init__(self)

        # Initialize DGFileGroup
        group.DGFileGroup.__init__(self, dg_file)

        # Set window properties
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # Set properties from group file
        self._set_group_properties()

        # Set theme
        if theme:
            customtkinter.set_default_color_theme(theme)

        # Set language
        self._set_language()

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

        # Build layout
        self._build_layout()

    def _build_layout(self):
        """Builds app layout"""

        # Spawn GroupInfoFrame
        self.group_info_frame = GroupInfoFrame(self, self.icon, self.name, self.scale_factor, self.title_font)
        self.group_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Spawn GroupItemsFrame
        self.group_items_frame = GroupItemsScrollableFrame(self, self.items, self.scale_factor, self.base_font)
        self.group_items_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Spawn ButtonFrame
        self.button_frame = ButtonFrame(self, self.group_items_frame, self.base_font, self.lang_data)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    def _set_geometry(self):
        """Sets the window geometry, centers the window on the screen, and applies the scaling factor"""

        # Get screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Calculate window position
        self.window_x, self.window_y = self._calculate_window_position()

        # Set window geometry
        self.geometry(self._window_geometry())

    def _calculate_window_position(self):
        """Calculates the position of the window to center it on the screen, considering the scaling factor.

        :return: A tuple (x, y) representing the position of the window
        """

        win_x = int(((self.screen_width / 2) - (self.window_width / 2)) * self.scale_factor)
        win_y = (int(((self.screen_height / 2) - (self.window_height / 1.5)) * self.scale_factor) +
                 (80 * self.scale_factor))
        return win_x, win_y

    def _window_geometry(self):
        """Creates a string representing the window geometry (size and position)

        :return: A geometry string in the format 'widthxheight+x+y'.
        """

        return f'{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}'

    def _set_group_properties(self):
        """Sets the window title and icon based on the group properties. Uses a default icon if none is provided."""

        self.title(self.name)

        if self.icon:
            self.iconbitmap(self.icon)
        else:
            # Use default icon as fallback
            inp_file = importlib.resources.files(assets) / 'img/desktopgroups256px.ico'
            with inp_file.open('rb') as default_icon:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.ico') as tmp_file:
                    tmp_file.write(default_icon.read())
                    tmp_file.flush()
                    icon_path = tmp_file.name

                    self.iconbitmap(icon_path)

                    def on_close():
                        os.remove(icon_path)
                        self.destroy()

                    self.protocol("WM_DELETE_WINDOW", on_close)

    def _create_font_objects(self):
        """Creates font objects for base text and titles using the system default font"""

        # Get system font
        default_font = font.nametofont('TkDefaultFont')

        # Create objects
        self.base_font = customtkinter.CTkFont(default_font.cget('family'))
        self.title_font = customtkinter.CTkFont(default_font.cget('family'), 22, 'bold')

    def _set_language(self):
        """Loads the language file"""

        if os.name == 'nt':
            try:
                from ctypes import windll
                lang_id = windll.kernel32.GetUserDefaultUILanguage()
                self.lang_code = locale.windows_locale.get(lang_id, 'en')
            except:
                self.lang_code = 'en'
        elif os.name == 'posix':
            try:
                language = locale.getdefaultlocale()
                self.lang_code = language[0]
            except:
                self.lang_code = 'en'
        else:
            self.lang_code = 'en'

        self.split_lang_code = self.lang_code.split('_')[0]

        try:
            inp_file = importlib.resources.files(assets) / f'lang/{self.split_lang_code}.json'
            with inp_file.open('rt') as lang_file:
                self.lang_data = json.load(lang_file)
        except:
            inp_file = importlib.resources.files(assets) / 'lang/en.json'
            with inp_file.open('rt') as lang_file:
                self.lang_data = json.load(lang_file)
