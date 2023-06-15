import tkinter as tk
import time
import pygame

from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from components.dbService import DatabaseService
from components.menu import Menu
from components.login import LoginScreen


class HomeScreen:
    # Default values for class attributes
    DEFAULT_HAPPINESS_METER = 50
    DEFAULT_GOOD_DEEDS_HISTORY = []
    DEFAULT_DRAIN_DELAY = 5

    def __init__(self, username=None):
        """Username sourced from LoginScreen when HomeScreen was initialised"""
        self.username = username
        self.dbService = DatabaseService()
        self.initialise_values()
        self.load_user_data()
        self.initialise_window()
        self.set_pet_mood()
        self.initialise_audio()
        self.draw_home_screen()

    def initialise_values(self):
        """Initialises the values of all the factors at startup"""
        self.timer_paused = False
        self.meter_event_id = None
        self.last_good_deed_time = None
        self.drain_delay = self.DEFAULT_DRAIN_DELAY
        self.remaining_drain_delay = self.drain_delay
        self.happiness_meter = self.DEFAULT_HAPPINESS_METER
        self.good_deeds_history = self.DEFAULT_GOOD_DEEDS_HISTORY
        self.pet_states = None
        self.accessory = 'None'
        self.colour = 'None'

    def load_user_data(self):
        """Loads the user's data from the database"""
        user_data = self.dbService.get_user_activity(self.username)
        if user_data:
            self.happiness_meter = user_data["happiness_meter"]
            self.good_deeds_history = user_data["good_deeds_history"]

    def initialise_window(self):
        self.initialise_window()
        self.meter_event_id = self.window.after(5000, self.start_draining_meter)

    def initialise_audio(self):
        """Defaults to sound on"""
        self.sound_on = True

    def initialise_window(self):
        """initialise the main window."""
        self.window = tk.Tk()
        self.window.geometry('390x700')
        self.window.configure(bg='#99ebff')
        self.window.title('Home - projectGDG')
        self.window.resizable(False, False)
        self.label_pet_image = tk.Label(self.window, bg="#99ebff")

    def initialise_pet_moods(self):
        """initialise the images of the pet without the sunglasses."""
        self.pet_states = {}
        for state in ['neutral', 'sad', 'happy']:
            pet_image = Image.open(f'images/None-pet-{state}.png')

            # Resize the pet image
            pet_image_size = (178, 243)  # adjust as necessary
            pet_image = pet_image.resize(pet_image_size, Image.ANTIALIAS)

            pet_image_photo = ImageTk.PhotoImage(pet_image)
            self.pet_states[state] = pet_image_photo

    def current_user(self):
        return self.username

    def draw_home_screen(self):
        """Draw the elements on the home screen."""
        self.draw_username_label()
        self.draw_menu_button()
        self.draw_daily_mission_label()
        self.set_pet_mood()
        self.draw_meter_bar()
        self.draw_input_and_button()

    def run(self):
        """Run the tkinter main event loop."""
        self.window.mainloop()

    def draw_username_label(self):
        """Draw the label with the username."""
        frame_username = tk.Frame(self.window, bg='#99ebff')
        frame_username.grid(row=0, column=0, sticky='w', padx=(20, 10), pady=(20, 10))
        username_title = tk.Label(frame_username, text="Username:", font=("Arial", 16), bg='#99ebff', fg='black')
        username_title.pack(side="left")
        username_label = tk.Label(frame_username, text=self.username, font=("Arial", 18, "bold"), bg='#99ebff',
                                  fg='black')
        username_label.pack(side="left")

    def draw_menu_button(self):
        """Draw the menu button."""
        button_menu = tk.Button(self.window, text="Menu", command=self.show_menu, font=("Arial", 16, "bold"),
                                bg='white', highlightbackground='white', highlightthickness=0)
        button_menu.grid(row=0, column=1, sticky='e', padx=(10, 20), pady=(20, 10))

    def draw_daily_mission_label(self):
        """Draw the label for the daily mission."""
        label_daily_missions = tk.Label(self.window, text="Good Deeds Gamified", bg='#99ebff', fg='black',
                                        font=("Arial", 20), highlightbackground='white',
                                        highlightthickness=15)
        label_daily_missions.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(30, 15), padx=(50, 50))

    def draw_pet_image(self, state):
        """Draw the image of the pet with the given state."""
        # Verify that pet_states is not None before using it
        if self.pet_states is None:
            return

        pet_image = self.pet_states[state]

        self.label_pet_image.configure(image=pet_image)
        self.label_pet_image.image = pet_image  # Keep a reference to the image

        self.label_pet_image.grid(row=3, column=0, columnspan=2, sticky='nsew')
        self.label_pet_image.bind("<Button-1>", self.on_pet_image_click)  # Bind a click event to the label

    def on_pet_image_click(self, event):
        """Play petting_sound when the pet image is clicked"""
        self.play_petting_sound()

    def draw_meter_bar(self):
        """Draw the meter bar."""
        self.meter_bar = ttk.Progressbar(self.window, length=220, mode='determinate', orient='vertical',
                                         style="TProgressbar")
        self.meter_bar.grid(row=3, column=0, columnspan=2, sticky='w', padx=(20, 10), pady=(15, 15))
        self.meter_bar['value'] = self.happiness_meter
        self.window.style = ttk.Style()
        self.window.style.configure("TProgressbar", thickness=30)

    def draw_input_and_button(self):
        """Draw the input field and the submit button."""
        frame_input = tk.Frame(self.window, bg='#99ebff')
        frame_input.place(x=0, y=500, width=390, height=150)
        self.user_input = tk.StringVar()
        label_input = tk.Label(frame_input, text="Enter good deed:", font=("Arial", 16), bg='white', fg='black')
        label_input.pack(pady=10, padx=20)
        entry_input = tk.Entry(frame_input, width=30, textvariable=self.user_input, fg='black')
        entry_input.pack(padx=20)

        # Once the user submits a good deed, wait 5 seconds before updating meter
        button_input = ttk.Button(frame_input, text="Submit", command=self.prepare_to_update_meter)
        button_input.pack(pady=10, padx=20)

    def show_menu(self):
        """Show the menu window and disable the home screen."""
        # Pause the timer to stop drain
        self.pause_timer()
        # Hide the home screen
        self.window.withdraw()
        # Open Menu Screen
        self.menu_window = Menu(self.window, self)
        # If a good deed has been submitted
        if self.last_good_deed_time is not None:
            # Calculate elapsed time
            elapsed_time = time.time() - self.last_good_deed_time
            # Update the remaining drain delay
            self.remaining_drain_delay = max(self.remaining_drain_delay - elapsed_time, 0)

    def restore_home_screen(self):
        """Restore the home screen after the menu is closed."""
        # Show the home screen
        self.window.deiconify()

    def set_pet_mood(self):
        """Set the mood of the pet based on happiness meter."""
        if self.pet_states is None:
            self.initialise_pet_moods()
        if self.happiness_meter < 25:
            self.draw_pet_image('sad')
        elif self.happiness_meter < 66:
            self.draw_pet_image('neutral')
        else:
            self.draw_pet_image('happy')

    def change_pet_accessory(self, accessory):
        """Change the pet's accessory."""
        self.accessory = accessory  # Store the selected accessory
        if accessory == 'Sunglasses':
            self.apply_sunglasses()  # Apply the sunglasses accessory
        elif accessory == 'None':
            self.remove_sunglasses()  # Remove the sunglasses
        else:
            self.set_pet_mood()  # Redraw the pet without any accessory
        self.set_pet_mood()

    def apply_sunglasses(self):
        """Apply sunglasses to the pet's images."""
        # Only apply sunglasses if the accessory is 'Sunglasses'
        if self.accessory == 'Sunglasses':
            # Load your overlay image using PIL
            overlay = Image.open('images/sunglasses.png')

            # Resize the overlay image
            overlay_size = (100, 50)
            overlay = overlay.resize(overlay_size, Image.ANTIALIAS)

            # Then for each pet state, open the image, paste the overlay, and save the result
            for state in ['neutral', 'sad', 'happy']:
                # Open the pet image with current colour
                pet_image = Image.open(f'images/{self.colour}-pet-{state}.png').convert("RGBA")

                # Resize the pet image
                pet_image_size = (178, 243)
                pet_image = pet_image.resize(pet_image_size, Image.ANTIALIAS)

                # Apply the overlay
                pet_image.paste(overlay, (38, 41), overlay)

                # Save the result to a PhotoImage and add it to pet_states
                pet_image_photo = ImageTk.PhotoImage(pet_image)
                self.pet_states[state] = pet_image_photo

    def remove_sunglasses(self):
        """Remove sunglasses from the pet's images."""
        if self.accessory == 'None':
            # Re-initialises the pet's moods with current colour and no accessory
            self.pet_states = {
                'neutral': PhotoImage(file=f'images/{self.colour}-pet-neutral.png').subsample(2, 2),
                'sad': PhotoImage(file=f'images/{self.colour}-pet-sad.png').subsample(2, 2),
                'happy': PhotoImage(file=f'images/{self.colour}-pet-happy.png').subsample(2, 2)
            }
            self.set_pet_mood()

    def change_pet_colour(self, colour):
        """Change the colour of the pet."""
        if colour == 'Default':
            colour = 'None'

        self.colour = colour  # Stores the selected colour

        # Adjusts the pet states according to the colour
        self.pet_states = {
            'neutral': PhotoImage(file=f'images/{colour}-pet-neutral.png').subsample(2, 2),
            'sad': PhotoImage(file=f'images/{colour}-pet-sad.png').subsample(2, 2),
            'happy': PhotoImage(file=f'images/{colour}-pet-happy.png').subsample(2, 2)
        }

        # Reapplies sunglasses if accessory is 'Sunglasses'
        if self.accessory == 'Sunglasses':
            self.apply_sunglasses()

        self.set_pet_mood()

    def change_background_colour(self, colour):
        """Change the background colour of pet image label."""
        self.label_pet_image.configure(bg=colour)

    pygame.mixer.init()

    def play_reward_sound(self):
        pygame.mixer.music.load("audio/reward.mp3")
        pygame.mixer.music.play()

    def play_petting_sound(self):
        pygame.mixer.music.load("audio/petting.mp3")
        pygame.mixer.music.play()

    def mute_sound(self):
        pygame.mixer.music.set_volume(0)
        self.sound_on = False

    def unmute_sound(self):
        pygame.mixer.music.set_volume(1.0)
        self.sound_on = True

    def handle_menu_option(self, option):
        """Handle the Logout menu option."""
        # Quits the app
        if option == 'Logout':
            self.dbService.save_user_activity(self.username, self.happiness_meter, self.good_deeds_history)
            # Close the database connection
            self.dbService.close()
            # Destroy the current HomeScreen instance
            self.window.destroy()

            # Show the LoginScreen
            login_screen = LoginScreen()
            login_screen.run()

    def start_draining_meter(self):
        """Stop the scheduled meter event and schedule a new one."""
        if self.meter_event_id is not None:
            self.window.after_cancel(self.meter_event_id)
        if not self.timer_paused:
            self.meter_event_id = self.window.after(5000, self.update_meter)

    def prepare_to_update_meter(self):
        """Update the database and prepare to update the meter."""
        user_input = self.user_input.get().strip()
        if user_input:  # Check if the input is not empty
            self.update_database_and_meter()
            if self.meter_event_id is not None:
                self.window.after_cancel(self.meter_event_id)
            self.last_good_deed_time = time.time()  # Record the time of the good deed submission
            self.remaining_drain_delay = self.drain_delay  # Reset the remaining drain delay
            if not self.timer_paused:
                self.meter_event_id = self.window.after(int(self.remaining_drain_delay * 1000),
                                                        self.start_draining_meter)
            self.play_reward_sound()  # Play reward_sound when a good deed is submitted

    def pause_timer(self):
        """Pause the timer."""
        self.timer_paused = True
        if self.meter_event_id is not None:
            self.window.after_cancel(self.meter_event_id)

    def resume_timer(self):
        """Resume the timer."""
        self.timer_paused = False
        if not self.timer_paused:
            self.meter_event_id = self.window.after(int(self.remaining_drain_delay * 1000), self.start_draining_meter)

    def start_delay(self):
        """Start the delay after user input before starting to drain the meter."""
        if not self.timer_paused:
            # After submitting a good deed, wait 5 seconds before starting to drain the meter again
            self.meter_event_id = self.window.after(5000, self.start_draining_meter)

    def update_database_and_meter(self):
        """Update the database and the meter based on the user's input."""
        user_input = self.user_input.get().strip()
        if user_input:
            self.user_input.set("")
            self.happiness_meter = min(self.happiness_meter + 10, 100)

            # Add the good deeds to the good_deeds_history list
            self.good_deeds_history.append(user_input)
            print(f'Good deeds history after update: {self.good_deeds_history}')

            # Save user activity to the database
            self.dbService.save_user_activity(self.username, self.happiness_meter, self.good_deeds_history)

            # Update the meter immediately after updating the value
            self.meter_bar['value'] = self.happiness_meter
            if self.happiness_meter < 25:
                self.draw_pet_image('sad')
            elif self.happiness_meter < 66:
                self.draw_pet_image('neutral')
            else:
                self.draw_pet_image('happy')

            # Only cancel the current meter event and schedule a new one if the user input is not empty
            if self.meter_event_id is not None:
                self.window.after_cancel(self.meter_event_id)
            # After submitting a good deed, wait 5 seconds before starting to drain the meter again
            self.meter_event_id = self.window.after(5000, self.start_draining_meter)

    def update_meter(self):
        """Update the meter value and the pet image based on the time since the last input."""
        self.happiness_meter = max(self.happiness_meter - 1, 0)

        # Update the pet mood based on updated happiness meter
        self.set_pet_mood()

        self.meter_bar['value'] = self.happiness_meter
        # Update the meter every second
        if not self.timer_paused:  # only update meter if not paused
            self.meter_event_id = self.window.after(1000, self.update_meter)

    def get_deeds_history(self):
        """Gets the good deeds history"""
        deeds = self.good_deeds_history[-7:]
        print(f'Getting last 7 deeds: {deeds}')
        return deeds


if __name__ == "__main__":
    app = HomeScreen("Username")
    app.run()
