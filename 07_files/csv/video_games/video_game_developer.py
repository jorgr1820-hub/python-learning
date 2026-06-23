import csv


def read_CSV_file():
    with open("/Users/jordan.guzman/python/manejo_archivos/video_juegos/videojuego.csv", "r", newline="") as csv_video_juego:
        lector = csv.DictReader(csv_video_juego)
        return list(lector)


def validar_break(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ["S", "SI"]:
            return True
        elif respuesta in ["N", "NO"]:
            return False
        else:
            print("Respuesta no válida")


def buscar_por_desarrollador():
    videojuegos = read_CSV_file()
    desarrollador_usuario = input(
        "Ingrese el nombre del desarrollador: ").strip().upper()
    encontrados = []
    for juego in videojuegos:
        if juego["Desarrollador"].strip().upper() == desarrollador_usuario:
            encontrados.append(juego)
    if len(encontrados) > 0:
        print(f"\nVideojuegos desarrollados por {desarrollador_usuario}:")
        for juego in encontrados:
            print(
                f"- {juego['Nombre']} "
                f"(Clasificación: {juego['Clasificacion']}, "
                f"Género: {juego['Genero']})" )
    else:
        print("No se encontraron videojuegos para ese desarrollador.")


def main():
    while True:
        buscar_por_desarrollador()
        if not validar_break(
            "\n¿Desea buscar otro desarrollador? Si|No: "):
            print("Gracias por usar el programa.")
            break


main()