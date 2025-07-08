import sqlite3
import customtkinter as tk
import time
import re

database = sqlite3.connect("usersdb.db")
cursor = database.cursor()

root = tk.CTk()
root.geometry("1280x720")
root.title("Scrum")
header = tk.CTkLabel(root, text="Create Account")
header.pack()

cursor.execute("SELECT teamName from Teams")
teams = [team[0] for team in cursor.fetchall()]
print(teams)

selection = tk.StringVar(value=teams[0])
teamsDropdown = tk.CTkOptionMenu(root, variable=selection, values=teams)
teamsDropdown.pack(pady=10, padx=10)

usernameLabel = tk.CTkLabel(root, text="Username")
usernameLabel.pack()
username = tk.CTkEntry(root, placeholder_text='username')
username.pack()

passwordLabel = tk.CTkLabel(root, text="Password")
passwordLabel.pack()
password = tk.CTkEntry(root, placeholder_text='password')
password.pack()


def CreateAccount():

    print("Created account with\nUsername: " + usernameValue + "\nPassword: " + passwordValue + "\nTeam: " + teamsDropdown.get())

createButton = tk.CTkButton(root, text="Create Account", command=CreateAccount)
createButton.pack(pady=20)

root.mainloop()
