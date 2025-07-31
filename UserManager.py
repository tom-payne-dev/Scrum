import sqlite3
import customtkinter as tk
import time
import re
import DatabaseManager

database = sqlite3.connect("usersdb.db") # connects to database file
cursor = database.cursor()

root = tk.CTk() # root of all GUI
root.geometry("1280x720")
root.title("Scrum")
header = tk.CTkLabel(root, text="Create Account")
header.pack()

cursor.execute("SELECT teamName from Teams") # uses SQL to select all the different team names from the database
teams = [team[0] for team in cursor.fetchall()] # Creates an array of all the team names from the database
print(teams)

selection = tk.StringVar(value=teams[0]) # creates a string variable using the first team in the database array
teamsDropdown = tk.CTkOptionMenu(root, variable=selection, values=teams) # creates a gui dropdown including all the different teams
teamsDropdown.pack(pady=10, padx=10)

usernameLabel = tk.CTkLabel(root, text="Username")
usernameLabel.pack()
username = tk.CTkEntry(root, placeholder_text='username') # initialises a username field
username.pack()

passwordLabel = tk.CTkLabel(root, text="Password")
passwordLabel.pack()
password = tk.CTkEntry(root, placeholder_text='password', show="*") # initialises a password field
password.pack()

def CreateAccount():
    usernameValue = username.get() # Retrieves username from username field
    passwordValue = password.get() # Retrieves password from password field

    specialChars = re.findall(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]", passwordValue) # returns all special characters
    numbers = re.findall("[1234567890]", passwordValue) # returns all numbers

    if (len(specialChars) >= 2 and len(numbers) >= 1 and len(passwordValue) >= 12 and len(usernameValue) > 0): # Validation checks
        DatabaseManager.AddUser(usernameValue, passwordValue, teamsDropdown.get()) # Uses the database manager and passes through the data
        validationPopup.configure(text="Account Created", text_color="green")
    else:
        validationPopup.configure(text="Requires 12 characters, 2 special characters, 1 number", text_color="red")


createButton = tk.CTkButton(root, text="Create Account", command=CreateAccount)
createButton.pack(pady=20)

validationPopup = tk.CTkLabel(root, text="", text_color="green")
validationPopup.pack()

root.mainloop()
