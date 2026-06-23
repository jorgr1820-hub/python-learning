
#Cree un programa que abra un archivo .csv con la información de videojuegos (el que fue generado en el ejercicio 1) y:
#Lea cada línea usando csv.reader()
#Muestre el contenido en pantalla de forma legible, línea por línea




import csv


def read_CSV_file():
    with open("/Users/jordan.guzman/python/manejo_archivos/video_juegos/videojuego.csv", "r", newline="") as csv_video_juego:
        lector = csv.DictReader(csv_video_juego)
        return list(lector)


def input_clasificador_juegos():
    print("Ingrese el clasificador de juegos:\nE-Everyone| E10+ | T-Teen| M-Mature | AO-Adults Only | RP-Rating Pending")
    lista_clasificadores = ["E", "E10+", "T", "M", "AO", "RP", "EVERYONE", "E10+", "TEEN", "MATURE", "ADULTSONLY", "RATINGPENDING"]
    while True:
        clasificador_juegos = input("Ingrese el clasificador de juegos: ").strip().upper()
        if clasificador_juegos in lista_clasificadores:
            return clasificador_juegos
        else:
            print("Clasificador no válido. Por favor, ingrese un clasificador usando las opciones disponibles.\nE-Everyone| E10+ | T-Teen| M-Mature | AO-Adults Only | RP-Rating Pending")


def validar_break(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ["S","SI"]:
            return True
        elif respuesta in ["N","NO"]:
            return False
        else:
            print("Respuesta no válida")


def cantidad_videojuegos():
    videojuegos = read_CSV_file()
    cantidad_juegos = 0
    for juego in videojuegos:
        cantidad_juegos += 1
    print(f"Cantidad de videojuegos encontrados: {cantidad_juegos}")


def main():
        clasificador_usuario = input_clasificador_juegos()
        videojuegos = read_CSV_file()
        encontrados = False
        for juego in videojuegos:
            if juego["Clasificacion"] == clasificador_usuario:
                print(f"Se encontro: {juego['Nombre']}")
                encontrados = True
                cantidad_videojuegos()
        if not encontrados:
            print("No se encontraron videojuegos")
        if validar_break("Desea buscar otro clasificador? Si| No: ") == True:
            main()
        else:
            print("Gracias por usar el programa")


main()

