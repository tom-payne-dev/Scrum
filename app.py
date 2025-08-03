import customtkinter as tk
import DatabaseManager

class User:
    def __init__(self, username):
            userRecord = DatabaseManager.getUserRecord(username)
            print(userRecord)
            self.username = username
            self.email = userRecord[1]
            self.password = userRecord[2]
            self.role = userRecord[3]
            self.position = userRecord[4]
            self.teamID = userRecord[5]

class MainTabView(tk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # create tabs
        self.add("Fixtures")
        self.add("Statistics")

        # add widgets on tabs
        self.label = tk.CTkLabel(master=self.tab("Fixtures"), text="Hello")
        self.label.grid(row=0, column=0, padx=20, pady=20)


class App(tk.CTk):
    def __init__(self, username):
        super().__init__()
        self.tab_view = MainTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=150, pady=150)
        self.user = User(username)

session = App("tom")
session.mainloop()