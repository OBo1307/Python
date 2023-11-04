import pickle

# Function to take a recipe from the user
def take_recipe():

    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients of the recipe (separated by commas): ").split(",")
    difficulty = calc_difficulty(cooking_time, len(ingredients))

    recipe = {
        "name": name, 
        "cooking_time": cooking_time, 
        "ingredients": ingredients,
        "difficulty": difficulty
        }
    
    return recipe

# Function to calculate the difficulty level of a recipe
def calc_difficulty(cooking_time, ingredient_cnt):
    if cooking_time < 10 and ingredient_cnt < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and ingredient_cnt >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and ingredient_cnt < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and ingredient_cnt >= 4:
        difficulty = "Hard"
    
    return difficulty

filename = input("Enter the name of the file to save the recipes: ")

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Creating a new file...")
    data = {'recipes_list': [], 'all_ingredients': []}
except:
    print("Something went wrong. Please try again.")
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

n = int(input("Enter the number of recipes you would like to add: "))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

try:
    with open(filename, "wb") as file:
        pickle.dump(data, file)
        print("Data saved successfully.")
except:
    print("Something went wrong. Please try again.")
else:
    file.close()
finally:
    print("Thank you for using the Recipe App.")