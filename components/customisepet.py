import tkinter as tk
from components.baseScreen import BaseScreen


class CustomisePetScreen(BaseScreen):
    def __init__(self, master=None, home_screen=None):
        super().__init__(master, home_screen, title="Customise")
        self.options = ['Colour', 'Accessories', 'Background']
        self.home_screen = home_screen  # Save reference to home screen
        self.create_options()

    def create_options(self):
        """Creates and displays the options of customisation"""
        # Middle Section
        middle_frame = tk.Frame(self, bg='#99ebff', padx=5)
        middle_frame.pack(fill='x', pady=(5, 0))

        # Display options
        for option in self.options:
            if option == 'Colour':
                option_button = tk.Button(middle_frame, text=option, font=("Arial", 18, "bold"), bg='white', fg='black',
                                          anchor='center', padx=10, pady=10, command=self.create_colour_options)
                option_button.pack(fill='x', padx=10, pady=15)
            elif option == 'Background':
                option_button = tk.Button(middle_frame, text=option, font=("Arial", 18, "bold"), bg='white', fg='black',
                                          anchor='center', padx=10, pady=10, command=self.create_background_options)
                option_button.pack(fill='x', padx=10, pady=15)
            elif option == 'Accessories':
                option_button = tk.Button(middle_frame, text=option, font=("Arial", 18, "bold"), bg='white', fg='black',
                                          anchor='center', padx=10, pady=10, command=self.create_accessory_options)
                option_button.pack(fill='x', padx=10, pady=15)
            else:
                option_label = tk.Label(middle_frame, text=option, font=("Arial", 18, "bold"), bg='white', fg='black',
                                        anchor='center', padx=10, pady=10)
                option_label.pack(fill='x', padx=10, pady=15)

    def create_colour_options(self):
        """Creates and displays the options for the pet colour"""
        colour_options_window = tk.Toplevel(self)
        colour_options_window.title("Select Colour")

        colour_options = ['Default', 'Red', 'Blue', 'Green']
        for colour in colour_options:
            colour_button = tk.Button(colour_options_window, text=colour, font=("Arial", 18, "bold"), bg='white',
                                      fg='black', anchor='center', padx=10, pady=10,
                                      command=lambda c=colour: self.change_pet_colour(c))
            colour_button.pack(fill='x', padx=10, pady=15)

    def change_pet_colour(self, colour):
        """Changes the colour of the pet."""
        if self.home_screen:
            self.home_screen.change_pet_colour(colour)

    def create_background_options(self):
        """Creates and displays the options for the background colour"""
        background_options_window = tk.Toplevel(self)
        background_options_window.title("Select Background Colour")

        background_options = ['Blue', 'Red', 'Green', 'White', 'Black']
        for colour in background_options:
            colour_button = tk.Button(background_options_window, text=colour, font=("Arial", 18, "bold"), bg='white',
                                     fg='black', anchor='center', padx=10, pady=10,
                                     command=lambda c=colour: self.change_background_colour(c))
            colour_button.pack(fill='x', padx=10, pady=15)

    def change_background_colour(self, colour):
        """Changes the background colour."""
        colour_dict = {'Blue': '#99ebff', 'Red': '#FF0000', 'Green': '#008000', 'White': '#FFFFFF', 'Black': '#000000'}
        if colour in colour_dict:
            if self.home_screen:
                self.home_screen.change_background_colour(colour_dict[colour])

    def create_accessory_options(self):
        """Creates and displays the accessory options"""
        accessory_options_window = tk.Toplevel(self)
        accessory_options_window.title("Select Accessory")
        accessory_options = ['None', 'Sunglasses']
        for accessory in accessory_options:
            accessory_button = tk.Button(accessory_options_window, text=accessory, font=("Arial", 18, "bold"),
                                         bg='white',
                                         fg='black', anchor='center', padx=10, pady=10,
                                         command=lambda a=accessory: self.change_pet_accessory(a))
            accessory_button.pack(fill='x', padx=10, pady=15)

    def change_pet_accessory(self, accessory):
        """Changes the pet's accessory."""
        self.home_screen.change_pet_accessory(accessory)

