"""Ejercicio 3 — Shape abstracta + Circle, Square y Rectangle.

Dominio: geometria.

LAS 5 PREGUNTAS
  1. ESTADO     Circle -> radius. Rectangle -> width, height. Square -> side.
                Y nada mas: una figura ES sus dimensiones.
  2. ACCIONES   calcular perimetro, calcular area. Ninguna CAMBIA nada.
  3. INVARIANTE (a) ninguna dimension es cero o negativa;
                (b) las dimensiones no cambian nunca despues de crear la figura.
  4. LIMITE     no imprime; los numeros son adimensionales (no sabe de cm ni m).
  5. MANANA     van a venir mas figuras. Lo que NO debe cambiar es el codigo
                que las usa.

LA DIFERENCIA:
Una figura es un objeto de VALOR INMUTABLE   -> una vez construida no hay
    nada que atacar, asi que casi todas las puertas estan en el constructor.

EL TIPO: aqui uso float; una medida
geometrica es una MEDICION aproximada y pi es irracional, asi que el valor
exacto no existe ni en teoria. El tipo correcto no es una preferencia: lo
dicta el dominio. La pregunta es "esto se cuenta o se mide?".
"""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Contrato: toda figura sabe calcular su perimetro y su area.

    Es ABC y no una clase normal para que olvidarse de implementar un metodo
    falle AL INSTANCIAR, no la primera vez que alguien lo llame en produccion.
    Esa es la unica razon de existir de una clase abstracta.
    """

    @abstractmethod
    def calculate_perimeter(self) -> float:
        """Largo del borde de la figura."""

    @abstractmethod
    def calculate_area(self) -> float:
        """Superficie encerrada por la figura."""

    # Una clase abstracta SI puede tener metodos concretos. Este se escribe una
    # vez y lo tienen las tres figuras, y las que se agreguen manana.
    # Es el mismo Template Method de withdraw(), pero al reves: alla el padre
    # definia la coreografia y PREGUNTABA un dato al hijo; aqui el padre define
    # la coreografia y LLAMA a los dos metodos que el hijo esta obligado a tener.
    def describe(self) -> str:
        return (
            f"{type(self).__name__:<10} "
            f"perimetro={self.calculate_perimeter():>8.2f}  "
            f"area={self.calculate_area():>8.2f}"
        )

    @staticmethod
    def _positive(value, name: str) -> float:
        """Invariante (a), comun a las tres figuras.

        Vive en el padre para escribirse una sola vez: el dia que quieras
        permitir el 0 (un punto, un segmento degenerado) se cambia aqui y no
        en tres lugares. @staticmethod porque es una regla sobre el dato.
        """
        value = float(value)          # tapa Circle("cinco") -> ValueError
        if value <= 0:
            raise ValueError(f"{name} debe ser positivo, llego {value}.")
        return value


class Circle(Shape):
    """Invariante: radius > 0."""

    def __init__(self, radius) -> None:
        self._radius = self._positive(radius, "radius")

    @property
    def radius(self) -> float:
        """Invariante (b): solo lectura.

        Las dimensiones SON la identidad de la figura. Un circulo al que le
        cambias el radio no es el mismo circulo con otro radio: es otro
        circulo. Y una figura inmutable se puede usar como clave de
        diccionario, guardar en un set y compartir entre dos listas sin miedo.
        """
        return self._radius

    def calculate_perimeter(self) -> float:
        return 2 * math.pi * self._radius

    def calculate_area(self) -> float:
        return math.pi * self._radius ** 2

    def __repr__(self) -> str:
        return f"Circle(radius={self._radius})"


class Rectangle(Shape):
    """Invariante: width > 0 y height > 0."""

    def __init__(self, width, height) -> None:
        self._width = self._positive(width, "width")
        self._height = self._positive(height, "height")

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def calculate_perimeter(self) -> float:
        return 2 * (self._width + self._height)

    def calculate_area(self) -> float:
        return self._width * self._height

    def __repr__(self) -> str:
        return f"Rectangle(width={self._width}, height={self._height})"


class Square(Shape):
    """Invariante: side > 0.

    POR QUE HEREDA DE Shape Y NO DE Rectangle
    -----------------------------------------
    Primero: porque el enunciado lo pide asi.

    Pero la razon de fondo vale mas que el ejercicio. "Un cuadrado ES UN
    rectangulo" es verdad en matematica, asi que la prueba ES-UN diria
    Square(Rectangle). Y es el ejemplo canonico de violacion del principio
    de sustitucion de Liskov. Mira por que:

        def hacer_mas_ancho(rect):      # funcion escrita para Rectangle
            rect.width = rect.width * 2 # valida para CUALQUIER rectangulo

        hacer_mas_ancho(Square(4))      # width=8, height=4 -> ya no es cuadrado

    El cuadrado heredaria una operacion que rompe su propia promesa.

    La prueba de Liskov, en una frase:
        "puedo pasarle el hijo a cualquier funcion escrita para el padre
         sin que nada se rompa?"
    Si la respuesta es no, no es herencia, por mas que "ES-UN" suene bien.

    EL MATIZ HONESTO: como estas figuras son inmutables (no hay setters que
    romper), Square(Rectangle) seria legitimo aqui. La inmutabilidad hace
    segura una herencia que de otro modo seria un bug. Se eligio Shape por
    el enunciado y porque no obliga al lector a razonar todo esto.
    """

    def __init__(self, side) -> None:
        self._side = self._positive(side, "side")

    @property
    def side(self) -> float:
        return self._side

    def calculate_perimeter(self) -> float:
        return 4 * self._side

    def calculate_area(self) -> float:
        return self._side ** 2

    def __repr__(self) -> str:
        return f"Square(side={self._side})"


# --------------------------------------------------------------------------
# Demostracion: una seccion por fila de la tabla de trazabilidad del README
# --------------------------------------------------------------------------

def _check(label: str, action) -> None:
    try:
        action()
        print(f"    [ABIERTA] {label}")
    except (TypeError, ValueError, AttributeError) as error:
        print(f"    [tapada ] {label:<40} {type(error).__name__}")


if __name__ == "__main__":
    print("=== Filas 10 y 11: las tres figuras, un solo bucle, cero ifs ===")
    shapes: list[Shape] = [Circle(5), Square(4), Rectangle(3, 7)]
    for shape in shapes:
        print("   ", shape.describe())
    print("    valores esperados: Circle(5)=31.42/78.54  Square(4)=16/16"
          "  Rectangle(3,7)=20/21")
    print(f"    isinstance de las tres -> "
          f"{[isinstance(s, Shape) for s in shapes]}")

    print("\n=== Filas 8 y 9: por que es abstracta ===")
    try:
        Shape()
    except TypeError as error:
        print(f"    Shape() -> TypeError:\n      {error}")

    class Triangle(Shape):
        """A proposito incompleta: implementa uno de los dos metodos."""

        def __init__(self, a, b, c):
            self.a, self.b, self.c = a, b, c

        def calculate_perimeter(self):
            return self.a + self.b + self.c

    try:
        Triangle(3, 4, 5)
    except TypeError as error:
        print(f"    Triangle(3,4,5) -> TypeError:\n      {error}")
    print("    el mensaje NOMBRA el metodo que falta: por eso la fila 9 se")
    print("    verifica con el mismo error que la fila 8.")

    print("\n=== Las puertas del invariante ===")
    _check("1. Circle(0)", lambda: Circle(0))
    _check("2. Circle(-3)", lambda: Circle(-3))
    _check("3. circulo.radius = 10", lambda: setattr(Circle(5), "radius", 10))
    _check("4. Shape() directo", lambda: Shape())
    _check("5. hija con un solo metodo", lambda: Triangle(3, 4, 5))
    _check("6. Rectangle(3) sin altura", lambda: Rectangle(3))
    _check("7. Circle('cinco')", lambda: Circle("cinco"))

    print("\n=== El pago del diseno ===")
    print(f"    area total = {sum(s.calculate_area() for s in shapes):.2f}")
    print("    esa linea no sabe que existen circulos. Agregar un Triangle")
    print("    completo no la toca: eso es el valor real del polimorfismo.")
