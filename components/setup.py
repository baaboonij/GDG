import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from components.dbService import DatabaseService
import bcrypt


class SetupScreen:
    """A class representing the setup screen for a user."""
    def __init__(self):
        """initialise the setup screen."""
        self.dbService = DatabaseService()

        # Initialise window
        self.initialise_window()
        self.draw_setup_screen()

    def run(self):
        # Starting the Tkinter event loop
        self.window.mainloop()

    def initialise_window(self):
        """initialise the main window."""
        self.window = tk.Tk()
        self.window.geometry('390x850')
        self.window.configure(bg='white')
        self.window.title('Sign Up - projectGDG')
        self.window.resizable(False, False)

    def draw_setup_screen(self):
        # Draw UI
        """Draw the elements on the setup screen."""
        self.draw_header_section()
        self.draw_username_field()
        self.draw_password_field()
        self.draw_firstname_field()
        self.draw_lastname_field()
        self.draw_button_setup()

    def draw_header_section(self):
        # Drawing the header with the brand logo
        header = tk.Frame(self.window, bg='white')
        header.grid(row=0, column=0, columnspan=1, pady=20, padx=15)

        # Create the left column for the logo
        frame_logo = tk.Frame(header, bg='white')
        frame_logo.grid(row=0, column=0, padx=(10, 20))

        self.image_logo = PhotoImage(file='images/logo.png')

        # Resize the logo image (this requires the Pillow library)
        self.image_logo = self.image_logo.subsample(4, 4)  # decrease size

        # Create a label for the logo and add it to the left column
        label_logo = tk.Label(frame_logo, image=self.image_logo, bg='white')
        label_logo.image = self.image_logo  # keep a reference to the image to prevent it from being garbage collected
        label_logo.pack(pady=2)

        # Create the right column for the "Sign up" label
        frame_signup = tk.Frame(header, bg='black')
        frame_signup.grid(row=0, column=1, padx=(20, 10))

        # Add the "Sign up" label to the right column
        label_signup = tk.Label(frame_signup, text="Sign up", font=("Helvetica", 26), bg='light blue', fg='white')
        label_signup.pack(side=tk.RIGHT)

    def draw_username_field(self):
        """Draw the input field for the username."""
        frame_username = ttk.Frame(self.window, padding="15 10 15 10")
        frame_username.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        label_username = tk.Label(frame_username, text="Username:", font=("Arial", 16), fg='black')
        label_username.pack(pady=10)
        self.username_input = tk.StringVar()
        entry_username = ttk.Entry(frame_username, width=30, textvariable=self.username_input)
        entry_username.pack(padx=10)
        self.label_username_error = tk.Label(frame_username, text="", font=("Arial", 14), fg='red')
        self.label_username_error.pack(padx=10)

    def draw_password_field(self):
        """Draw the input field for the password."""
        frame_password = ttk.Frame(self.window, padding="15 10 15 10")
        frame_password.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        label_password = tk.Label(frame_password, text="Password:", font=("Arial", 16), fg='black')
        label_password.pack(pady=10)
        self.password_input = tk.StringVar()
        entry_password = ttk.Entry(frame_password, width=30, textvariable=self.password_input, show='*')
        entry_password.pack(padx=10)
        self.label_password_error = tk.Label(frame_password, text="", font=("Arial", 14), fg='red')
        self.label_password_error.pack(padx=10)

    def draw_firstname_field(self):
        """Draw the input field for the first name."""
        frame_firstname = ttk.Frame(self.window, padding="15 10 15 10")
        frame_firstname.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        firstname_label = tk.Label(frame_firstname, text="First Name:", font=("Arial", 16), fg='black')
        firstname_label.pack(pady=10)
        self.firstname_input = tk.StringVar()
        entry_firstname = ttk.Entry(frame_firstname, width=30, textvariable=self.firstname_input)
        entry_firstname.pack(padx=10)
        self.label_firstname_error = tk.Label(frame_firstname, text="", font=("Arial", 14), fg='red')
        self.label_firstname_error.pack(padx=10)

    def draw_lastname_field(self):
        """Draw the input field for the last name."""
        frame_lastname = ttk.Frame(self.window, padding="15 10 15 10")
        frame_lastname.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        label_lastname = tk.Label(frame_lastname, text="Last Name:", font=("Arial", 16), fg='black')
        label_lastname.pack(pady=10)
        self.lastname_input = tk.StringVar()
        entry_lastname = ttk.Entry(frame_lastname, width=30, textvariable=self.lastname_input)
        entry_lastname.pack(padx=10)
        self.label_lastname_error = tk.Label(frame_lastname, text="", font=("Arial", 14), fg='red')
        self.label_lastname_error.pack(padx=10)

    def draw_button_setup(self):
        """Draw the button for the setup."""
        button_setup = tk.Button(self.window, text="Sign Up", command=self.setup_account,
                                 font=('Arial', 16), 
                                 bg='light blue',
                                 activebackground='#ADD8E6',
                                 fg='#000000',
                                 relief="flat",
                                 bd=0,
                                 overrelief='raised')
        button_setup.grid(row=5, column=0, columnspan=2, padx=(15, 15), pady=(10, 20))

    def setup_account(self):
        """Create a new account with the input details."""
        username = self.username_input.get().strip()
        password = self.password_input.get().strip()
        firstname = self.firstname_input.get().strip()
        lastname = self.lastname_input.get().strip()

        # Clear all error labels
        self.label_username_error.config(text="")
        self.label_password_error.config(text="")
        self.label_firstname_error.config(text="")
        self.label_lastname_error.config(text="")

        error_occurred = False

        # Check if any field is empty
        if not username:
            # Display a red label that says "Invalid field"
            self.label_username_error.config(text="Field cannot be blank!")
            error_occurred = True

        if not password:
            self.label_password_error.config(text="Field cannot be blank!")
            error_occurred = True

        if not firstname:
            self.label_firstname_error.config(text="Field cannot be blank!")
            error_occurred = True

        if not lastname:
            self.label_lastname_error.config(text="Field cannot be blank!")
            error_occurred = True

        if error_occurred:
            # Don't proceed with account setup if any field is invalid
            return  

        # hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # create the new user
        self.dbService.create_user(username, hashed_password, firstname, lastname)
        self.window.destroy()

        # After account creation, direct the user to the login screen
        from components.login import LoginScreen
        login_screen = LoginScreen()
        login_screen.run()

if __name__ == "__main__":
    setup_screen = SetupScreen()
    tk.mainloop()
