import tkinter as tk
from tkinter import messagebox
from components.baseScreen import BaseScreen
from components.dbService import DatabaseService

class SettingsScreen(BaseScreen):
    def __init__(self, master=None, home_screen=None):
        super().__init__(master, home_screen, title="Settings")
        self.options = ['Sound', 'Credits', 'Delete User']
        self.sound_state = self.home_screen.sound_on if self.home_screen else True
        self.create_options()
        self.dbService = DatabaseService()  # Create a new instance of the DatabaseService class

    def create_options(self):
        # Middle Section
        frame_middle = tk.Frame(self, bg='#99ebff', padx=5)
        frame_middle.pack(fill='x', pady=(5,0))

        # Display options
        for option in self.options:
            if option == 'Sound':
                self.sound_button = tk.Button(frame_middle, text='Sound ON', font=("Arial", 18, "bold"), bg='white', fg='black',
                                              command=self.toggle_sound)
                self.sound_button.pack(fill='x', padx=10, pady=15)
            elif option == 'Credits':
                self.credits_button = tk.Button(frame_middle, text='Credits', font=("Arial", 18, "bold"), bg='white', fg='black',
                                                command=self.show_credits)
                self.credits_button.pack(fill='x', padx=10, pady=15)
            elif option == 'Delete User':
                self.delete_button = tk.Button(frame_middle, text='Delete User', font=("Arial", 18, "bold"), bg='white', fg='black',
                                              command=self.delete_user)
                self.delete_button.pack(fill='x', padx=10, pady=15)

    def toggle_sound(self):
        """Toggle the sound state."""
        if self.sound_state:
            self.sound_button.config(text='Sound OFF', bg='red')
            if self.home_screen:
                self.home_screen.mute_sound()
        else:
            self.sound_button.config(text='Sound ON', bg='white')
            if self.home_screen:
                self.home_screen.unmute_sound()

        # update both local and home screen sound state
        self.sound_state = self.home_screen.sound_on = not self.sound_state

    def show_credits(self):
        """Show the credits in a new window."""

        credits_window = tk.Toplevel(self)
        credits_window.title("Credits")

        canvas = tk.Canvas(credits_window)
        canvas.pack()

        credits_text = """
        
        
        
        
        
        
        
        
        
        
        
                Credits:
                
                PROJECT GDG
                Good Deeds Gamified
                
                By Aymen Ahmed
                City University of London Project
                """

        text_id = canvas.create_text(10, 10, anchor='nw', text=credits_text)

        def scroll():
            canvas.move(text_id, 0, -1)
            canvas.after(100, scroll)

        scroll()

    def delete_user(self):
        confirm = messagebox.askyesno("Confirmation",
                                      "This will log you out and delete your account, do you wish to proceed?",
                                      parent=self)
        if confirm:
            self.delete_user_data()

    def delete_user_data(self):
        """Delete user data."""
        self.dbService.delete_user_activity(self.home_screen.current_user())
        self.dbService.delete_user(self.home_screen.current_user())
        messagebox.showinfo("User Deleted", "Your account has been successfully deleted.")

        # Navigate back to the login screen
        self.home_screen.window.destroy()  # Destroy the home screen
