import csv

CSV_PATH = "/Users/jordan.guzman/python/07_files/csv/video_games/video_game.csv"


def read_csv_file():
    with open(CSV_PATH, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def confirm_continue(message):
    while True:
        answer = input(message).strip().upper()
        if answer in ["Y", "YES"]:
            return True
        elif answer in ["N", "NO"]:
            return False
        else:
            print("Invalid answer.")


def search_by_developer():
    games = read_csv_file()
    developer_input = input("Enter the developer name: ").strip().upper()
    found = []
    for game in games:
        if game["Developer"].strip().upper() == developer_input:
            found.append(game)
    if len(found) > 0:
        print(f"\nVideo games developed by {developer_input}:")
        for game in found:
            print(
                f"- {game['Name']} "
                f"(Rating: {game['Rating']}, "
                f"Genre: {game['Genre']})"
            )
    else:
        print("No video games found for that developer.")


def main():
    while True:
        search_by_developer()
        if not confirm_continue("\nSearch another developer? Yes | No: "):
            print("Thank you for using the program.")
            break


main()
