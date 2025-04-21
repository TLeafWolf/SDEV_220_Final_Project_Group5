import sqlite3
from tkinter import *
from tkinter import ttk

def query():
    db_conn = sqlite3.connect("inventory.db")
    c = db_conn.cursor()
    c.execute("SELECT name, price, quantity, Location FROM Supply")
    records = c.fetchall()
    for index, record in enumerate(records):

        formatted_record = (record[0], f"${record[1]:.2f}", record[2], record[3])
        if index % 2 == 0:
            InventoryTreeView.insert("", "end", values=formatted_record, tags=("even_row",))
        else:
            InventoryTreeView.insert("", "end", values=formatted_record, tags=("odd_row",))

    db_conn.close()

root = Tk()
root.title("Inventory Treeview")


frame = Frame(root)
frame.pack(padx=10, pady=10, fill=BOTH, expand=True)


InventoryTreeView = ttk.Treeview(frame, columns=("name", "price", "quantity", "Location"), show='headings', height=10)


InventoryTreeView.heading("name", text="Name", anchor=W)  
InventoryTreeView.heading("price", text="Price", anchor=W)  
InventoryTreeView.heading("quantity", text="Quantity", anchor=W)  
InventoryTreeView.heading("Location", text="Location", anchor=W) 


InventoryTreeView.column("name", anchor=W, width=150)  
InventoryTreeView.column("price", anchor=W, width=100) 
InventoryTreeView.column("quantity", anchor=W, width=100) 
InventoryTreeView.column("Location", anchor=W, width=150)  

scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=InventoryTreeView.yview)
scrollbar.pack(side=RIGHT, fill=Y)


InventoryTreeView.configure(yscrollcommand=scrollbar.set)


InventoryTreeView.pack(side=LEFT, fill=BOTH, expand=True)

InventoryTreeView.tag_configure("even_row", background="lightblue")  
InventoryTreeView.tag_configure("odd_row", background="white")  

query()  
root.mainloop()
