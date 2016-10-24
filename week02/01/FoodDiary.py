"""
The problem where you write what you are eating write now.
That program would be really helpful if you are a fat panda and you are trying to track your meals.

Write a program that have two options:
Ask "what are you eating now?" and save the given information.
List all the meals that you took for a given date.
Write all that information in file in such a format that you could read it later.

$ python3 food.py
Hello and Welcome!
Choose an option.
1. meal - to write what are you eating now.
2. list <dd.mm.yyyy> - lists all the meals that you ate that day,

Enter command>

meal

meal - food you are eating write now

That option saves in to file the meal and the date write now.

$ python3 food.py
Hello and Welcome!
Choose an option.
1. meal - to write what are you eating now.
2. list <dd.mm.yyyy> - lists all the meals that you ate that day,

Enter command> meal pizza
Ok it is saved
Enter command> meal pasta
Ok it is saved
list

That option list all the meals that you took in a current day.

Example:

Hello and Welcome!
Choose an option.
1. meal - to write what are you eating now.
2. list <dd.mm.yyyy> - lists all the meals that you ate that day,

Enter command> list 25.11.2015
pizza
pasta
Google "how to get current date in python"

Good luck!
"""
from datetime import datetime
import csv

CSV_FILE_PATH = 'foods.csv'


def main():
    today = datetime.now()
    date_str = "{:%d.%m.%Y}".format(today)

    print("Hello and Welcome!")
    print("Choose an option.")
    print("1.meal - to write what you are eating now.")
    print('2.list <dd.mm.yyyy> - lists all the meals that you ate that day')

    while True:
        command = input('Enter command>')
        if command[:4] == "meal":
            quantity = input('How much have you eaten?>')
            meal = command[5:]
            grams = get_quantity_in_grams(quantity)

            calories_per_100g = int(input("How much calories per 100g?>"))

            save_to_csv(date_str, meal, grams, calories_per_100g)

            print("Ok this it a total of {calories} calories for this meal.".format(
                calories=calories_per_100g * (grams/100)
            ))
        elif command[:4] == "list":
            date = command[5:]

            foods_eaten_at_that_date, _ = get_date_foods(date)
            if not foods_eaten_at_that_date:
                print("You did not eat anything on {}".format(date))
            else:
                for meal in foods_eaten_at_that_date[::3]:  # step 3 because they're ordered food, grams, calories
                    print(meal)


def get_quantity_in_grams(input_quantity: str) -> int:
    """ given a string 200g or 2kg, return the result in grams"""

    if input_quantity.endswith('kg'):
        kilograms = int(input_quantity[:-2])
        grams = kilograms * 1000
    else:
        grams = int(input_quantity[:-1])

    return grams


def save_to_csv(date_str: str, food: str, grams: int, calories_per_100g: int):
    """ save information to the CSV in the format
        date_str, food
        first by getting the information we have and appending the food where necessary"""
    # get old csv values
    with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as _:
        reader = csv.reader(_)
        old_values = list(reader)

    with open(CSV_FILE_PATH, mode='w', encoding='utf-8') as _:
        writer = csv.writer(_)

        eaten_foods, idx = get_date_foods(date_str, old_values)
        # append the date to the list
        eaten_foods.insert(0, date_str)
        # add the food to the list
        eaten_foods.extend([food, grams, calories_per_100g])

        if idx is None:
            old_values.append(eaten_foods)
        else:
            old_values[idx] = eaten_foods  # update the old values

        writer.writerows(old_values)


def get_date_foods(date_str: str, csv_values=None):
    """
    this function returns a list of all the foods we've eaten at a given date
    returns a list with the associated date and it's index
    """
    if not csv_values:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as _:
            reader = csv.reader(_)
            csv_values = list(reader)

    for idx, list_ in enumerate(csv_values):
        if list_[0] == date_str:
            return list_[1:], idx

    return [], None


if __name__ == "__main__":
    main()