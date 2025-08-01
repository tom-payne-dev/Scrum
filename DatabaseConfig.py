import sqlite3

database = sqlite3.connect('usersdb.db') # This creates the database file, usersdb.db in the currect directories and creates a database object so that we can excecute SQL on the statement
cursor = database.cursor()

cursor.execute("""
               CREATE TABLE Users(
                   username TEXT PRIMARY KEY,
                   email TEXT,
                   hashedPassword TEXT,
                   role TEXT,
                   preferredPosition INTEGER,
                   teamID TEXT,
                   FOREIGN KEY (teamID) REFERENCES Teams(teamID)
               )
               """)

cursor.execute("""
               CREATE TABLE Statistics(
                   username TEXT,
                   matchesPlayed INTEGER,
                   tacklesMade INTEGER,
                   metersGained INTEGER,
                   statisticsID TEXT PRIMARY KEY,
                   FOREIGN KEY (username) REFERENCES Users(username)
               )
               """) 

cursor.execute("""
               CREATE TABLE Injuries(
                   username TEXT,
                   injuryType TEXT,
                   injuryDate TEXT,
                   expectedRecovery TEXT,
                   injuryID TEXT PRIMARY KEY,
                   FOREIGN KEY (username) REFERENCES Users(username)
               )
               """) 

cursor.execute("""
               CREATE TABLE rsvp(
                   rsvpID TEXT PRIMARY KEY,
                   username TEXT,
                   sessionID TEXT,
                   response BOOLEAN,
                   declinedReason TEXT,
                   FOREIGN KEY (username) REFERENCES Users(username)
               )
               """)

cursor.execute("""
               CREATE TABLE Teams(
                   teamName TEXT,
                   latitude REAL,
                   longitude REAL,
                   availability TEXT,
                   teamID TEXT PRIMARY KEY,
                   FOREIGN KEY (latitude, longitude) REFERENCES Location(latitude, longitude)
               )
               """)

cursor.execute("""
               CREATE TABLE Attendance(
                   attendanceID TEXT PRIMARY KEY,
                   username TEXT,
                   sessionID TEXT,
                   status BOOLEAN,
                   notes TEXT,
                   FOREIGN KEY (username) REFERENCES Users(username)
               )
               """)

cursor.execute("""
               CREATE TABLE Availability(
                   availabilityID TEXT PRIMARY KEY,
                   date TEXT,
                   available BOOLEAN
               )
               """)

cursor.execute("""
               CREATE TABLE Fixture(
                    homeTeam TEXT,
                    visitingTeam TEXT,
                    date TEXT,
                    meetTime TEXT,
                    startTime TEXT,
                    finishTime TEXT,
                    details TEXT,
                    longitude REAL,
                    latitude REAL,
                    scoreHome INTEGER,
                    scoreAway INTEGER,
                    fixtureID TEXT PRIMARY KEY,
                    FOREIGN KEY (homeTeam) REFERENCES Teams(teamID),
                    FOREIGN KEY (visitingTeam) REFERENCES Teams(teamID),
                    FOREIGN KEY (longitude, latitude) REFERENCES Location(longitude, latitude)
               )
               """)

cursor.execute("""
               CREATE TABLE Training(
                    trainingType TEXT,
                    meetTime TEXT,
                    date TEXT,
                    teamID TEXT,
                    trainingID TEXT PRIMARY KEY,
                    FOREIGN KEY (teamID) REFERENCES Teams(teamID)
               )
               """)

cursor.execute("""
               CREATE TABLE Location(
                    longitude REAL,
                    latitude REAL,
                    PRIMARY KEY(latitude, longitude)
               )
               """)

cursor.execute("""
                INSERT INTO Location (latitude, longitude)
                VALUES 
                    (51.4550, -0.3419),
                    (48.9244, 2.3602),
                    (41.9339, 12.4544)
               """)

cursor.execute("""
                INSERT INTO Teams (teamName, latitude, longitude, availability, teamID)
                VALUES 
                    ('England RFC', 51.4550, -0.3419, 'Available', 'ENG001'),
                    ('France RFC', 48.9244, 2.3602, 'Available', 'FRA001'),
                    ('Italy RFC', 41.9339, 12.4544, 'Available', 'ITA001')
               """)

cursor.close()


