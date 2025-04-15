import tkinter

window = tkinter.Tk()
window.title("login form")
window.geometry('340x440')

label = tkinter.Label(window, text = "Login")
label.pack()

window.mainloop()