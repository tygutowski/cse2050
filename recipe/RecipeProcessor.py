import re  # to search json
import json  # to read json

from Recipe import Recipe

# class that processes the recipies into a list of recipes. allows loading, searching, and tabulation
class RecipeProcessor:

    # initializes the lists that we need. one for all recipes, and one for searched recipes
    def __init__(self):
        self.recipe_list = []
        self.searched_recipe_list = []

    # search the json, and add all items in the json to the recipe list, creating new recipes for each item
    def load_recipes(self, json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        for item in json_data:
            recipe = Recipe(item)
            recipe.get_name()
            recipe.get_cook_time()
            recipe.get_prep_time()
            self.recipe_list.append(recipe)

    # search the recipe_list for a string. if returns a list of all recipes with the string in the name
    def search_recipes(self):
        search = input("Search: ")
        i = 0
        while i < len(self.recipe_list):
            recipe = self.recipe_list[i]
            name = recipe.get_name()
            if search.lower() in name.lower():
                self.searched_recipe_list.append(recipe)
            i += 1
        return search

    # return all searched recipes (recipes created from search_recipes())
    def get_searched_recipes(self):
        return self.searched_recipe_list

    # returns all recipes (recipes created from load_recipes())
    def get_recipes(self):
        return self.recipe_list

    # displays a tabulation of recipes in the list.
    # if list_type is 0, it will print ALL recipes
    # if list_type is 1, it will print ONLY searched recipes
    def tabulate_recipes(self, list_type):
        recipe_tabulation = {}
        recipe_num = 1
        recipe_list = []
        if list_type == 0:  # if you are printing all recipes, get all recipes
            recipe_list = self.get_recipes()
        elif (
            list_type == 1
        ):  # if you are printing only searched recipes, get only the searched recipes
            recipe_list = self.get_searched_recipes()
        print(f'{"Recipe":<10}{"Name":<40}{"Prep Time":<15}{"Cook Time":<15}{"Yield":<25}')
        for recipe in recipe_list:
            print(f'{str(recipe_num):<10}{recipe.get_name()[0:35]:<35}...  {recipe.get_prep_time():<15}{recipe.get_cook_time():<15}{recipe.get_yield():<25}')
            recipe_num += 1