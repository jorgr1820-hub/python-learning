#Cree un programa que lea nombres de canciones de un archivo (línea por línea) 
#y guarde en otro archivo los mismos nombres ordenados alfabéticamente.




songs = {
    "Blinding Lights": "The Weeknd",
    "Shape of You": "Ed Sheeran",
    "Someone Like You": "Adele",
    "Bohemian Rhapsody": "Queen",
    "Billie Jean": "Michael Jackson",
    "Rolling in the Deep": "Adele",
    "Smells Like Teen Spirit": "Nirvana",
    "Uptown Funk": "Bruno Mars",
    "Havana": "Camila Cabello",
    "Bad Guy": "Billie Eilish",
    "Lose Yourself": "Eminem",
    "Counting Stars": "OneRepublic",
    "Despacito": "Luis Fonsi",
    "Thinking Out Loud": "Ed Sheeran",
    "Firework": "Katy Perry",
    "Stay": "Rihanna",
    "Radioactive": "Imagine Dragons",
    "Perfect": "Ed Sheeran",
    "Shallow": "Lady Gaga",
    "Believer": "Imagine Dragons",
    "Closer": "The Chainsmokers",
    "Hello": "Adele",
    "Roar": "Katy Perry",
    "All of Me": "John Legend",
    "Thunder": "Imagine Dragons",
    "Dark Horse": "Katy Perry",
    "God's Plan": "Drake",
    "Take On Me": "A-ha",
    "Sweet Child O' Mine": "Guns N' Roses",
    "Wonderwall": "Oasis",
    "Let It Be": "The Beatles",
    "Hotel California": "Eagles"
}

with open("songs.txt", "w") as song_file:
    for song, artist in songs.items():
        song_file.write(f"{song} - {artist}\n")


with open("songs.txt", "r") as song_file:
    content = song_file.readlines()


print(f"This is the content read from the file:\n{content}\n")


for line in content:
    song, artist = line.strip().split(" - ")
    print(f"{song} - {artist}")

sorted_songs = sorted(content)


with open("songs_sorted.txt", "w") as new_file:
    for line in sorted_songs:
        new_file.write(line)

print("Archivo ordenado creado correctamente")

print(f"Contenido del archivo ordenado:\n{sorted_songs}")