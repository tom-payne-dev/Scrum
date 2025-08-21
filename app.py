import customtkinter as tk
from CTkDatePicker import CTkDatePicker
import DatabaseManager
import datetime
import math

class User:
    def __init__(self, username):
            userRecord = DatabaseManager.getUserRecord(username)
            # print(userRecord)
            self.username = username
            self.email = userRecord[1]
            self.password = userRecord[2]
            self.role = userRecord[3]
            self.position = userRecord[4]
            self.teamID = userRecord[5]

class MainTabView(tk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Fixtures") # Adds Fixtures tabs
        self.add("Statistics") # Adds Statistics tabs

        #Fixtures Tab
        self.label = tk.CTkLabel(master=self.tab("Fixtures"), text="Upcoming Matches") # Adds a placeholder label to the tab
        self.label.grid(row=0, column=0, padx=10, pady=10) # Adds the label to the tab
        self.button = tk.CTkButton(master=self.tab("Fixtures"), text="New Fixture", command=master.OpenFixtureCreator)
        self.button.grid(row=1, column=0, padx=10, pady=10)

class FixtureWindow(tk.CTkToplevel):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialises the parent class
        self.user = user

        self.geometry("400x300") # Defines window geometry

        self.header = tk.CTkLabel(self, text="Matchmake Fixture", font=('Helvetica', 32, 'bold')) 
        self.header.grid(row=0, column=0, padx=10, pady=10) # Adds the heading for the window
        
        self.datePicker = CTkDatePicker(self)
        self.datePicker.set_date_format(r"%d/%m/%Y")
        self.datePicker.grid(pady=10) # Adds a Date picker UI widget
        self.submitDate = tk.CTkButton(self, text="Submit", command=lambda: self.Matchmake(self.datePicker.get_date()))
        self.submitDate.grid(pady=10) # Adds a submit button, resulting in the getDate procedure

        self.closestTeamLabel = tk.CTkLabel(self, text="")
        self.closestTeamLabel.grid()
        self.submitFixtureButton = tk.CTkButton(self, state="disabled", text="Create Fixture")
        self.submitFixtureButton.grid(pady=10)
    
    
    def getDate(self):
        date = self.datePicker.get_date() # Gets the date from the date picker
        # print(date)
        return date
    
    def Matchmake(self, date):
        homeTeam = self.user.teamID
        self.chosenDate = date
        availableTeams = DatabaseManager.getTeamsAvailable(self.chosenDate) # Uses the getTeamsAvailable algorithm to retrieve teams on date
        if homeTeam in availableTeams:
            availableTeams.remove(homeTeam)

        distances = {
            #Team : Distance from Home
        }
        for awayTeam in availableTeams:
            awayLatLong = DatabaseManager.getLatLong(awayTeam) # Gets the coordinates of the away team
            distance = self.calculateDistance(awayLatLong) # Finds distance between clubs
            distances[awayTeam] = distance # Creates a Team : Distance pair in the distances dictionary

        self.closestTeam = availableTeams[0] # Basic value
        for awayTeam in distances: # Loops through all teams
            if distances[awayTeam] < distances[self.closestTeam]:
                self.closestTeam = awayTeam # If the team is closer than the stored closest team, then it becomes the closest team
        print("Teams:", distances)
        print("Closest Team:", self.closestTeam)

        self.closestTeamLabel.configure(text=("Closest Team Available: " + DatabaseManager.fetchTeamName(self.closestTeam)[0]))
        self.submitFixtureButton.configure(state="normal", command=self.openCreateFixtureWindow)

    def openCreateFixtureWindow(self):
        self.createFixtureWindow = CreateFixtureWindow(master=self, user=self.user, awayTeam=self.closestTeam, date=self.chosenDate)

    def calculateDistance(self, awayLatLong):
        homeLatLong = DatabaseManager.getLatLong(self.user.teamID) # Retrieve coordinates of user team

        # print(homeLatLong)
        # print(awayLatLong)
        homeLatLong = tuple(map(math.radians, homeLatLong))
        awayLatLong = tuple(map(math.radians, awayLatLong)) # Convert coordinate tuple to radians
        # print(homeLatLong)
        # print(awayLatLong)


        # Haversine Formula
        R = 6371000
        deltaCoords = (awayLatLong[0]-homeLatLong[0], awayLatLong[1]-homeLatLong[1])
        
        a = (math.sin(deltaCoords[0]/2) * math.sin(deltaCoords[0]/2) +
            math.cos(homeLatLong[0]) * math.cos(awayLatLong[0]) *
            math.sin(deltaCoords[1]/2) * math.sin(deltaCoords[1])/2) # Square of half the chord length between points
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) # Angular distance in radians
        d = R * c # Calculates distance in kilometres
        # print(d/1000, "KM")

        return d

