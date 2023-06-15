# login.py
import tkinter as tk
from tkinter import ttk, PhotoImage
import bcrypt
from components.setup import SetupScreen
from components.dbService import DatabaseService

class LoginScreen:
    # LoginScreen Constructor
    def __init__(self):
        # Initialising the Tkinter window
        self.window = tk.Tk()
        self.window.geometry('390x700')
        self.window.configure(bg='white')
        self.window.title('Login')

        # Creating a database service instance
        self.dbService = DatabaseService()

        # Drawing the header and login form UI
        self.draw_title_logo_section()
        self.draw_login_form_section()

    def run(self):
        # Starting the Tkinter event loop
        self.window.mainloop()

    def draw_title_logo_section(self):
        # Drawing the header with the brand logo
        header_title = tk.Label(self.window, text="Good Deeds Gamified", font=("Helvetica", 26), bg='black', fg='white')
        header_title.pack(pady=20, padx=15) 

        image_logo = PhotoImage(file='images/logo.png')
        # Resize the logo image (this requires the Pillow library)
        image_logo = image_logo.subsample(3, 3)  # decrease size

        # Creating a label for the logo to be placed to remove default styles
        label_logo = tk.Label(self.window, image=image_logo, bg='white') # Use same bg as app
        label_logo.image = image_logo  # keep a reference to the image to prevent it from being garbage collected
        label_logo.pack(pady=5)

    def draw_login_form_section(self):
        # Drawing the login form
        frame_login_form = ttk.Frame(self.window, padding="20 10 20 10")
        frame_login_form.pack(pady=3)

        # Creating and arranging the Username label and entry box
        label_username = ttk.Label(frame_login_form, text='Username:')
        label_username.grid(row=0, column=0, sticky='W')
        self.entry_username = ttk.Entry(frame_login_form)
        self.entry_username.grid(row=0, column=1, sticky='E', padx=5, pady=5)

        # Creating and arranging the Password label and entry box
        password_label = ttk.Label(frame_login_form, text='Password:')
        password_label.grid(row=1, column=0, sticky='W', padx=5, pady=5)
        self.entry_password = ttk.Entry(frame_login_form, show="*")
        self.entry_password.grid(row=1, column=1, sticky='E', padx=5, pady=5)

        # Creating the error label for invalid login credentials
        self.label_error_invalid = ttk.Label(frame_login_form, text='', foreground='red')
        self.label_error_invalid.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Creating the Login and Sign Up buttons
        button_login = ttk.Button(frame_login_form, text='Login', command=self.login)
        button_login.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        button_signup = ttk.Button(frame_login_form, text='Sign Up', command=self.signup)
        button_signup.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        from components.home import HomeScreen

        # Retrieve user input from username and password fields
        # Removing white-space at the beginning and at the end of the String
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        # Query the DB to see if a user exists with that username
        user = self.dbService.get_user(username)

        # If the user exists and the entered password matches, destroy the window and open the home screen
        # bcrypt checkpw function compares a hashed password version User has entered with the hashed password in DB
        if user and bcrypt.checkpw(password.encode(), user['password']):
            # self.dbService.create_user_activity_table()
            self.window.destroy()
            home_screen = HomeScreen(username)  # Pass the username to home-screen
            home_screen.run()
        else:
            # If the credentials are invalid, show an error message
            self.label_error_invalid['text'] = "Invalid credentials"

    def signup(self):
        """The signup page"""
        # Destroy the current login screen
        self.window.destroy()
        
        # Show the setup screen
        setup_screen = SetupScreen()
        setup_screen.run()
