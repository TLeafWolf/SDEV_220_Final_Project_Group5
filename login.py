# this program opens a window display in vs code when it is ran as of right now

import tkinter
#imports message box for popups
from tkinter import messagebox


window = tkinter.Tk()
window.title("login form")
window.geometry('340x440')
window.configure(bg = '#333333')

# the def for logging in. will obviously need to repelace the stuff inside of it as right now it is a place holder account information
def login():
    username = "BobMax"
    password = "12345"
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title = "Login Success", message = "You successfully logged in.")
    else:
        messagebox.showinfo(title = "Error", message = "Invalid login.")

# make the gui responsive to the screen. it allows it to change size and location based on the size of the screen and keeps it centered
frame = tkinter.Frame(bg = '#333333')

# creating them
# the ones with label are the text ion it own
# entry is the boxes to put user information
#and the button is th ebutton
# bg is background color
#fg is font color
#font is the fontsize and font type
login_label = tkinter.Label(frame, text = "Login", bg = '#333333', fg = "#008000", font =("Arial",30))
username_label = tkinter.Label(frame, text = "Username", bg = '#333333', fg = "#FFFFFF", font =("Arial",16))
username_entry = tkinter.Entry(frame, font =("Arial",16))
password_entry = tkinter.Entry(frame, show ="*", font =("Arial",16))
password_label = tkinter.Label(frame, text = "Password", bg = '#333333', fg = "#FFFFFF", font =("Arial",16))
login_button = tkinter.Button(frame, text = "Login", bg = '#008000', fg = "#FFFFFF", font =("Arial",16), command = login)

# placing them on the screen
# row and colums is how w eplace it left to right and up and down
# pady is the padding on the y axis it adds space between the object on other objects in the vertical direction
login_label.grid(row = 0, column=0, columnspan=2, sticky=  "news", pady = 40)
username_label.grid(row = 1, column=0)
username_entry.grid(row = 1, column=1, pady = 20)
password_label.grid(row = 2, column=0)
password_entry .grid(row = 2, column=1, pady = 20)
login_button .grid(row = 3, column=0, columnspan=2, pady = 30)

# displays the frame that is making the form center of screen
frame.pack()
window.mainloop()