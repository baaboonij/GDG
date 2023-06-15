This is an instruction manual for the app's download and use. There is an image reference word document that will be submitted in the extra materials section for use of the examiner.

-------------
TO RUN THE PROGRAM
-------------
1. Ensure PyCharm is installed. Both community edition and professional edition are fine. [ https://www.jetbrains.com/pycharm/download/#section=windows ]

2. Ensure Python is installed. [ https://www.python.org/downloads/ ]

3. Ensure XAMPP is installed [ https://www.apachefriends.org/ ]
    
4. Using PyCharm, open the Project folder and configure the Python interpreter. [To configure, in PyCharm go to File > Settings > ProjectName > Python Interpreter > Add local interpreter, then find the interpreter installed and apply it. PyCharm may need a restart]

5. Install these packages by typing into the terminal:
    pip install mysql-connector-python
    pip install bcrypt
    pip install Pillow
    pip install pygame

6. Using the XAMPP control panel, start Apache and MySQL. Ensure that the ports being used to carry this out are not in use by another application
[note, if there is an error in this step, it could be because a port is already in use. To fix this, go into the command prompt and type 'netstat -ano | findstr :portnumber' to find out what is using it, and end the process via task bar]

7. Select Admin on the MySQL section, a localhost website should launch on your default browser as a phpmyadmin website

8. On the phpmyadmin website, navigate to User Accounts at the top tab, and add a User Account

9. When adding the User Account, you will be asked to put in details. They should look like so:

    Username: Use text field: admin
    Host name: Local: localhost
    Password: Use text field: password
    Retype: password

You must also check these boxes:

    Create database with the same name and grant all privileges
    Grant all privileges on wildcard name (username\_%)
    Global privileges [note, this should check all the boxes in the data, structure, and administration sections]

When you have put in these details, select 'Go' at the bottom

10. Now that you have created the admin account, navigate to the 'Databases' section at the top. There should be a 'Create database' section in that page.
Type 'projectgdg' in the textfield and select the 'Collation' option, then create the database.

11. Once the database has been created, navigate to 'Import' at the top, and select 'Choose file'. Find the 'projectGDG.sql' file in the project folder and import that.

12. Run main.py
-------------




-------------
DIRECTIONS OF USE
-------------
- You can create an account by selecting the sign up button on the login page, and login once an account has been signed up

- The home page consists of a meter on the left side, which increases when a good deed is submitted into the text field and decreases for every period of time that a good deed isn't submitted. (The decrease time period should every few hours however for testing purposes it has been set to decrease every five seconds)

- Input good deeds into the text field to keep the bar high, and the pet happy. The lower the bar, the sadder the expression on the pet.

- Clicking on the pet will pet it, producing a 'purring' sound.

- When the menu is selected, you can navigate to customise the pet, the settings, the good deeds history, the missions, or the logout. Each is self explanatory.

- Customise pet has the options of changing the colour of the pet, the accessory the pet wears, and the background colour of the pet image.

- In settings, you can toggle the sound on or off, view the credits, and delete your account from the database.

- In missions, you can view challenges to carry out as good deeds.

- In history, you can check the history of your good deeds, updated in real time and saved in the database for the next time you login.

- You can logout with the logout button.
-------------



