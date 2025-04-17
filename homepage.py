import tkinter as tk


root = tk.Tk()
root.title("Main")
root.geometry("1920x1080")

bottomframe = tk.Frame(root)
bottomframe.pack(expand = True)

logo = tk.Label(root, text="Logo", width=20, height=2,font =('Helvetica', 18),)
logo.place(x=30, y=10, width=100, height=50)

low_stock = tk.Button(root, text="Low Stock", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
low_stock.place(x=30, y=60, width=150, height=50)

Aisle = tk.Button(root, text="Aisle", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Aisle.place(x=30, y=120, width=150, height=50)

Bay = tk.Button(root, text="Bay", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Bay.place(x=30, y=180, width=150, height=50)

Searcha = tk.Button(root, text="Search", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Searcha.place(x=30, y=240, width=150, height=50)

Veiw_all = tk.Button(root, text="Veiw all", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Veiw_all.place(x=30, y=300, width=150, height=50)

Log_out = tk.Button(root, text="Log out", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Log_out.place(x=30, y=360, width=150, height=50)

Inventory_label = tk.Label(root, text="Inventory",font =('Helvetica', 28), width=20, height=2, bg = '#ffffff')
Inventory_label.place(x=250, y=10, width=1600, height=100)

data = tk.Label(root, text="Data placeholder",font =('Helvetica', 28), width=20, height=2, bg = '#aaaaaa')
data.place(x=250, y=100, width=1600, height=850)

add= tk.Button(root, text="Add", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
add.place(x=1380, y=1000, width=150, height=50)

modify = tk.Button(root, text="Modify", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
modify.place(x=1540, y=1000, width=150, height=50)

remove = tk.Button(root, text="Remove", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
remove.place(x=1700, y=1000, width=150, height=50)

root.mainloop()