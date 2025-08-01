import sqlite3
import bcrypt

database = sqlite3.connect("usersdb.db")
cursor = database.cursor()

def AddUser(email, username, password, teamID, role, position):
    
    passwordBytes = password.encode("utf-8") # Converts the string into a byte array
    salt = bcrypt.gensalt() # Generates the salt for unique encryption
    hashedPassword = bcrypt.hashpw(passwordBytes, salt)
    hashedPassword = hashedPassword.decode('utf-8')
    # print(hashedPassword)

    cursor.execute(f"INSERT INTO Users(username, email, hashedPassword, role, preferredPosition, teamID) VALUES ('{username}', '{email}', '{hashedPassword}', '{role}', {position}, '{teamID}')") # FILL THIS OUT
    database.commit()
    print("Created account with\nEmail: " + email + "\nUsername: " + username + "\nPassword: " + password + "\nTeamID: " + teamID + "\nRole: " + role + "\nPosition: " + position)


# AddUser("tom@gmail.com", "tom", "password12!$", "England RFC", "Player", "8") # Testing Code

def CheckPassword(username, userPassword):
    cursor.execute(f"SELECT hashedPassword FROM Users WHERE username = '{username}'") # uses SQL to select the password of the user
    hashedPassword = cursor.fetchone()[0]
    hashedPassword = hashedPassword.encode('utf-8')

    userBytes = userPassword.encode('utf-8')
    result = bcrypt.checkpw(userBytes, hashedPassword)
    print(result)


#CheckPassword("tom", "password12!$")