# Read about the rest of the csv module methods and create an alternative version
# of the exercise above that saves the file separated by tabs instead of commas.

import csv

CSV_PATH = "/Users/jordan.guzman/python/07_files/csv/video_games/video_game_tabulated.csv"

video_games = []


def ask_quantity():
    while True:
        try:
            quantity = int(input("Enter the number of video games to add: "))
            if quantity > 0:
                return quantity
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def ask_game_info():
    name = input("Enter the game name: ")
    genre = input("Enter the game genre: ")
    developer = input("Enter the game developer: ")
    rating = input("Enter the ESRB rating: ")
    return {
        "Name": name,
        "Genre": genre,
        "Developer": developer,
        "Rating": rating
    }


quantity = ask_quantity()
for x in range(quantity):
    print(f"\nEnter information for video game {x + 1}:")
    game = ask_game_info()
    video_games.append(game)


with open(CSV_PATH, "w", newline="") as csvfile:
    fieldnames = ["Name", "Genre", "Developer", "Rating"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    for game in video_games:
        writer.writerow(game)

print("\nVideo game information saved to video_game_tabulated.csv")
