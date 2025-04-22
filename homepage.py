import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3

def open_view_page():
    subprocess.Popen(["python", "view.py"])
    
root = tk.Tk()
root.title("Main")
root.geometry("1200x850")

top = tk.Frame(root)
top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Alert System")

     
        self.conn = sqlite3.connect('inventory.db')  
        self.cursor = self.conn.cursor()

        self.alert_threshold = 10  # Threshold for alert

        # label for inventory alerts
        self.label = tk.Label(left_top, text="", font=("Helvetica", 16))
        self.label.grid(row=8, column=0, padx=20, pady=20)

        # button to refresh inventory 
        self.button = tk.Button(left_top, text="Refresh Inventory", command=self.check_inventory, bg = 'yellow', borderwidth=2, width=20, height=1,font =('Helvetica', 18))
        self.button.grid(row=9, column=0, padx=20, pady=10)

        self.check_inventory() 

    def check_inventory(self):
        # Query the inventory from the database
        self.cursor.execute("SELECT name, quantity FROM Supply")  # Adjust the table name if needed
        items = self.cursor.fetchall()

        low_inventory_count = sum(1 for item in items if item[1] < self.alert_threshold)

        if low_inventory_count > 0:
            self.label.config(text=f"Inventory Alert: {low_inventory_count} items low in stock!", fg="red")
        else:
            self.label.config(text="Inventory Level: Sufficient", fg="black")

        # Checks inventory again after 2000 milliseconds (2 seconds)
        self.root.after(2000, self.check_inventory)

    def simulate_inventory_change(self):
        self.inventory_level -= 1
        if self.inventory_level < 0:
            self.inventory_level = 10

    def __del__(self):
        # Closes the database connection when the app is closed
        self.conn.close()


logo = tk.Label(left_top, text="Logo", width=20, height=2,font =('Helvetica', 18), pady=16)
logo.grid(row =0, column =0)

#for veiw section
# aisle and bay are for veiwing section via aisle or aisle+bay to figure out which section of the store to veiw items in
Aisle = tk.Button(left_top, text="Aisle", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Aisle.grid(row =1, column =0, pady=16, padx = 16)

Bay = tk.Button(left_top, text="Bay", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Bay.grid(row =2, column =0, pady=16)

# for search
Searcha = tk.Button(left_top, text="Search", width=20, height=1,font =('Helvetica', 18), bg = 'yellow', borderwidth=2)
Searcha.grid(row =3, column =0, pady=16)

# for veiw all
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

#root.mainloop()
if __name__ == "__main__":
    app = InventoryApp(root)
    #root = tk.Tk()
    root.mainloop()
