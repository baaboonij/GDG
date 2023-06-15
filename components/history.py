import tkinter as tk

class HistoryScreen(tk.Toplevel):
    """A class to represent a history window."""
    def __init__(self, master=None, home_screen=None, good_deeds=[]):
        """Initialise the history screen."""
        super().__init__(master)
        self.master = master
        self.home_screen = home_screen
        self.resizable(False, False)  # Prevent the window from being resized
        self['bg'] = '#99ebff'  # Set the background colour
        self.create_widgets(good_deeds)
        self.update_idletasks()  # Update "idle" tasks to calculate widget sizes
        self.set_window_position()  # Set the position of the window

    def set_window_position(self):
        """Set the window to the same position as the home screen."""
        # Get the position of the master window
        x = self.master.winfo_x()
        y = self.master.winfo_y()

        # Set the size of the window and its position
        self.geometry(f'390x700+{x}+{y}')

    def close_window(self):
        self.home_screen.resume_timer()  # Resume the timer on the home screen
        self.home_screen.restore_home_screen()  # Show the home screen
        self.destroy()

    def create_widgets(self, good_deeds):
        """Create the widgets for the history screen."""

        # Top Section
        top_frame = tk.Frame(self, bg='#99ebff')
        top_frame.pack(fill='x')

        # Left side label
        menu_label = tk.Label(top_frame, text="Menu:", font=("Arial", 20, "bold"), bg='#99ebff', fg='black')
        menu_label.pack(side='left', padx=10, pady=10)

        # Middle title
        title_label = tk.Label(top_frame, text="History", font=("Arial", 20, "bold"), bg='#99ebff', fg='black')
        title_label.pack(side='left', padx=(75, 0), pady=10)

        # Right side close button - modified to match MenuScreen
        close_button = tk.Label(top_frame, text="x", bg='light blue', fg='black', font=("Arial", 14, "bold"), padx=10, pady=10)
        close_button.pack(side='right', padx=(0, 10), pady=(5, 0))
        close_button.bind("<Button-1>", lambda e: self.close_window())

        # Middle Section
        middle_frame = tk.Frame(self, bg='#99ebff', padx=5)
        middle_frame.pack(fill='x', pady=(5,0))

        # Display good deeds
        for deed in good_deeds:
            deed_label = tk.Label(middle_frame, text=deed, font=("Arial", 18, "bold"), bg='white', fg='black', anchor='center', padx=10, pady=10)
            deed_label.pack(fill='x', padx=10, pady=15)
