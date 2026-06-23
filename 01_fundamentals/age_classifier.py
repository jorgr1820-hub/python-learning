#Programa que pide nombre edad, y luego muestra un mensaje personalizado
#Clasificacion segun rangos de edad 
#Adulto mayor: 65 años o mas
#Adulto: 18 a 64 años
#Menores de edad: 13 a 17 años
#Niño: 0 a 12 años

def validar_edad():
    while True:
        try:
            edad = int(input("Ingrese su edad: "))
            if edad < 0:
                print("La edad no puede ser negativa. Por favor, ingrese una edad válida.")
            else:
                return edad
        except ValueError:
            print("Por favor, ingrese un número válido.")
#Validamos que la edad sea un numero valido y positivo.

def validar_nombre():
    while True:
        nombre = input("Ingrese su nombre:").strip()
        if nombre == "":
            print("El nombre no puede estar vacío. Por favor, ingrese un nombre válido.")
        else: 
            return nombre
#Validamos que el nombre no este vacio o solo contenga espacios en blanco.




def clasificador_edad(edad):
    if edad < 13:
        return "Niño"
    elif edad >= 13:
        return "Menor de edad"
    elif edad >= 18:
        return "Adulto"
    elif edad >= 65:
        return "Adulto mayor"
#Clasificamos la edad segun los rangos establecidos entre adulto mayor, adulto, menor de edad y niño.


def breakpoint():
    while True:
        opcion = input("¿Desea ingresar otra edad? (s/n): ").lower().upper()
        if opcion == 's' or opcion == 'S':
            edad()
        elif opcion == 'n' or opcion == 'N':
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, ingrese 's' para sí o 'n' para no.")
#Funcion que pregunta al usuario si desea ingresar otra edad, y dependiendo de la respuesta, llama a la funcion edad() nuevamente 
# o finaliza el programa.


def edad():
    edad = 0
    nombre = validar_nombre()
    edad = validar_edad()
    clasificacion = clasificador_edad(edad)
    print(f"Hola {nombre}, tu clasificación de edad es: {clasificacion}")
    breakpoint()
#Funcion principal que llama a las funciones de validacion y clasificacion, y muestra el mensaje personalizado 
# con el nombre y la clasificacion de edad.


edad()