import sqlite3

database = sqlite3.connect("usersdb.db")
cursor = database.cursor()

def AddUser(username, password, team):
    # to finish
    print("Created account with\nUsername: " + username + "\nPassword: " + password + "\nTeam: " + team)