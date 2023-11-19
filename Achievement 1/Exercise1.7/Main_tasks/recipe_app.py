# Import necessary packages
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Create engine and session
engine = create_engine("mysql+mysqlconnector://cf-python:pythonpass@localhost/task_database")

Session = sessionmaker(bind=engine)
session = Session()

# Create base class
Base = declarative_base()

# Create Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def calculate_difficulty(self):
        ingredients_num = len(self.ingredients.split(", "))
        if self.cooking_time < 10 and ingredients_num < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and ingredients_num >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and ingredients_num < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
    
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            return self.ingredients.split(", ")

    def __repr__(self):
        return "<RecipeID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"
    
    def __str__(self):
        recipe_str = "-" * 16 + "\n"
        recipe_str += f"RecipeID: {self.id}\n"
        recipe_str += f"Recipe: {self.name}\n"
        recipe_str += f"Dificulty: {self.difficulty}\n"
        recipe_str += f"Ingredients:\n"
        ingredients_list = self.ingredients.split(", ")
        for ingredient in ingredients_list:
            recipe_str += f"\t- {ingredient.strip()}\n"
        recipe_str += f"Cooking time: {self.cooking_time} minutes\n"
        recipe_str += "-" * 16 + "\n"
        return recipe_str

# Create the corresponding table in the database
Base.metadata.create_all(engine)

# Function to create a new recipe
def create_recipe():
    name = input("Enter the name of the recipe: ")
    while len(name) > 50 or not name.strip():
        if len(name) > 50:
            print("The recipe name should not exceed 50 characters.")
        else:
            print("The recipe name should not be empty.")
        name = input("Enter the name of the recipe: ")
    
    num_ingredients = input("Enter the number of ingredients: ")
    while not num_ingredients.isdigit():
        print("Invalid number of ingredients. Please enter a valid number.")
        num_ingredients = input("Enter the number of ingredients: ")

    num_ingredients = int(num_ingredients)
    ingredients = []
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i + 1}: ")
        ingredients.append(ingredient)

    while not ingredients:
        print("The ingredients field cannot be empty.")
        ingredients = []
        for i in range(num_ingredients):
            ingredient = input(f"Enter ingredient {i + 1}: ")
            ingredients.append(ingredient)

    sorted_ingredients = sorted(ingredients)
    ingredients_str = ", ".join(sorted_ingredients)
    
    cooking_time = input("Enter the cooking time (in minutes): ")
    while not cooking_time.isnumeric():
        print("Invalid cooking time. Please enter a valid number.")
        cooking_time = input("Enter the cooking time (in minutes): ")
    
    recipe_entry = Recipe(
        name=name, 
        ingredients=ingredients_str, 
        cooking_time=int(cooking_time)
        )
    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()

    print("Recipe created successfully!")

# Function to see all recipes
def view_all_recipes():
    print("\nAll Recipes:")
    print("="*45)
    recipes = session.query(Recipe).all()

    if not recipes:
        print("No recipes found in the database.")
        return None
    for recipe in recipes:
        print(recipe)

# Function to search for a recipe by ingredient
def search_by_ingredients():
    # Check if there are any recipes in the database
    count = session.query(Recipe).count()
    if count == 0:
        print("No recipes found in the database.")
        return None
    
    # Retrieve all the ingredients and store them in a list
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    all_ingredients.sort()

    # Display the available ingredients to the user
    print("\nAvailable ingredients: ")
    print("="*45)
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")
    
    # Ask the user to select ingredients by their numbers
    user_input = input("Enter the ingredient numbers separated by spaces: ")
    user_input = user_input.strip().split()

    # Validate the user's input
    for number in user_input:
        if not number.isnumeric() or int(number) < 1 or int(number) > len(all_ingredients):
            print("Invalid ingredient number(s). Please try again.")
            return None
    
    search_ingredients = [all_ingredients[int(number) - 1] for number in user_input]

    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Perform the query to retrieve matching recipes
    recipes = session.query(Recipe).filter(*conditions).all()

    # Display the matching recipes
    print(f"\nRecipes containing {search_ingredients}:")
    if not recipes:
        print("No recipes found matching the given ingredients.")
    else:
        for recipe in recipes:
            print(recipe)

# Function to edit an existing recipe
def edit_recipe():
    # Check if there are any recipes in the database
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found in the database.")
        return
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:")
    print("="*45)
    for recipe_id, recipe_name in results:
        print(f"{recipe_id}. {recipe_name}")
    
    try:
        chosen_id = int(input("Enter the ID of the recipe you want to edit: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    recipe_to_edit = session.query(Recipe).get(chosen_id)
    if not recipe_to_edit:
        print("No recipe found with the given id.")
        return
    
    print("\nRecipe to Edit:")
    print("1. Name:", recipe_to_edit.name)
    print("2. Ingredients:", recipe_to_edit.ingredients)
    print("3. Cooking time:", recipe_to_edit.cooking_time)

    attribute_choice = input("Enter the number corresponding to the attribute you want to edit: ")

    if attribute_choice == "1":
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute_choice == "2":
        new_ingredients = input("Enter the new ingredients (separated by commas): ")
        recipe_to_edit.ingredients = new_ingredients
    elif attribute_choice == "3":
        new_cooking_time = input("Enter the new cooking time: ")
        recipe_to_edit.cooking_time = int(new_cooking_time)
    else:
        print("Invalid choice.")
        return
    
    # Update the difficulty of the recipe
    recipe_to_edit.calculate_difficulty()

    # Commit the changes to the database
    session.commit()

    print("Recipe updated successfully!")

# Function to delete a recipe
def delete_recipe():
    # Check if there are any recipes in the database
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found in the database.")
        return
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:")
    for recipe_id, recipe_name in results:
        print(f"{recipe_id}. {recipe_name}")
    
    chosen_id = input("Enter the ID of the recipe you want to delete: ")
    if not chosen_id.isdigit():
        print("Invalid ID. Please entera a number.")
        return

    recipe_to_delete = session.query(Recipe).get(chosen_id)
    if not recipe_to_delete:
        print("No recipe found with the given id.")
        return
    
    confirm = input(f"Are you sure you want to delete the recipe '{recipe_to_delete.name}'? (yes/no): ")
    if confirm.lower() == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Deletion canceled.")

    

# Function for the main menu
def main_menu():
    while True:
        print("\nMAIN MENU:")
        print("="*45)
        print("What would you like to do? Pick a choice!")
        print(" 1. Create a new recipe")
        print(" 2. Search for a recipe by ingredients")
        print(" 3. Update an existing recipe")
        print(" 4. Delete a recipe")
        print(" 5. View all recipes")
        print("\n   Type 'quit' to exit the program")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        elif choice == "quit":
            session.close()
            engine.dispose()
            break
        else:
            print("Invalid choice.")

main_menu()
print("Goodbye!")