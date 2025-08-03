import customtkinter as tk
import DatabaseManager
import app

root = tk.CTk() # root of all GUI
root.geometry("1280x720")
root.title("Scrum")
header = tk.CTkLabel(root, text="Log In", font=('Helvetica', 32, 'bold'))
header.pack()

usernameLabel = tk.CTkLabel(root, text="Username")
usernameLabel.pack()
username = tk.CTkEntry(root, placeholder_text='username') # initialises a username field
username.pack()

passwordLabel = tk.CTkLabel(root, text="Password")
passwordLabel.pack()
password = tk.CTkEntry(root, placeholder_text='password', show="*") # initialises a password field
password.pack()

def LogIn():
    usernameValue = username.get() # retrieves username
    passwordValue = password.get() # and password

    if DatabaseManager.ValueExists(usernameValue, "username", "Users"): # Checks if there is a user record
        if DatabaseManager.CheckPassword(usernameValue, passwordValue): # Checks if the inputted password is correct
            validationPopup.configure(text="Signing you in...", text_color="green")
            session = app.App(usernameValue) # Starts main app, passing the username through to the app
            root.destroy() # Closes the sign in window
            session.mainloop()
        else:
            validationPopup.configure(text="Password Incorrect", text_color="red")
    else:
        validationPopup.configure(text="User does not exist", text_color="red")


button = tk.CTkButton(root, text="Log In", command=LogIn) # Log in button
button.pack(pady=20)

validationPopup = tk.CTkLabel(root, text="", text_color="green") # Validation text for error messages
validationPopup.pack()

root.mainloop()