# to do 
# need a data base or some way to store these added data
# potentially display this final as a website

class DataAdd:
    def __init__(self):
        self.data = {}

    def get_input(self):
        Item_ID = input("Enter the items ID: ")
        name = input("Enter the Items name: ")
        count = input("How many of that item do we have?: ")
        price = input("What is their price?: ")
        aisle= input("What aisle is it going in?(aisle A-F): ")
        bay= input("What bay is it going in?(bay 1-20): ")
        print("Added Data:")
        print(f"{Item_ID} : {name}: {count} : {price}: {aisle} : {bay}")



 
        

# Example usage
storage = DataAdd()
storage.get_input()
