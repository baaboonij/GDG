import tkinter as tk
from components.missions import MissionsScreen
from components.history import HistoryScreen
from components.customisepet import CustomisePetScreen
from components.settings import SettingsScreen


class Menu(tk.Toplevel):
    """A class to represent a menu window."""
    # MenuScreen constructor
    def __init__(self, master=None, home_screen=None):
        """Initialise the menu."""
        super().__init__(master)
        self.master = master
        self.home_screen = home_screen
        # Prevent the window from being resized
        self.resizable(False, False)
        # Set the background color
        self['bg'] = 'white'
        self.create_widgets()
        # Update "idle" tasks to calculate widget sizes
        self.update_idletasks()
        # Set the position of the window so when MenuScreen is open, stick to HomeScreen position
        self.set_window_position()

    def set_window_position(self):
        """Set the window to the same position as the home screen."""
        # Get the position of the master window
        x = self.master.winfo_x()
        y = self.master.winfo_y()

        # Set the size of the window and its position
        self.geometry(f'390x700+{x}+{y}')

    def handle_menu_option(self, option):
        """Handle a menu option being selected."""
        print(f'{option} selected')
        # Pause the timer
        self.home_screen.pause_timer()
        # Hide the current screen
        self.withdraw()
        # Hide the home screen
        self.master.withdraw()
        
        # Handles which screen will be shown when user clicks a Menu option
        if option == 'Missions':
            self.missions_screen = MissionsScreen(self.master, self.home_screen)
        elif option == 'Good Deed History':
            good_deeds = self.retrieve_good_deeds_history()
            self.history_screen = HistoryScreen(self.master, self.home_screen, good_deeds)  # Open the history screen
        elif option == 'Settings':
            self.settings_screen = SettingsScreen(self.master, self.home_screen)  # Open the settings screen
        elif option == 'Customise Pet':
            self.customise_pet_screen = CustomisePetScreen(self.master, self.home_screen)  # Open the customise pet screen

    def close_window(self):
        # Resume the timer on the home screen
        self.home_screen.resume_timer()
        # Show the home screen
        self.home_screen.restore_home_screen()
        self.destroy()

    def create_widgets(self):
        """Create the widgets for the menu."""
        # Create a frame for the top section of the menu
        frame_top = tk.Frame(self, bg='white')
        frame_top.pack(side='top', fill='x', padx=5, pady=5)  # Apply padding to all sides

        # Create a label for the logo and add it to the top frame
        image_logo = tk.PhotoImage(file='images/logo.png')
        # Adjust the size of the logo image
        image_logo = image_logo.subsample(5, 5)
        label_logo = tk.Label(frame_top, image=image_logo, bg='white')
        # Keep a reference to the image to prevent it from being garbage collected
        label_logo.image = image_logo
        label_logo.pack(side='left')

        # Creating a custom style for the closing menu button
        button_close = tk.Label(frame_top, text="x", bg='light blue', fg='black', font=("Arial", 14, "bold"), padx=10, pady=10)
        button_close.pack(side='right')
        # Binding a lambda function to handle user interaction
        button_close.bind("<Button-1>", lambda e: self.close_window())

        # Create a frame for the menu options
        frame_options = tk.Frame(self, bg='white')
        frame_options.pack(expand=True, fill='both')  # Center the frame

        # Create the buttons for the menu options
        self.menu_options = ['Missions', 'Good Deed History', 'Customise Pet', 'Settings', 'Logout']
        for option in self.menu_options:
            button_option = tk.Label(frame_options, text=option, bg='light blue', fg='black',
                                     font=('Arial', 18, 'bold'), anchor='center', padx=10, pady=10)
            button_option.pack(fill='x', padx=10, pady=10)
            # Binding a lambda function to handle user interaction
            button_option.bind("<Button-1>", lambda e, o=option: self.handle_menu_option(o))

    def retrieve_good_deeds_history(self):
        return self.home_screen.get_deeds_history()


if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()