import sys
import tkinter

from PIL import Image
import customtkinter
import group


class GroupItemsScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, items: list, **kwargs):
        """
        Displays all the items in the items list
        :param master: Root frame
        :param items: List containing all items
        """
        super().__init__(master, **kwargs)

        # Prepare radio buttons
        self.radio_buttons = []
        self.radio_var = tkinter.IntVar(value=0)

        # Add buttons to frame
        for index, list_item in enumerate(items):
            radio_button = customtkinter.CTkRadioButton(self, text=list_item.get('name'), variable=self.radio_var, value=index)
            self.radio_buttons.append(radio_button)
            radio_button.grid(row=index, column=0, padx=10, pady=10, sticky="ew")


class GroupInfoFrame(customtkinter.CTkFrame):
    def __init__(self, master, icon: str, text: str, scale: float, **kwargs):
        """
        Displays logo and text of a group
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
        self.gi_title = customtkinter.CTkLabel(self, text=text)
        self.gi_title.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Configure icon
        self.img = customtkinter.CTkImage(light_image=Image.open(icon), size=((int(32 * scale)), int((32 * scale))))

        # Spawn icon
        self.gi_icon = customtkinter.CTkLabel(self, text="", image=self.img)
        self.gi_icon.grid(row=0, column=0, padx=10, pady=10, sticky="w")

class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        """
        Displays the 'Continue' and 'Cancel' button
        :param master: Root frame
        """
        super().__init__(master, **kwargs)

        # Configure grid
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Configure and place buttons
        self.continue_button = customtkinter.CTkButton(self, text="Continue", command=lambda: self.continue_button_command())
        self.continue_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=lambda: self.cancel_button_command())
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def cancel_button_command(self):
        """Closes the app when the cancel button gets pressed"""
        sys.exit(0)

    def continue_button_command(self):
        pass


class App(customtkinter.CTk, group.DGFileGroup):
    def __init__(self, dg_file):
        """
        Main window for opening a .desktopgroup file
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
        self.group_info_frame = GroupInfoFrame(self, self.icon, self.name, self.scale_factor)
        self.group_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Spawn GroupItemsFrame
        self.group_items_frame = GroupItemsScrollableFrame(self, self.items)
        self.group_items_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Spawn ButtonFrame
        self.button_frame = ButtonFrame(self)
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
        win_y = int(((self.screen_height / 2) - (self.window_height / 1.5)) * self.scale_factor) + (80 * self.scale_factor)
        return win_x, win_y

    def _window_geometry(self):
        """Creates geometry string"""
        return f'{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}'

    def _set_group_properties(self):
        """Renders the group properties"""
        self.title(self.name)

        if self.icon:
            self.iconbitmap(self.icon)