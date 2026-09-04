import json

def write_json_file(pokemon_list):
    with open(
        "/Users/jordan.guzman/python/07_files/json/pokemon.json",
        "w"
    ) as json_pokemon:
        json.dump(pokemon_list, json_pokemon, indent=4)


pokemon_list = [
    {
        "name": "Pikachu",
        "type": "Electric",
        "level": 54,
        "weight_kg": 6.0,
        "is_shiny": False,
        "held_item": None,
        "skills": [
            "Thunder Shock",
            "Quick Attack",
            "Thunderbolt",
            "Volt Tackle"
        ],
        "stats": {
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "sp_attack": 50,
            "sp_defense": 50,
            "speed": 90
        }
    },
    {
        "name": "Charmander",
        "type": "Fire",
        "level": 8,
        "weight_kg": 8.5,
        "is_shiny": True,
        "held_item": "Charcoal",
        "skills": [
            "Ember",
            "Scratch",
            "Tackle",
            "Smokescreen"
        ],
        "stats": {
            "hp": 39,
            "attack": 52,
            "defense": 43,
            "sp_attack": 60,
            "sp_defense": 50,
            "speed": 65
        }
    }
]

write_json_file(pokemon_list)