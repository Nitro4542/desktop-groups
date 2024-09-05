import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("DesktopGroups")

        # Define window dimensions
        self.window_width = 500
        self.window_height = 800
        self.scale_factor = self._get_window_scaling()

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
        win_y = int(((self.screen_height / 2) - (self.window_height / 1.5)) * self.scale_factor) + (
                    80 * self.scale_factor)
        return win_x, win_y

    def _window_geometry(self):
        """Creates the geometry string"""
        return f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}"