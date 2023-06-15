import mysql.connector
import bcrypt
import base64
import json


class DatabaseService:
    def __init__(self):
        """Initialise database connection"""
        self.conn = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='password',
            database='projectGDG'
        )

    def validate_credentials(self, username, password):
        """Check if entered password matches stored hashed password for given username"""
        user = self.get_user(username)
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            return True
        else:
            return False

    def get_user(self, username):
        """Get user details for the provided username"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user:
            user['password'] = base64.b64decode(user['password'].encode('utf-8'))
        return user

    def create_user(self, username, hashed_password, firstname, lastname):
        """Create a new user entry with the given details"""
        cursor = self.conn.cursor()
        base64_hashed_password = base64.b64encode(hashed_password).decode('utf-8')
        cursor.execute("""
            INSERT INTO Users (username, password, firstname, lastname) 
            VALUES (%s, %s, %s, %s)
        """, (username, base64_hashed_password, firstname, lastname))
        self.conn.commit()

    def drop_users_table(self):
        """Delete users table from database"""
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Users")
        self.conn.commit()

    def create_users_table(self):
        """Create a users table in the database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE Users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                firstname VARCHAR(255),
                lastname VARCHAR(255)
            )
        """)
        self.conn.commit()

    def create_user_activity_table(self):
        """Create a table for user activity in the database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE UserActivity (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                happiness_meter INT,
                good_deeds_history TEXT,
                FOREIGN KEY(username) REFERENCES Users(username)
            )
        """)
        self.conn.commit()

    def save_user_activity(self, username, happiness_meter, good_deeds_history):
        """Store the user's activity in the database"""
        cursor = self.conn.cursor()
        # Serialise good deeds history to a string
        good_deeds_history_str = json.dumps(good_deeds_history)
        cursor.execute("""
            INSERT INTO UserActivity (username, happiness_meter, good_deeds_history) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE happiness_meter=VALUES(happiness_meter), good_deeds_history=VALUES(good_deeds_history)
        """, (username, happiness_meter, good_deeds_history_str))
        self.conn.commit()

    def get_user_activity(self, username):
        """Fetch the user's activity for the username provided in the parameter"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM UserActivity WHERE username=%s", (username,))
        activity = cursor.fetchone()
        if activity:
            activity['good_deeds_history'] = json.loads(activity['good_deeds_history'])
        return activity
    
    def close(self):
        """Close the database connection"""
        self.conn.close()

    def delete_user_activity(self, username):
        """Delete the user's activity for the provided username"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM UserActivity WHERE username=%s", (username,))
        self.conn.commit()

    def delete_user(self, username):
        """Delete the user's account for the provided username"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Users WHERE username=%s", (username,))
        cursor.execute("DELETE FROM UserActivity WHERE username=%s", (username,))
        self.conn.commit()


