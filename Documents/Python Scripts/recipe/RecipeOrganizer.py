# import classes
from Recipe import Recipe
from RecipeProcessor import RecipeProcessor
from RecipeUI import RecipeUI


# runner class
def main():
    # create a new processor
    processor = RecipeProcessor()
    # load all recipes in the .json using the processor
    processor.load_recipes("recipes.json")
    # search the processor, using user input
    search = processor.search_recipes()
    # tabluate using list_type 1 (prints ONLY searched recipes. change to 0 to search ALL recipes)
    processor.tabulate_recipes(1)

    # creates a new RecipeUI item
    window = RecipeUI()
    # then layout the UI using the processor
    window.layout_ui(processor.get_searched_recipes(), search)

# call main
main()
