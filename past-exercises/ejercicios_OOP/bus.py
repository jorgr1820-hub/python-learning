# Cree una clase de Bus con:
#  Un atributo de max_passengers.
#  Un método para agregar pasajeros uno por uno (que acepte como parámetro
#  una instancia de la clase Person vista en la lección).
#  Este solo debe agregar pasajeros si lleva menos de su máximo.
#  Sino, debe mostrar un mensaje de que el bus está lleno.
#  Un método para bajar pasajeros uno por uno (en cualquier orden).


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers = []

    def is_full(self):
        return len(self.passengers) >= self.max_passengers

    def add_passenger(self, person):
        """Sube un pasajero. Retorna True si subió, False si el bus está lleno."""
        if self.is_full():
            return False
        self.passengers.append(person)
        return True

    def remove_passenger(self, name):
        """Baja al pasajero con ese nombre. Retorna la Person que bajó, o None."""
        for index, person in enumerate(self.passengers):
            if person.name.lower() == name.lower():
                return self.passengers.pop(index)
        return None


# ---- Interfaz de usuario: aquí, y SOLO aquí, se usa print() e input() ----

def run_menu(bus):
    while True:
        print(f"\nBus: {len(bus.passengers)}/{bus.max_passengers} pasajeros")
        print("1) Subir pasajero   2) Bajar pasajero   3) Ver lista   4) Salir")
        option = input("> ").strip()

        if option == "1":
            name = input("Nombre del pasajero: ").strip()
            if not name:
                print("El nombre no puede estar vacío.")
            elif bus.add_passenger(Person(name)):
                print(f"{name} subió al bus.")
            else:
                print("El bus está lleno.")

        elif option == "2":
            name = input("Nombre del pasajero que baja: ").strip()
            person = bus.remove_passenger(name)
            if person:
                print(f"{person} bajó del bus.")
            else:
                print(f"{name} no está en el bus.")

        elif option == "3":
            if bus.passengers:
                for person in bus.passengers:
                    print(f" - {person}")
            else:
                print("El bus está vacío.")

        elif option == "4":
            print("Fin del recorrido.")
            break

        else:
            print("Opción inválida, elige 1, 2, 3 o 4.")


if __name__ == "__main__":
    run_menu(Bus(3))
