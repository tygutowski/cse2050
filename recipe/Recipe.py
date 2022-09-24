import requests  # to download file from url


# class the contains all recipe data
class Recipe:

    # constructor that sets up the necessary variables
    # item is the dictionary supplied by the RecipeProcessor
    # item is a dictionary, and can be searched to get values
    def __init__(self, item):
        self.item = item

    # checks item
    def get_name(self):
        return self.item["name"]

    # returns the raw cook time of an item. this is unformatted, and is formatted later
    def get_cook_time(self):
        cook_time = self.item["cookTime"]
        return self.format_time(cook_time)

    # returns the raw prep time of an item. this is unformatted, and is formatted later
    def get_prep_time(self):
        prep_time = self.item["prepTime"]
        return self.format_time(prep_time)

    # returns the yield of a recipe from an item
    def get_yield(self):
        return self.item["recipeYield"]

    # downloads the a .jpg file given its URL. this is converted to a .gif later
    # in order to save resources
    def set_image(self, url):
        img_data = requests.get(url).content
        with open("image.jpg", "wb") as handler:
            handler.write(img_data)

    # gets the name of an recipe's URL image from the item json.
    def get_image(self):
        return self.item["image"]

    # formats time in a MM:HH format with leading zeros
    def format_time(self, time):
        if time:  # If the time has a value
            hours = re.search(r"\d{1,2}H", time)
            minutes = re.search(r"\d{1,2}M", time)
            days = re.search(r"\d{1,2}D", time)
            if (
                hours or minutes or days
            ):  # If the time is in correct format (ex. 1D8H35M)
                if minutes: # if there are minutes
                    minutes = minutes.group(0)[0:-1]
                else:
                    minutes = 0
                minutes = int(minutes)

                if hours: # if there are hours
                    hours = hours.group(0)[0:-1]
                else:
                    hours = 0
                hours = int(hours)
                if days: # if there are days
                    days = days.group(0)[0:-1]
                else:
                    days = 0
                days = int(days)
                hours += days * 24
                minutes += hours * 60
                hours = minutes / 60
                hours = int(hours)
                minutes %= 60
                hours = str(hours)
                minutes = str(minutes)

                # add leading zeros
                if len(hours) == 1:
                    hours = "0" + hours
                if len(minutes) == 1:
                    minutes += "0"
                return hours + ":" + minutes
            else:  # If time is in fucky format (ex. 1 day 3 hours 10 minutes)
                hours = re.search(r"\d{1,2} hour", time)
                minutes = re.search(r"\d{1,2} minute", time)
                days = re.search(r"\d{} day", time)
                if minutes:
                    minutes = minutes.group(0).split()[0]
                else:
                    minutes = 0
                minutes = int(minutes)

                if hours:
                    hours = hours.group(0).split()[0]
                else:
                    hours = 0
                hours = int(hours)
                if days:
                    days = days.group(0).split()[0]
                else:
                    days = 0
                days = int(days)
                hours += days * 24
                minutes += hours * 60
                hours = minutes / 60
                hours = int(hours)
                minutes %= 60
                hours = str(hours)
                minutes = str(minutes)
                if len(hours) == 1:
                    hours = "0" + hours
                if len(minutes) == 1:
                    minutes += "0"
                return hours + ":" + minutes
        else:  # If time has no value, assume it's instantaneous
            return "00:00"