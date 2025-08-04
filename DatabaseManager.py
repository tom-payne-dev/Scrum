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

def addFixture(homeTeam, visitingTeam, date, meetTime, startTime, finishTime, details, longitude, latitude, scoreHome='0', scoreAway='0'):
    fixtureID = "1" # generate new fixtureID OR ERROR!!!!!
    
    cursor.execute(f"""
        INSERT INTO Fixture(
            homeTeam, visitingTeam, date, meetTime, startTime, finishTime,
            details, longitude, latitude, scoreHome, scoreAway, fixtureID
        ) 
        VALUES (
            '{homeTeam}', '{visitingTeam}', '{date}', '{meetTime}', '{startTime}', '{finishTime}',
            '{details}', {longitude}, {latitude}, {scoreHome}, {scoreAway}, '{fixtureID}'
        )
    """)
    database.commit()

    print(
        f"Created fixture:\n"
        f"Home: {homeTeam}, Away: {visitingTeam}\n"
        f"Date: {date}, Meet: {meetTime}, Start: {startTime}, Finish: {finishTime}\n"
        f"Location: ({latitude}, {longitude})\n"
        f"Details: {details}\n"
        f"Score: {scoreHome} - {scoreAway}, ID: {fixtureID}"
    )

def getTeamsAvailable(date):
    cursor.execute(f"""
        SELECT teamName from Teams WHERE teamID NOT IN(
            SELECT homeTeam FROM Fixture WHERE date = "{date}"
            UNION
            SELECT visitingTeam FROM Fixture WHERE date = "{date}"
        )
    """) # Selects all teams that do not have a fixture on the passed date
    return ([value[0] for value in cursor.fetchall()])


# print(getTeamsAvailable("19/12/2024"))
# print(getTeamsAvailable("20/12/2024"))
# print(getUserRecord("tom"))
# print(ValueExists("tom", "username", "Users"))
# addFixture("ENG001", "FRA001", "20/12/2024", "13:00", "14:00", "16:00", "Bring Gumshield", "-0.3419", "51.455")


#CheckPassword("tom", "password12!$")