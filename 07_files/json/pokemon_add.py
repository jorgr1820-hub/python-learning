# Research how to read and write JSON files in Python.
# Create a program that allows adding a new Pokemon to the JSON file.
# It must read the file to import the existing Pokemon.
# Then ask for the information of the new Pokemon.
# Finally save the new Pokemon to the file.

import json


def read_json_file(file_path):
    with open(file_path, "r") as json_pokemon:
        return json.load(json_pokemon)


def save_json_file(data, file_path):
    with open(file_path, "w") as json_pokemon:
        json.dump(data, json_pokemon, indent=4)


def ask_new_pokemon():
    print("\n--- Add new Pokemon ---")
    name = input("Name: ")
    type_ = input("Type: ")
    level = int(input("Level: "))
    return {"name": name, "type": type_, "level": level}


def print_pokemons(pokemons):
    print("\n--- Registered Pokemon ---")
    for pokemon in pokemons:
        print(f"Name: {pokemon['name']}, Type: {pokemon['type']}, Level: {pokemon['level']}")


def main():
    file_path = "/Users/jordan.guzman/python/07_files/json/pokemon.json"

    pokemons = read_json_file(file_path)
    print_pokemons(pokemons)

    new_pokemon = ask_new_pokemon()
    pokemons.append(new_pokemon)

    save_json_file(pokemons, file_path)

    print("\nPokemon added successfully.")
    print_pokemons(pokemons)


main()
