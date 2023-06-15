import tkinter as tk
import random
from components.baseScreen import BaseScreen


class MissionsScreen(BaseScreen):
    def __init__(self, master=None, home_screen=None):
        super().__init__(master, home_screen, title="Missions")
        self.good_deeds = ['Give to the poor', 'Help a neighbour', 'Help an elderly person', 'Giving a gift',
                           'Compliment somebody',
                           'Donate something', 'Visit the sick', 'Volunteer at a charity', 'Plant a tree',
                           'Resolve a conflict']
        self.options = self.generate_random_deeds()
        self.middle_frame = tk.Frame(self, bg='#99ebff', padx=5)
        self.middle_frame.pack(fill='x', pady=(5, 0))
        self.create_options()

        update_button = tk.Button(self, text='Update Missions', command=self.update_options,
                                  font=("Arial", 16, "bold"), bg='white', highlightbackground='white',
                                  highlightthickness=0)
        update_button.pack(pady=(10, 20))

    def generate_random_deeds(self):
        # Select 3 random good deeds
        return random.sample(self.good_deeds, 3)

    def create_options(self):
        # Display options
        for option in self.options:
            option_config = {
                'text': option,
                'font': ("Arial", 18, "bold"),
                'bg': 'white',
                'fg': 'black',
                'anchor': 'center',
                'padx': 10,
                'pady': 10
            }
            option_label = tk.Label(self.middle_frame, **option_config)
            option_label.pack(fill='x', padx=10, pady=15)

    def update_options(self):
        # Clear current options
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        # Generate new random options
        self.options = self.generate_random_deeds()
        # Create new options
        self.create_options()
