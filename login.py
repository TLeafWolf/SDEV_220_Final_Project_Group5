# this program opens a window display in vs code when it is ran as of right now

import customtkinter
import sqlite3
import tkinter

from tkinter import messagebox

connection = sqlite3.connect('users.db')

cursor = connection.cursor()

command1 = """
    CREATE TABLE IF NOT EXISTS
    USERS(username text, password text)
"""
cursor.execute(command1)
cursor.execute("INSERT INTO USERS VALUES('user1', 'password1')")
cursor.execute("INSERT INTO USERS VALUES('user2', 'password2')")
cursor.execute("INSERT INTO USERS VALUES('user3', 'password3')")
cursor.execute("INSERT INTO USERS VALUES('user4', 'password4')")



customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()

app.title("Inventory Management Login")
app.geometry("960x540")

bottomframe = tkinter.Frame(app)
bottomframe.pack(expand = True)

def button_event():
    cursor.execute("SELECT * from USERS")
    results = cursor.fetchall()
    for result in results:
        if user_name.get() == result[0] and password.get() == result[1]:
            messagebox.showinfo(title = "Login Success", message = "You successfully logged in.")
            break
        else:
            messagebox.showinfo(title = "Error", message = "Invalid login.")


user_name = customtkinter.CTkEntry(master=bottomframe,
                                   placeholder_text="Username",
                                  font =('Helvetica', 28),
                                   width =800,
                                   height=100,
                                   border_width=2,
                                   corner_radius = 30)
user_name.pack()

password = customtkinter.CTkEntry(master=bottomframe,
                                   placeholder_text="Password",
                                  font =('Helvetica', 28),
                                   width =800,
                                   height=100,
                                   border_width=2,
                                   corner_radius = 30,
                                   show = "*")
password.pack()

button = customtkinter.CTkButton(master=bottomframe,
                                 width =500,
                                 height=100,
                                 border_width=0,
                                 corner_radius = 8,
                                 text = "Log In",
                                 font =('Helvetica', 28),
                                 command = button_event)
button.pack()

label = customtkinter.CTkLabel(master=bottomframe,
                               text ="",
                               text_color="black",
                                width =200,
                                 height=100,
                                 font =('Helvetica', 28),
                                 fg_color = ("white"),
                                 corner_radius = 8)
label.pack()
app.mainloop()