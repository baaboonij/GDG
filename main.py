# main.py
# This is the main entry point for the application.
# It initialises and then runs the login screen.
from components.login import LoginScreen

def main():
    login_screen = LoginScreen()
    login_screen.run()

if __name__ == "__main__":
    main()
