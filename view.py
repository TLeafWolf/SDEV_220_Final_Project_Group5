# view.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ViewPage:
    def __init__(self, master):
        self.master = master
        self.master.title("View Inventory")
        self.master.geometry("1000x600")

        control_frame = tk.Frame(master)
        control_frame.pack(pady=10)

        self.mode = tk.StringVar(value="all")
        tk.Radiobutton(control_frame, text="View All", variable=self.mode, value="all", command=self.refresh).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(control_frame, text="View by Section", variable=self.mode, value="section", command=self.refresh).pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Aisle:").pack(side=tk.LEFT)
        self.aisle_entry = tk.Entry(control_frame, width=10)
        self.aisle_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Bay:").pack(side=tk.LEFT)
        self.bay_entry = tk.Entry(control_frame, width=10)
        self.bay_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Search", command=self.refresh).pack(side=tk.LEFT, padx=10)

        self.tree = ttk.Treeview(master, columns=("Name", "Price", "Qty", "Location"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        action_frame = tk.Frame(master)
        action_frame.pack()

        tk.Button(action_frame, text="Add Item", command=self.add_item_popup).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Edit Selected", command=self.edit_selected_item).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Delete Selected", command=self.delete_selected_item).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def get_connection(self):
        return sqlite3.connect("inventory.db")

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        query = "SELECT name, price, quantity, Location FROM Supply"
        params = ()

        if self.mode.get() == "section":
            aisle = self.aisle_entry.get().strip()
            bay = self.bay_entry.get().strip()
            if aisle and bay:
                query += " WHERE Location LIKE ?"
                params = (f"%Aisle {aisle}, Bay {bay}%",)
            elif aisle:
                query += " WHERE Location LIKE ?"
                params = (f"%Aisle {aisle}%",)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

    def add_item_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Add Item")

        tk.Label(popup, text="Name").grid(row=0, column=0)
        tk.Label(popup, text="Price").grid(row=1, column=0)
        tk.Label(popup, text="Quantity").grid(row=2, column=0)
        tk.Label(popup, text="Aisle").grid(row=3, column=0)
        tk.Label(popup, text="Bay").grid(row=4, column=0)

        name = tk.Entry(popup)
        price = tk.Entry(popup)
        quantity = tk.Entry(popup)
        aisle = tk.Entry(popup)
        bay = tk.Entry(popup)

        name.grid(row=0, column=1)
        price.grid(row=1, column=1)
        quantity.grid(row=2, column=1)
        aisle.grid(row=3, column=1)
        bay.grid(row=4, column=1)

        def submit():
            loc = f"Aisle {aisle.get()}"
            if bay.get():
                loc += f", Bay {bay.get()}"
            with self.get_connection() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO Supply (name, price, quantity, Location) VALUES (?, ?, ?, ?)", 
                          (name.get(), float(price.get()), int(quantity.get()), loc))
                conn.commit()
            popup.destroy()
            self.refresh()

        tk.Button(popup, text="Add", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

    def edit_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an item to edit.")
            return

        item = self.tree.item(selected[0])["values"]
        name, price, quantity, location = item

        popup = tk.Toplevel(self.master)
        popup.title("Edit Item")

        tk.Label(popup, text="Name").grid(row=0, column=0)
        tk.Label(popup, text="Price").grid(row=1, column=0)
        tk.Label(popup, text="Quantity").grid(row=2, column=0)
        tk.Label(popup, text="Location").grid(row=3, column=0)

        name_entry = tk.Entry(popup)
        price_entry = tk.Entry(popup)
        quantity_entry = tk.Entry(popup)
        location_entry = tk.Entry(popup)

        name_entry.insert(0, name)
        price_entry.insert(0, price)
        quantity_entry.insert(0, quantity)
        location_entry.insert(0, location)

        name_entry.grid(row=0, column=1)
        price_entry.grid(row=1, column=1)
        quantity_entry.grid(row=2, column=1)
        location_entry.grid(row=3, column=1)

        def update():
            with self.get_connection() as conn:
                c = conn.cursor()
                c.execute("""
                    UPDATE Supply SET name=?, price=?, quantity=?, Location=?
                    WHERE name=? AND Location=?
                """, (name_entry.get(), float(price_entry.get()), int(quantity_entry.get()),
                      location_entry.get(), name, location))
                conn.commit()
            popup.destroy()
            self.refresh()

        tk.Button(popup, text="Save Changes", command=update).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an item to delete.")
            return

        item = self.tree.item(selected[0])["values"]
        name, location = item[0], item[3]

        if messagebox.askyesno("Confirm Delete", f"Delete '{name}' from inventory?"):
            with self.get_connection() as conn:
                c = conn.cursor()
                c.execute("DELETE FROM Supply WHERE name=? AND Location=?", (name, location))
                conn.commit()
            self.refresh()
