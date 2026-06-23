condo_houses = [
    {
        "number": 93,
        "area_m2": 125,
        "rooms": [
            "living_room",
            "kitchen",
            "main_sleeping_room",
            "second_sleeping_room",
            "bathroom"
        ],
    },
    {
        "number": 95,
        "area_m2": 125,
        "rooms": [
            "living_room",
            "kitchen",
            "main_sleeping_room",
            "second_sleeping_room",
            "third_sleeping_room",
            "bathroom"
        ],
    },
]






for house in condo_houses:
    print(house["number"])
    for room in house["rooms"]:
        print(" -", room)
