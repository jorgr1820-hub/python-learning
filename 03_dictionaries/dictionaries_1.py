
#This program creates a dictionary and reads and print those elements until it found the stars, 
# then it reads the room list and print the dictionary elements.

hotel = {
    "name" : "Trivago",
    "stars": 4,
    "rooms" :[
        {
            "number" : "room 1"  , 
            "floor" : 1 , 
            "price_per_night" : 700
            }, 

        {"number" : "room 2"  , 
            "floor" : 2 , 
            "price_per_night" : 800
            }, 
        {"number" : "room 3"  , 
            "floor" : 3 , 
            "price_per_night" : 9000
            }, 
        {"number" : "room 4"  , 
            "floor" : 4 , 
            "price_per_night" : 1000
            }
            
        ]
    }

for key , value in hotel.items():
    print(key, ":" ,value)
    if key == "stars":
        break

for room in hotel["rooms"]:
    print(
        f"\nRoom #{room["number"]}"
        f"\nFloor:{room["floor"]}"
        f"\nPrice per night:${room["price_per_night"]}"
        )


