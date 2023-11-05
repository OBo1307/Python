class Shoppinglist:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    
    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f"Added {item} to the shopping list.")
        else:
            print(f"{item} is already on the shopping list.")
    
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f"Removed {item} from the shopping list.")
        else:
            print(f"{item} is not on the shopping list.")
    
    def view_list(self):
        print(f"Shopping List: {self.list_name}")
        print("Items:")
        for item in self.shopping_list:
            print("- " + item)

pet_store_list = Shoppinglist("Pet Store Shopping List")

pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

pet_store_list.remove_item("flea collars")

pet_store_list.add_item("frisbee")

pet_store_list.view_list()