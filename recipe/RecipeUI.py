from ezgraphics import GraphicsWindow  # to make the window
from ezgraphics import GraphicsImage  # to use images on the window
from PIL import Image  # to convert jpg to gif

# class that works with the RecipeProcessor class to print the recipes onto a window
class RecipeUI:

    # constructor that sets all of the values of the window
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.x_init = 20
        self.y_init = 10
        self.x_distance = (self.width) / 4
        self.y_distance = (self.height) / 4 + 5
        self.window = self.setup_window()

    # creates the window and canvas, and returns the window to be used later
    def setup_window(self):
        window = GraphicsWindow(self.width, self.height)
        window.setTitle("Loading recipes...")
        self.canvas = window.canvas()
        return window

    # creates a grid of photos, names, cook_time and prep_time of all
    # recipes provided (either from get_recipes() or get_searched_recipes())
    def layout_ui(self, recipes, search):
        counter = 0
        image_height_incrementer = 0
        for y in range(4):
            for x in range(4):
                if counter < len(recipes):
                    # gets the recipe using the counter
                    recipe = recipes[counter]

                    # converts the image's URL into a .jpg
                    recipe.set_image(recipe.get_image())

                    # converts the .jpg into a .gif
                    image_size = self.convert_imagejpg_to_imagegif()

                    # creates a new GraphicsImage object using the "image.gif" image
                    image = GraphicsImage("image.gif")

                    # draw the image into the canvas at the designated position
                    self.canvas.drawImage(
                        self.x_init + self.x_distance * x,
                        self.y_init + self.y_distance * y,
                        image,
                    )

                    # prints the recipe description
                    x_position = self.x_init + self.x_distance * x
                    image_height = image_size[1]
                    y_position = self.y_init + self.y_distance * y + image_height
                    self.show_recipe_desc(recipe, x_position, y_position)

                    counter += 1

        # set the window title using the number of recipes displayed, number of recipes found, and the search term
        self.window.setTitle(
            "Displaying: "
            + str(counter)
            + "/"
            + str(len(recipes))
            + ' recipe(s) for "'
            + search
            + '"'
        )
        self.window.wait()

    # checks the folder for an image named "image.jpg"
    # then converts that .jpg image into a .gif image,
    # named "image.gif". this image is used in layout_ui()
    # as a GraphicsImage
    def convert_imagejpg_to_imagegif(self):
        scaled_width = 150
        img = Image.open("image.jpg")
        percent_width = scaled_width / float(img.size[0])
        h_size = int((float(img.size[1]) * float(percent_width)))
        img = img.resize((scaled_width, h_size), Image.ANTIALIAS)
        img.save("image.gif")
        return img.size

    # draws text on the canvas at the positions given
    def show_recipe_desc(self, recipe, x, y):
        self.canvas.drawText(x, y, ("Name: " + recipe.get_name()[0:25]))
        self.canvas.drawText(x, y + 20, ("Prep Time: " + recipe.get_prep_time()[0:25]))
        self.canvas.drawText(x, y + 40, ("Cook Time: " + recipe.get_cook_time()[0:25]))