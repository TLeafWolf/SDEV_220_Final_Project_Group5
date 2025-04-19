import tkinter as tk
from tkinter import messagebox
import sqlite3


root = tk.Tk()
root.title("Main")
root.geometry("1920x1080")

left_top= tk.Frame(root)
left_top.grid(row=0, column=0, sticky='n')

left_bottom= tk.Frame(root)
left_bottom.grid(row=1, column=0, sticky='n')

Frame_right = tk.Frame(root)
Frame_right.grid(row=0, column=1)

Bottom_frame= tk.Frame(root)
Bottom_frame.grid(row=1, column=1, sticky='n')

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
threshold_label = tk.Label(left_top, text="Enter Inventory Threshold:")
threshold_label.grid(row =8, column =0)

threshold_entry = tk.Entry(left_top)
threshold_entry.grid(row =9, column =0)


result_label = tk.Label(left_top, text="")
result_label.grid(row =10, column =0)


logo = tk.Label(left_top, text="Logo", width=20, height=2,font =('Helvetica', 18), pady=16)
logo.grid(row =0, column =0)

low_stock = tk.Button(left_top, text="Low Stock", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff', command=display_low_inventory)
low_stock.grid(row =7, column =0)

Aisle = tk.Button(left_top, text="Aisle", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Aisle.grid(row =2, column =0)

Bay = tk.Button(left_top, text="Bay", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Bay.grid(row =3, column =0)

Searcha = tk.Button(left_top, text="Search", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Searcha.grid(row =4, column =0)

Veiw_all = tk.Button(left_top, text="Veiw all", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
Veiw_all.grid(row =5, column =0)

Log_out = tk.Button(left_bottom, text="Log out", width=20, height=2, font =('Helvetica', 18), bg = '#ffffff')
Log_out.grid(row =0, column =0)

Inventory_label = tk.Label(Frame_right, text="Inventory",font =('Helvetica', 28), width=20, height=2, bg = '#ffffff')
Inventory_label.grid(row =1, column =1)


data = tk.Text(Frame_right, width=100, height=50, state=tk.DISABLED)
data.grid(row =2, column =1)

add= tk.Button(Bottom_frame, text="Add", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
add.grid(row =13, column =6)

modify = tk.Button(Bottom_frame, text="Modify", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
modify.grid(row =13, column =8)

remove = tk.Button(Bottom_frame, text="Remove", width=20, height=2,font =('Helvetica', 18), bg = '#ffffff')
remove.grid(row =13, column =10)

root.mainloop()