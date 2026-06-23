#Cree un programa que me permita ingresar información de n cantidad de videojuegos y los guarde en un archivo csv.
#Debe incluir:
#Nombre
#Género
#Desarrollador
#  Clasificación ESRB





from ast import While
import csv

videojuegos = []

def pedir_cantidad_videojuegos():
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad de videojuegos que desea agregar: "))
            if cantidad > 0:
                return cantidad
            else:
                print("Ingrese un número mayor a 0.")
        except ValueError:
            print("Por favor, ingrese un número válido.")


def pedir_info_videojuego():
    nombre = input("Ingrese el nombre del videojuego:")
    genero = input("Ingrese el género del videojuego:")
    desarrollador = input("Ingrese el desarrollador del videojuego:")
    clasificacion = input("Ingrese la clasificacion del videojuego\nE-Everyone| E10+ | T-Teen| M-Mature | AO-Adults Only | RP-Rating Pending:").upper().strip()
    return {"Nombre": nombre,
        "Género": genero,
        "Desarrollador": desarrollador,
        "Clasificación": clasificacion}


def crear_csv():
    with open("/Users/jordan.guzman/python/manejo_archivos/video_juegos/videojuego.csv", "w", newline="") as csvfile:
        fieldnames = ["Nombre", "Genero", "Desarrollador", "Clasificacion"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for videojuego in videojuegos:
            writer.writerow({
                "Nombre": videojuego["Nombre"],
                "Genero": videojuego["Género"],
                "Desarrollador": videojuego["Desarrollador"],
                "Clasificacion": videojuego["Clasificación"]
            })
    print("\nInformación de videojuegos guardada en videojuego.csv")


def main():
    cantidad_videojuegos = pedir_cantidad_videojuegos()
    for x in range(cantidad_videojuegos):
        print(f"\nIngrese la información del videojuego {x + 1}:")
        videojuego = pedir_info_videojuego()
        videojuegos.append(videojuego) 
    crear_csv()

main()



