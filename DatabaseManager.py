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

def addFixture(homeTeam, visitingTeam, date, meetTime, startTime, finishTime, details, latitude, longitude, scoreHome='0', scoreAway='0'):
    cursor.execute(f"""
        INSERT INTO Fixture(
            homeTeam, visitingTeam, date, meetTime, startTime, finishTime,
            details, latitude, longitude, scoreHome, scoreAway
        ) 
        VALUES (
            '{homeTeam}', '{visitingTeam}', '{date}', '{meetTime}', '{startTime}', '{finishTime}',
            '{details}', {latitude}, {longitude}, {scoreHome}, {scoreAway}
        )
    """)
    database.commit()

    print(
        f"Created fixture:\n"
        f"Home: {homeTeam}, Away: {visitingTeam}\n"
        f"Date: {date}, Meet: {meetTime}, Start: {startTime}, Finish: {finishTime}\n"
        f"Location: ({latitude}, {longitude})\n"
        f"Details: {details}\n"
        f"Score: {scoreHome} - {scoreAway}"
    )

def getTeamsAvailable(date):
    cursor.execute(f"""
        SELECT teamID from Teams WHERE teamID NOT IN(
            SELECT homeTeam FROM Fixture WHERE date = "{date}"
            UNION
            SELECT visitingTeam FROM Fixture WHERE date = "{date}"
        )
    """) # Selects all teams that do not have a fixture on the passed date
    return ([value[0] for value in cursor.fetchall()])

def getFutureFixtures(teamID):
    cursor.execute(f"""
        SELECT * FROM Fixture WHERE (homeTeam = "ENG001" OR visitingTeam = "ENG001") and "date" > date('now') ORDER BY "date" ASC;
    """)
    return cursor.fetchall()

def getFixture(fixtureID):
    cursor.execute(f"""
        SELECT * FROM Fixture WHERE fixtureID = {fixtureID}
    """)
    return cursor.fetchall()[0]
    
def getLatLong(teamID):
    cursor.execute(f"""
        SELECT latitude, longitude FROM Teams WHERE teamID = "{teamID}"
    """)
    return cursor.fetchone()

def fetchTeamName(teamID):
    cursor.execute(f"""
        SELECT teamName FROM Teams WHERE teamID = "{teamID}"
    """)
    return cursor.fetchone()[0]

def getPlayersInPosition(position, team):
    cursor.execute(f"""
        SELECT username FROM Users WHERE preferredPosition = {position} AND teamID = "{team}" AND role="Player"
    """)
    players = cursor.fetchall()
    if players:
        return [player[0] for player in players] # Returns players in the specified position
    else:
        cursor.execute(f"""
            SELECT username FROM Users WHERE teamID = "{team}" AND role="Player"
        """)
        return [player[0] for player in cursor.fetchall()] # Returns all players if no players in position
    
def getPlayerInPosition(position, fixtureID):
    cursor.execute(f"""
        SELECT username FROM rsvp WHERE position = {position} AND sessionID = '{fixtureID}'
    """)
    player = cursor.fetchone()
    if player:
        return player[0]
    else:
        return None

    
def submitRSVP(username, fixtureID, position):
    cursor.execute(f"""
        SELECT COUNT(*) FROM rsvp WHERE username = '{username}' AND sessionID = '{fixtureID}'
    """) # Selects the number of entries in the RSVP table for the user/fixture combination
    numOfEntries = cursor.fetchall()[0][0] # Fetches the number of entries from the cursor
    if numOfEntries == 0: # If there are no entries, the user has not been submitted an RSVP for this fixture
        #Check if the position is already filled
        cursor.execute(f"""
                SELECT username FROM rsvp WHERE position = '{position}' AND sessionID = '{fixtureID}'
            """)
        existing = cursor.fetchone()
        if existing: # If there is already a player in this position
            cursor.execute(f"""
                DELETE FROM rsvp WHERE sessionID = '{fixtureID}' AND position = '{position}'
            """)
            database.commit() # Remove them from the RSVP list
            print("Removed existing player " + existing[0] + " from position " + str(position) + " for fixture " + str(fixtureID))
        cursor.execute(f"""
                INSERT INTO rsvp(username, sessionID, response, declinedReason, position)
                VALUES('{username}', '{fixtureID}', 'Requested', 'N/A', '{position}')
            """)
        database.commit()
        print("RSVP Submitted for User/Fixture Combination " + "Username: " + username + " FixtureID: " + str(fixtureID) + " Position: " + str(position))
        return True
    else: # If there are entries, the user has already submitted an RSVP for this fixture
        # print("RSVP Already Exists for User/Fixture Combination " + "Username: " + username + " FixtureID: " + str(fixtureID) + " Position: " + str(position))
        cursor.execute(f"""
            SELECT position FROM rsvp WHERE username = '{username}' AND sessionID = '{fixtureID}' AND position = '{position}'
        """)
        if cursor.fetchone(): # If the user is trying to submit the same position again, do nothing
            return False
        
        # If the position is new, remove the user's old RSVP for this fixture
        cursor.execute(f"""
            DELETE FROM rsvp WHERE username = '{username}' AND sessionID = '{fixtureID}'
        """)
        database.commit()
        submitRSVP(username, fixtureID, position)

# submitRSVP("Player1", "11")

def acceptRSVP(username, fixtureID):
    cursor.execute(f"""
            UPDATE rsvp
            SET response = "Accepted"
            WHERE response = "Requested" and sessionID = '{fixtureID}'
        """)
    return cursor.fetchall()

def retrieveRSVPRequests(username):
    cursor.execute(f"""
            SELECT * FROM rsvp WHERE username = '{username}'
        """)
    return cursor.fetchall()

def retrieveRSVPStatus(username, fixtureID):
    cursor.execute(f"""
            SELECT response, position FROM rsvp WHERE username = '{username}' and sessionID = '{fixtureID}'
        """)
    status = cursor.fetchall()
    if status: # If there has been a request sent
        return status[0][0] + " in position " + str(status[0][1]) # Return the current response
    else: # Otherwise
        return "None Sent" # Return that no request has been sent

# print(retrieveRSVPStatus("Player20", "11"))
# print(retrieveRSVPStatus("Player2", "11"))

#print(getPlayersInPosition("2", "ENG001"))
# print(getLatLong("ENG001"))
# print(getTeamsAvailable("19/12/2024"))
# print(getTeamsAvailable("20/12/2024"))
# print(getUserRecord("tom"))
# print(ValueExists("tom", "username", "Users"))
# addFixture("ENG001", "FRA001", "20/12/2024", "13:00", "14:00", "16:00", "Bring Gumshield", "-0.3419", "51.455")
# print(getFutureFixtures("ENG001"))


#CheckPassword("tom", "password12!$")#