import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="cf-python",
    passwd="pythonpass")

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database;")

cursor.execute("USE task_database;")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
               )''')

# Function to create a new recipe
def create_recipes(conn, cursor):
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients separated by commas: ").split(", ")
    difficulty = calculate_difficulty(cooking_time, ingredients)

    # Sort the ingredients alphabetically
    ingredients.sort()

    # Convert ingredients list to a comma-separated string
    ingredients_str = ", ".join(ingredients)

    # Insert the recipe into the database
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    values = (name, ingredients_str, cooking_time, difficulty)
    cursor.execute(query, values)
    
    conn.commit()

    print("Recipe created successfully!")

# Function to calculate the difficulty of a recipe
def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    return difficulty

# Function to search for a recipe
def search_recipes(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = []
    for result in results:
        ingredients = result[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    # Display the available ingredients to the user
    print("\nAvailable ingredients: ")
    print("="*45)
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}. {ingredient}")
    
    try:
        # Ask the user to select an ingredient to search for
        ingredient_index = int(input("Choose an ingredient to search for (enter the corresponding number): "))
        search_ingredient = all_ingredients[ingredient_index - 1]
    except ValueError:
        print("Please enter a valid number.")
    except IndexError:
        print("Please enter a valid ingredient number.")
    else:
        # Search for recipes containing the selected ingredient
        print(f"\nRecipes containing {search_ingredient}:")
        print("="*45)
        cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s", ("%" + search_ingredient + "%",))
        search_results = cursor.fetchall()

        for result in search_results:
            print("\nID: ", result[0])
            print("Name: ", result[1])
            print("Ingredients: ", result[2])
            print("Cooking Time: ", result[3])
            print("Difficulty: ", result[4])

# Function to update an existing recipe
def update_recipes(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes;")
    recipes = cursor.fetchall()
    print("Available recipes: ")
    for recipe in recipes:
        print(f"{recipe[0]}. {recipe[1]}")
    
    recipe_id = int(input("Select a recipe to update (enter the corresponding ID): "))
    print("Select the column to update: ")
    print("1. Name")
    print("2. Cooking time")
    print("3. Ingredients")
    col_choice = int(input("Enter your choice: "))

    new_value = input("Enter the new value: ")

    if col_choice == 1:
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_value, recipe_id))
    elif col_choice == 2:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        cooking_time = int(new_value)
        ingredients = recipe[1].split(", ")
        difficulty = calculate_difficulty(cooking_time, ingredients)
        cursor.execute("UPDATE Recipes SET cooking_time = %s, difficulty = %s WHERE id = %s", (cooking_time, difficulty, recipe_id))
    elif col_choice == 3:
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_value, recipe_id))
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        ingredients = new_value
        difficulty = calculate_difficulty(cooking_time, ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))
    else:
        print("Invalid choice.")
        return
    
    conn.commit()

    print("Recipe updated successfully!")

# Function to delete a recipe
def delete_recipes(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes;")
    recipes = cursor.fetchall()

    print("Available recipes: ")
    for recipe in recipes:
        print(f"{recipe[0]}. {recipe[1]}")
    
    recipe_id = int(input("Select a recipe to delete (enter the corresponding ID): "))

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()

    print("Recipe deleted successfully!")

# Function to see all recipes
def view_recipes(conn, cursor):
    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes;")
    all_recipes = cursor.fetchall()

    if all_recipes:
        print("All Recipes:")
        print("="*45)
        for recipe in all_recipes:
            print("ID: ", recipe[0])
            print("Name: ", recipe[1])
            print("Ingredients: ", recipe[2])
            print("Cooking Time: ", recipe[3])
            print("Difficulty: ", recipe[4])
            print("-"*45)
    else:
        print("No recipes found.")

# Function for the main menu
def main_menu(conn, cursor):
    while True:
        print("\nMAIN MENU:")
        print("="*45)
        print("What would you like to do? Pick a choice!")
        print(" 1. Create a new recipe")
        print(" 2. Search for a recipe by ingredient")
        print(" 3. Update an existing recipe")
        print(" 4. Delete a recipe")
        print(" 5. View all recipes")
        print("\n   Type 'quit' to exit the program")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_recipes(conn, cursor)
        elif choice == "2":
            search_recipes(conn, cursor)
        elif choice == "3":
            update_recipes(conn, cursor)
        elif choice == "4":
            delete_recipes(conn, cursor)
        elif choice == "5":
            view_recipes(conn, cursor)
        elif choice == "quit":
            break
        else:
            print("Invalid choice.")

main_menu(conn, cursor)
print("Goodbye!")

