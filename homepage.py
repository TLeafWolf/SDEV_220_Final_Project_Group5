import tkinter as tk
from tkinter import messagebox
import sqlite3


root = tk.Tk()
root.title("Main")
root.geometry("1200x650")

top = tk.Frame(root)
top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a bottom frame for the bottom two quadrants
bottom = tk.Frame(root)
bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

left_top= tk.Frame(top, bg="green")
left_top.pack(side ="left", fill=tk.BOTH, expand=True)

Frame_right = tk.Frame(top)
Frame_right.pack(side ="right",fill=tk.BOTH, expand=True)

left_bottom= tk.Frame(bottom, bg="green")
left_bottom.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

Bottom_frame= tk.Frame(bottom)
Bottom_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


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
threshold_label.grid(row =8, column =0, pady=16)

threshold_entry = tk.Entry(left_top)
threshold_entry.grid(row =9, column =0)


result_label = tk.Label(left_top, text="")
result_label.grid(row =10, column =0)


logo = tk.Label(left_top, text="Logo", width=20, height=2,font =('Helvetica', 18), pady=16)
logo.grid(row =0, column =0)

low_stock = tk.Button(left_top, text="Low Stock", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2, command=display_low_inventory)
low_stock.grid(row =5, column =0, pady=16)

Aisle = tk.Button(left_top, text="Aisle", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Aisle.grid(row =1, column =0, pady=16, padx = 16)

Bay = tk.Button(left_top, text="Bay", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Bay.grid(row =2, column =0, pady=16)

Searcha = tk.Button(left_top, text="Search", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Searcha.grid(row =3, column =0, pady=16)

Veiw_all = tk.Button(left_top, text="Veiw all", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Veiw_all.grid(row =4, column =0, pady=16)

Log_out = tk.Button(left_bottom, text="Log out", width=20, height=1, font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Log_out.pack(side=tk.BOTTOM, anchor='w', pady=10, padx = 16)

Inventory_label = tk.Label(Frame_right, text="Inventory",font =('Helvetica', 28), width=20, height=2, bg = '#ffffff')
Inventory_label.pack()


data = tk.Text(Frame_right, width=100, height=30, state=tk.DISABLED)
data.pack(side='left')

add= tk.Button(Bottom_frame, text="Add", width=10, height=1,font =('Helvetica', 18), bg = '#ffffff')
add.grid(row =0, column =6)

modify = tk.Button(Bottom_frame, text="Modify", width=10, height=1,font =('Helvetica', 18), bg = '#ffffff')
modify.grid(row =0, column =8)

remove = tk.Button(Bottom_frame, text="Remove", width=10, height=1,font =('Helvetica', 18), bg = '#ffffff')
remove.grid(row =0, column =10)

root.mainloop()