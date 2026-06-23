####################################################################
#Lea sobre el resto de métodos del módulo csv aqui y cree una version alternativa del ejercicio de arriba que guarde el archivo 
#separado por tabulaciones en vez de por comas.

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
    clasificacion = input("Ingrese la clasificacion del videojuego:")
    return {"Nombre": nombre,
        "Género": genero,
        "Desarrollador": desarrollador,
        "Clasificación ESRB": clasificacion}


cantidad_videojuegos = pedir_cantidad_videojuegos()
for x in range(cantidad_videojuegos):
    print(f"\nIngrese la información del videojuego {x + 1}:")
    videojuego = pedir_info_videojuego()
    videojuegos.append(videojuego) 


with open("videojuego_tabulado.csv", "w", newline="") as csvfile:
    fieldnames = ["Nombre", "Genero", "Desarrollador", "Clasificacion"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    for videojuego in videojuegos:
        writer.writerow({
            "Nombre": videojuego["Nombre"],
            "Genero": videojuego["Género"],
            "Desarrollador": videojuego["Desarrollador"],
            "Clasificacion": videojuego["Clasificación ESRB"]
        })
print("\nInformación de videojuegos guardada en videojuego.csv")








