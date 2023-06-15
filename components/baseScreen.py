import tkinter as tk

# DRY Approach
class BaseScreen(tk.Toplevel):
    """The base class of the common attributes of the Screens e.g. Missions, Settings etc."""
    # BaseScreen Constructor
    def __init__(self, master=None, home_screen=None, title=""):
        """Initialise the screen."""
        super().__init__(master)
        self.master = master
        self.home_screen = home_screen
        self.title_text = title
        # Prevent the window from being resized
        self.resizable(False, False)
        # Set the background color
        self['bg'] = '#99ebff'
        self.create_widgets()
        # Update "idle" tasks to calculate widget sizes
        self.update_idletasks()
        # Set the position of the window
        self.set_window_position()

    def set_window_position(self):
        """Set the window to the same position as the home screen."""
        # Get the position of the master window
        x = self.master.winfo_x()
        y = self.master.winfo_y()

        # Set the size of the window and its position
        self.geometry(f'390x700+{x}+{y}')

    def close_window(self):
        # Resume the timer on the home screen
        self.home_screen.resume_timer()
        # Show the home screen
        self.home_screen.restore_home_screen()
        self.destroy()

    def create_widgets(self):
        """Create the widgets for the screen."""
        # Top Section
        frame_top = tk.Frame(self, bg='#99ebff')
        frame_top.pack(fill='x')

        # Left side label
        menu_label = tk.Label(frame_top, text="Menu:", font=("Arial", 20, "bold"), bg='#99ebff', fg='black')
        menu_label.pack(side='left', padx=10, pady=10)

        # Middle title
        label_title = tk.Label(frame_top, text=self.title_text, font=("Arial", 20, "bold"), bg='#99ebff', fg='black')
        label_title.pack(side='left', padx=(75, 0), pady=10)

        # Right side close button
        button_close = tk.Label(frame_top, text="x", bg='light blue', fg='black', font=("Arial", 14, "bold"), padx=10, pady=10)
        button_close.pack(side='right', padx=(0, 20))
        # Binding a lambda function to handle user interaction
        button_close.bind("<Button-1>", lambda e: self.close_window())

