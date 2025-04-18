import tkinter as tk
from tkinter import messagebox
import sqlite3


root = tk.Tk()
root.title("Main")
root.geometry("1920x1080")

bottomframe = tk.Frame(root)
bottomframe.pack(expand = True)

# Function to fetch low inventory items
def fetch_low_inventory(threshold):
    conn = sqlite3.connect('inventory.db')  # Connect to your database
    cursor = conn.cursor()
    
    # Query to select items with inventory below the threshold
    cursor.execute("SELECT name, quantity FROM Supply WHERE quantity < ?", (threshold,))
    low_inventory_items = cursor.fetchall()
    
    conn.close()
    return low_inventory_items
def display_low_inventory():
    threshold = int(threshold_entry.get())
    low_inventory_items = fetch_low_inventory(threshold)
    
    if low_inventory_items:
        result_text = "Low Inventory Items:\n"
        for item in low_inventory_items:
            result_text += f"Item: {item[0]}, Quantity: {item[1]}\n"
    else:
        result_text = "No low inventory items found."
    
    result_label.config(text=result_text)

# Create and place the threshold input
threshold_label = tk.Label(root, text="Enter Inventory Threshold:")
threshold_label.pack()

threshold_entry = tk.Entry(root)
threshold_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack()

logo = tk.Label(root, text="Logo", width=20, height=2,font =('Helvetica', 18),)
logo.place(x=30, y=10, width=100, height=50)

low_stock = tk.Button(root, text="Low Stock", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff', command=display_low_inventory)
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