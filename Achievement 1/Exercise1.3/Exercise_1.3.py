# Initialize two empty lists
recipes_list = []
ingredients_list = []

# Function to add a recipe
def take_recipe():
    # Get the name of the recipe
    name = input("Enter the name of the recipe: ")

    # Get the cooking time of the recipe
    cooking_time = int(input("Enter the cooking time (in minutes): "))

    # Get the ingredients of the recipe
    ingredients = input("Enter the ingredients of the recipe (separated by commas): ").split(",")

    # Create a dictionary for the recipe
    recipe = {
        "name": name, 
        "cooking_time": cooking_time, 
        "ingredients": ingredients
        }
    
    return recipe

# Ask the user how many recipes they would like to add
n = int(input("Enter the number of recipes you would like to add: "))

for i in range(n):
    # Run the function to add a recipe details
    recipe = take_recipe()

    # Iterate through the recipe's ingredients list and add them to the ingredients_list if they are not already present
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    # Add the recipe to the recipe_list
    recipes_list.append(recipe)

# Iterate through the recipes_list and display each recipe in the given format
for recipe in recipes_list:
    cooking_time = recipe["cooking_time"] 
    ingredient_cnt = len(recipe["ingredients"]) 

    if cooking_time < 10 and ingredient_cnt < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and ingredient_cnt >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and ingredient_cnt < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and ingredient_cnt >= 4:
        difficulty = "Hard"
    
    # Display the recipe details
    print("Recipe: ", recipe["name"])
    print("Cooking Time: ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty level: ", difficulty)

# Print all the ingredients in alphabetical order
print("Ingredients Available Across All Recipes: ")
ingredients_list.sort()
for ingredient in ingredients_list:
    print(ingredient)