import pickle

# Function to display a recipe
def display_recipe(recipe):
    print(f"""
    Recipe Name: {recipe['name']}
    Cooking Time: {recipe['cooking_time']} minutes
    Ingredients: {", ".join(recipe['ingredients'])}
    Difficulty: {recipe['difficulty']}
    """)

# Function to search for an ingredient
def search_ingredient(data):
    all_ingredients = data['all_ingredients']

    print("The available ingredients are: ")
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")
    
    try:
        ingredient_num = int(input("Enter the number corresponding to the ingredient you would like to search for: "))
        ingredient_searched = all_ingredients[ingredient_num-1]
    except (ValueError, IndexError):
        print("Invalid input! Please enter a valid ingredient number.")
    else:
        print("Recipes containing", ingredient_searched + ":")
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

filename = input("Enter the name of the file to load the recipes from (without extension): ")
filename += ".bin"

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please try again.")
else:
    file.close()
    search_ingredient(data)