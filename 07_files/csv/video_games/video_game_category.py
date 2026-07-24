
# Create a program that opens a .csv file with video game information
# (the one generated in exercise 1) and:
# Reads each line using csv.reader()
# Displays the content on screen in a readable format, line by line

import csv

CSV_PATH = "/Users/jordan.guzman/python/07_files/csv/video_games/video_game.csv"


def read_csv_file():
    with open(CSV_PATH, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def input_game_rating():
    print("Enter the game rating:\nE-Everyone| E10+ | T-Teen| M-Mature | AO-Adults Only | RP-Rating Pending")
    valid_ratings = ["E", "E10+", "T", "M", "AO", "RP", "EVERYONE", "TEEN", "MATURE", "ADULTS ONLY", "RATING PENDING"]
    while True:
        rating = input("Enter the game rating: ").strip().upper()
        if rating in valid_ratings:
            return rating
        else:
            print("Invalid rating. Please enter a rating using the available options.\nE-Everyone| E10+ | T-Teen| M-Mature | AO-Adults Only | RP-Rating Pending")


def confirm_continue(message):
    while True:
        answer = input(message).strip().upper()
        if answer in ["Y", "YES"]:
            return True
        elif answer in ["N", "NO"]:
            return False
        else:
            print("Invalid answer.")


def count_video_games():
    games = read_csv_file()
    print(f"Total video games found: {len(games)}")


def main():
    user_rating = input_game_rating()
    games = read_csv_file()
    found = False
    for game in games:
        if game["Rating"] == user_rating:
            print(f"Found: {game['Name']}")
            found = True
            count_video_games()
    if not found:
        print("No video games found.")
    if confirm_continue("Search another rating? Yes | No: "):
        main()
    else:
        print("Thank you for using the program.")


main()
