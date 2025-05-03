import os
import sqlite3
import django
from inventory.models import Supply as DjangoSupply


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings') 
django.setup()


project_directory = os.path.dirname(os.path.abspath(__file__))


db_path = os.path.join(project_directory, "Inventory.db")


con = sqlite3.connect(db_path)
cur = con.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS Supply
               (name text PRIMARY KEY, price real, quantity INTEGER, location text)''')


con.commit()




def insert_supply(name, price, quantity, location):
    new_supply = DjangoSupply(name=name, price=price, quantity=quantity, location=location)
    new_supply.save()
    print(f"Supply item '{name}' added with price {price}, quantity {quantity}, and location {location}.")


insert_supply('Cat Food z', 30.00, 15, 'C5')
insert_supply('Dog Food z', 30.00, 15, 'C5')


for row in cur.execute('''SELECT * FROM Supply'''):
    print(row)


con.close()
