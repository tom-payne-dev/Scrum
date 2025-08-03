import customtkinter as tk
import DatabaseManager

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
    usernameValue = username.get()
    passwordValue = password.get()

    if DatabaseManager.ValueExists(usernameValue, "username", "Users"):
        if DatabaseManager.CheckPassword(usernameValue, passwordValue):
            validationPopup.configure(text="Signing you in...", text_color="green")
        else:
            validationPopup.configure(text="Password Incorrect", text_color="red")
    else:
        validationPopup.configure(text="User does not exist", text_color="red")


button = tk.CTkButton(root, text="Log In", command=LogIn)
button.pack(pady=20)

validationPopup = tk.CTkLabel(root, text="", text_color="green")
validationPopup.pack()

root.mainloop()