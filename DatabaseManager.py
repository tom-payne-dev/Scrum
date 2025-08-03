import sqlite3
import bcrypt

database = sqlite3.connect("usersdb.db") # Connects to the database
cursor = database.cursor() # Opens a read/write cursor

def AddUser(email, username, password, teamID, role, position):
    
    passwordBytes = password.encode("utf-8") # Converts the string into a byte array
    salt = bcrypt.gensalt() # Generates the salt for unique encryption
    hashedPassword = bcrypt.hashpw(passwordBytes, salt) # Hashes the byte array to produce a byte hash
    hashedPassword = hashedPassword.decode('utf-8') # Decodes the byte array into string form, for database storage
    # print(hashedPassword)

    cursor.execute(f"""
                        INSERT INTO 
                        Users(username, email, hashedPassword, role, preferredPosition, teamID) 
                        VALUES ('{username}', '{email}', '{hashedPassword}', '{role}', {position}, '{teamID}')
                    """)
    database.commit() # Adds user using arguments
    print("Created account with\nEmail: " + email + "\nUsername: " + username + "\nPassword: " + password + "\nTeamID: " + teamID + "\nRole: " + role + "\nPosition: " + position)


# AddUser("tom@gmail.com", "tom", "password12!$", "England RFC", "Player", "8") # Testing Code

def CheckPassword(username, userPassword):
    cursor.execute(f"SELECT hashedPassword FROM Users WHERE username = '{username}'") # uses SQL to select the password of the user
    hashedPassword = cursor.fetchone()[0] # fetches the password from the cursor select

    hashedPassword = hashedPassword.encode('utf-8') # Converts the string into a byte array
    userBytes = userPassword.encode('utf-8') # Converts the string into a byte array

    result = bcrypt.checkpw(userBytes, hashedPassword)
    return result

def FetchAttributeValues(attribute, table):
    cursor.execute(f"SELECT {attribute} from {table}") # uses SQL to select the attribute values for all players
    return [value[0] for value in cursor.fetchall()] # returns an array of all the values from the database

def ValueExists(value, attribute, table):
    databaseValues = FetchAttributeValues(attribute, table)
    for i in databaseValues:
        if i == value:
            return True
    return False

def getUserRecord(username):
    cursor.execute(f"SELECT * from Users where username = '{username}'") # uses SQL to select the attribute values for all players
    return list(cursor.fetchall()[0]) # returns an array of all the values from the database


# print(getUserRecord("tom"))
# print(ValueExists("tom", "username", "Users"))


#CheckPassword("tom", "password12!$")