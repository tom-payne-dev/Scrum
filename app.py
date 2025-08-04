import customtkinter as tk
from CTkDatePicker import CTkDatePicker
import DatabaseManager
import datetime

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # initialises the parent class
        self.geometry("400x300") # Defines window geometry

        self.header = tk.CTkLabel(self, text="Matchmake Fixture", font=('Helvetica', 32, 'bold')) 
        self.header.grid(row=0, column=0, padx=10, pady=10) # Adds the heading for the window
        
        self.datePicker = CTkDatePicker(self)
        self.datePicker.grid(pady=10) # Adds a Date picker UI widget
        self.submitDate = tk.CTkButton(self, text="Submit", command=self.getDate)
        self.submitDate.grid(pady=10) # Adds a submit button, resulting in the getDate procedure
    
    def getDate(self):
        date = self.datePicker.get_date() # Gets the date from the date picker
        print(date)
        return date


class App(tk.CTk): # inherits the CTk class
    def __init__(self, username):
        super().__init__()
        self.tab_view = MainTabView(master=self) # Initialises the tab view
        self.tab_view.grid(row=0, column=0, padx=100, pady=100) # adds the tab view widget
        self.user = User(username) # adds the user to the app instance for further use

        self.fixtureWindow = None # initialises the fixture window class variable
    
    def OpenFixtureCreator(self):
        if self.fixtureWindow is None or not self.fixtureWindow.winfo_exists(): # Check for if the window is not open
            self.fixtureWindow = FixtureWindow() # instantiates the window
            print("Opening New Fixture Window...")
        else:
            self.fixtureWindow.focus() # focuses the window
            print("New Fixture Window Already Open")
        

session = App("tom")
session.mainloop()