class CreateFixtureWindow(tk.CTkToplevel):
    def __init__(self, master, user, date=datetime.date.today().strftime(r"%d/%m/%Y"), awayTeam="",*args, **kwargs):
        super().__init__(*args, **kwargs) # Initialises the parent class
        self.user = user
        self.geometry("600x500") # Defines window geometry
        self.grab_set() # Makes the window modal
        self.date = date
        self.awayTeam = awayTeam

        self.header = tk.CTkLabel(self, text="Create Fixture", font=('Helvetica', 32, 'bold')) 
        self.header.grid(row=0, column=0, padx=10, pady=10) # Adds the heading for the window

        self.homeTeam = user.teamID

        teams = DatabaseManager.FetchAttributeValues("teamID", "Teams")
        self.awayTeamLabel = tk.CTkLabel(self, text="Choose Away Team")
        self.awayTeamLabel.grid(pady=10, row=1, column=0)

        if self.awayTeam == "":
            self.awayTeamSelection = tk.StringVar(value=teams[0]) # creates a string variable using the first team in the database array
        else:
            self.awayTeamSelection = tk.StringVar(value=self.awayTeam)
            
        self.awayTeamsDropdown = tk.CTkOptionMenu(self, variable=self.awayTeamSelection, values=teams) # creates a gui dropdown including all the different teams
        self.awayTeamsDropdown.grid(pady=10, padx=10, row=1, column=1)

        self.datePicker = CTkDatePicker(self)
        self.datePicker.set_date_format(r"%d/%m/%Y")
        if date != "":
            self.datePicker.date_entry.insert(0, self.date)
        self.datePicker.grid(pady=10, row=2, column=0) # Adds a Date picker UI widget
        # self.submitDate = tk.CTkButton(self, text="Submit", command=self.setDate)
        # self.submitDate.grid(pady=10) # Adds a submit button, resulting in the getDate procedure

        self.meetTimeLabel = tk.CTkLabel(self, text="Meet Time")
        self.meetTimeLabel.grid(pady=10, row=3, column=0)
        self.meetTimeEntry = tk.CTkEntry(self, placeholder_text='Meet Time') # initialises a meet time field
        self.meetTimeEntry.grid(pady=10, row=3, column=1)

        self.startTimeLabel = tk.CTkLabel(self, text="Start Time")
        self.startTimeLabel.grid(pady=10, row=4, column=0)
        self.startTimeEntry = tk.CTkEntry(self, placeholder_text='Start Time') # initialises a start time field
        self.startTimeEntry.grid(pady=10, row=4, column=1)

        self.finishTimeLabel = tk.CTkLabel(self, text="Finish Time")
        self.finishTimeLabel.grid(pady=10, row=5, column=0)
        self.finishTimeEntry = tk.CTkEntry(self, placeholder_text='Finish Time') # initialises a finish time field
        self.finishTimeEntry.grid(pady=10, row=5, column=1)

        self.detailsLabel = tk.CTkLabel(self, text="Details")
        self.detailsLabel.grid(pady=10, row=6, column=0)
        self.detailsEntry = tk.CTkEntry(self, placeholder_text='Details') # initialises a details field
        self.detailsEntry.grid(pady=10, row=6, column=1)

        self.locationTeamLabel = tk.CTkLabel(self, text="Location")
        self.locationTeamLabel.grid(pady=10, row=7, column=0)
        self.locationTeamSelection = tk.StringVar(value=teams[0]) # creates a string variable using the first team in the database array
        self.locationTeamsDropdown = tk.CTkOptionMenu(self, variable=self.locationTeamSelection, values=teams) # creates a gui dropdown including all the different teams
        self.locationTeamsDropdown.grid(pady=10, padx=10, row=7, column=1)

        self.createFixtureButton = tk.CTkButton(self, text="Add Fixture", command=self.createFixture) # Calls the create fixture function on click
        self.createFixtureButton.grid(pady=20, row=8, column=0)
    
    def createFixture(self):
        homeTeam = self.homeTeam
        awayTeam = self.awayTeamSelection.get()
        date = self.datePicker.get_date()
        meetTime = self.meetTimeEntry.get()
        startTime = self.startTimeEntry.get()
        finishTime = self.finishTimeEntry.get()
        details = self.detailsEntry.get()
        locationTeam = self.locationTeamSelection.get() # Retrieves all entries

        locationLatLong = DatabaseManager.getLatLong(locationTeam) # Retrieves coordinates for the selected team location

        DatabaseManager.addFixture(homeTeam, awayTeam, date, meetTime, startTime, finishTime, details, locationLatLong[0], locationLatLong[1]) # Adds a new fixture to the database



class App(tk.CTk): # inherits the CTk class
    def __init__(self, username):
        super().__init__()
        self.tab_view = MainTabView(master=self) # Initialises the tab view
        self.tab_view.grid(row=0, column=0, padx=100, pady=100) # adds the tab view widget
        self.user = User(username) # adds the user to the app instance for further use

        self.fixtureWindow = None # initialises the fixture window class variable
    
    def OpenFixtureCreator(self):
        if self.fixtureWindow is None or not self.fixtureWindow.winfo_exists(): # Check for if the window is not open
            self.fixtureWindow = FixtureWindow(self.user) # instantiates the window
            print("Opening New Fixture Window...")
        else:
            self.fixtureWindow.focus() # focuses the window
            print("New Fixture Window Already Open")
        

session = App("tom")
session.mainloop()