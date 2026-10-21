# Practica OOP — 2026-10-04

## 0. Ficha rapida

| | |
|---|---|
| **Fecha** | 2026-10-04 |
| **Tema** | Programacion Orientada a Objetos en Python: composicion, referencias, fachada, properties, fabrica, recursion y serializacion CSV |
| **Archivos tocados** | `past-exercises/ejercicios_OOP/human.py`, `circle.py`, `bus.py`, `student_control_2/student_control/{model,data,actions,main,menu}.py` + `README.md` |
| **Estado** | Los 4 ejercicios de la tarea completos y verificados corriendo |
| **Rama / PR** | `ejercicios-oop` -> PR #3 en `jorgr1820-hub/python-learning` |
| **Conceptos nuevos** | composicion, referencia vs copia, fachada, `@property`, funcion fabrica, scope, recursion, polimorfismo, `@classmethod`, serializacion, atributo de clase |
| **Pendientes** | `count_parts()` en `human.py`; Paso 8 (herencia con `BodyPart`) y Paso 9 (export a JSON) |

---

## 1. La analogia maestra

**Todo lo de esta sesion es una empresa con su organigrama y su archivo de expedientes.**

Una empresa no es una bolsa de empleados sueltos. Tiene jerarquia, recepcion,
departamento de personal y un archivo fisico. Cada pieza del codigo que
escribimos tiene su equivalente ahi:

- **El organigrama.** El CEO no tiene 30 reportes directos: tiene uno. Cada
  gerente sabe quienes son *sus* subordinados. Nadie tiene dos jefes — si
  tuvieras dos, no sabrias a quien pedirle vacaciones. Eso es **composicion**,
  y la regla de "un solo dueno".

- **Asignar no es clonar.** Cuando asignas un empleado a un gerente, no
  fabricas una copia de la persona. Es el mismo humano. Si dos gerentes creen
  tenerlo en exclusiva, el lunes hay conflicto. Eso es una **referencia
  compartida**.

- **Contratar de abajo hacia arriba.** No puedes nombrar a un gerente de un
  equipo que no existe. Primero los empleados, luego el gerente. Eso es el
  **orden de construccion**, y revela las dependencias del sistema.

- **La recepcion.** No recorres pasillos buscando el laboratorio del sotano:
  le preguntas a recepcion y ella conoce el camino. Si el laboratorio se muda
  de piso, **recepcion se actualiza y tu no cambias nada**. Eso es la
  **fachada**.

- **La recepcionista no te dice si lo sabia o lo fue a buscar.** Le pides un
  dato y te lo da. No te enteras si estaba en su escritorio o si llamo a otro
  piso. Eso es `@property`: leer algo como si fuera un dato guardado, aunque
  por detras sea un recorrido.

- **Recursos Humanos arma equipos completos.** Pides "un equipo nuevo" y te
  llega ensamblado. No armas tu el equipo pieza por pieza cada vez, ni
  necesitas conocer el orden de contratacion. Esa es la **funcion fabrica**.

- **El conteo baja por el organigrama.** El CEO quiere saber cuantos empleados
  hay. No los cuenta: le pide a cada gerente "cuentame los tuyos". Cada gerente
  hace lo mismo hacia abajo. Quien no tiene gente reporta 1 y ahi se detiene.
  Esa es la **recursion**, y su caso base.

- **Todos responden la misma pregunta a su manera.** El CEO pregunta "¿quienes
  son tus subordinados?" y no le importa si habla con un gerente de ventas o
  de produccion: cada uno responde lo suyo. Eso es **polimorfismo**.

- **El expediente en papel.** La persona no entra al archivador: entran sus
  datos en una ficha. Y cuando la recontratas, reconstruyes al empleado leyendo
  la ficha. El empleado de ayer y el de hoy son dos personas distintas con los
  mismos datos. Eso es **serializacion**: un objeto no se guarda, se guardan
  sus atributos.

- **La ficha en blanco es igual para todos.** El formato del expediente
  (que casillas tiene y en que orden) es uno solo para la empresa entera, no
  uno por empleado. Eso es un **atributo de clase**.

- **Cada departamento hace lo suyo.** Recepcion habla con la gente, las
  gerencias aplican las reglas, el expediente define que es un empleado y el
  archivo fisico guarda papel. Si cambias de archivadores a un escaner, solo
  cambia el archivo. Esa es la **separacion de capas**.

### Traduccion analogia -> termino tecnico

| En la empresa | En el codigo | Nombre tecnico |
|---|---|---|
| Organigrama, un jefe por empleado | `self.hand = hand` | Composicion |
| Asignar no clona a la persona | `a is b` -> `True` | Referencia compartida |
| Contratar de abajo hacia arriba | `Arm("x", Hand("y"))` | Orden de dependencias |
| Recepcion conoce el camino | `jordan.left_foot` | Fachada |
| No sabes si lo sabia o lo busco | `@property` | Atributo calculado |
| RRHH arma el equipo | `build_human(name)` | Funcion fabrica |
| "Cuentame los tuyos" | `show_body(child, level + 1)` | Recursion |
| Mismo pregunta, cada uno responde lo suyo | `part.children()` | Polimorfismo |
| El expediente en papel | `to_dict()` / `from_dict()` | Serializacion |
| El formato de ficha de la empresa | `Student.FIELDS` | Atributo de clase |
| Departamentos separados | `menu / actions / model / data` | Separacion de capas |

---

## 2. El mapa

### El arbol de objetos (ejercicio Human)

```
Human ("Jordan")                <- la raiz, el punto de entrada
 └── Torso
      ├── Head                  <- caso base: children() == []
      ├── Arm  (left)  ──► Hand (left)    <- caso base
      ├── Arm  (right) ──► Hand (right)
      ├── Leg  (left)  ──► Foot (left)
      └── Leg  (right) ──► Foot (right)

Flecha hacia abajo = self.hand = hand   (el padre es dueno)
Una sola direccion. Nadie tiene dos duenos. No hay ciclos.
11 objetos en total.
```

### Las capas (ejercicio Student Control)

```
menu.py      UI             habla con el humano: input() y print()
   │
actions.py   Logica         reglas: validar, promediar, filtrar, ordenar
   │
model.py     Modelo         que ES un Student + to_dict() / from_dict()
   │
data.py      Persistencia   archivos, csv, OSError
   │
students.csv Disco          texto plano
```

La prueba de que las capas estan bien separadas: **se puede cambiar una sin
tocar las otras**. Cambiar CSV por SQLite = reescribir `data.py` completo;
`menu.py`, `actions.py` y `model.py` no se enteran.

### La frontera de tipos

```
  AFUERA (disco)          FRONTERA              ADENTRO (programa)
  ───────────────         ─────────             ──────────────────
  "85"  texto     ──► Student.from_dict() ──►   85   int
                                                 │
  "85"  texto     ◄── Student.to_dict()  ◄──    85   int
```

Regla: **la conversion de tipos ocurre en el borde.** Hacia adentro siempre
hay objetos con tipos correctos.

---

## 3. Conceptos

### 3.1 Composicion — un atributo puede ser otro objeto

**Que es:** guardar un objeto completo dentro de otro objeto, como atributo.

**Por que existe:** las cosas reales no son planas. Un brazo no es un dato: un
brazo *tiene* una mano, y esa mano tiene sus propios datos. Sin composicion
terminas con una sola clase gigante:

```python
class Arm:
    def __init__(self):
        self.hand_finger_count = 5
        self.hand_is_open = True
        self.hand_color = "..."     # y asi hasta el infinito
```

El problema que resuelve: **cada clase se encarga de lo suyo.** La mano sabe de
manos; el brazo solo sabe *cual* mano tiene.

**Analogia:** el organigrama. Un gerente no contiene a sus empleados dentro de
si: los tiene asignados.

**Codigo:**

```python
class Hand:
    def __init__(self, name):
        self.name = name


class Arm:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand        # <- aqui esta la composicion


right_hand = Hand("right_hand")
right_arm = Arm("right_arm", right_hand)

print(right_arm.hand.name)      # right_hand
```

**Que ocurre al ejecutar:** `right_arm.hand.name` se lee de izquierda a
derecha, como bajar escalones: Python va al objeto `Arm`, entra a su atributo
`hand`, llega al objeto `Hand`, y lee su atributo `name`. Cada punto es un
salto a otra direccion de memoria.

**Como verificar:** `python3 human.py` debe imprimir `right_arm` y
`right_hand`.

**Que problema futuro evita:** la clase-monstruo de 50 atributos que nadie
puede modificar sin romper algo.

**Donde se reusa:** es la relacion mas comun de todo el software.
`Account -> Contact -> Deal -> Activity` en un CRM, `Order -> OrderLine` en
e-commerce, `Component -> Children` en React. Composicion ("tiene-un") es lo
contrario de herencia ("es-un"): un brazo *tiene* una mano, un brazo no *es*
una mano.

---

### 3.2 Referencia vs copia — la variable es un control remoto

**Que es:** una variable no contiene el objeto. Contiene la direccion de
memoria donde el objeto vive.

**Por que existe:** copiar objetos enteros en cada asignacion seria lentisimo y
haria imposible que dos partes del programa vean el mismo dato actualizado.

**Analogia:** la variable es el control remoto, no el televisor. Dos controles
pueden apuntar al mismo televisor.

**Codigo:**

```python
right_hand = Hand("right_hand")
right_arm = Arm("right_arm", right_hand)

right_hand.name = "broken_hand"

print(right_hand.name)          # broken_hand
print(right_arm.hand.name)      # broken_hand   <- la MISMA mano
print(right_hand is right_arm.hand)             # True
print(id(right_hand), id(right_arm.hand))       # dos numeros identicos
```

**Que ocurre al ejecutar:** al pasar `right_hand` al constructor, Python **no
copio** la mano: paso su direccion. Quedo asi:

```
   right_hand  ──────┐
                     ▼
              ┌──────────────┐
              │  objeto Hand │   <- UN solo objeto
              └──────────────┘
                     ▲
right_arm.hand ──────┘
```

**Como verificar:** `is` pregunta "¿son el mismo objeto?" (`True`). `id()` da
la direccion; los dos numeros deben ser identicos. Ese numero cambia en cada
ejecucion — lo unico que importa es que coincidan entre si.

Diferencia clave: **`==` compara contenido, `is` compara identidad.** Dos manos
distintas con el mismo nombre serian `==` pero nunca `is`.

**Que problema futuro evita:** el bug silencioso de compartir un objeto sin
querer:

```python
left_arm = Arm("left_arm", right_hand)    # ❌ un humano con una sola mano
                                          #    conectada a dos brazos
left_arm = Arm("left_arm", Hand("left_hand"))   # ✅ mano nueva, exclusiva
```

Compila, corre, no da error — y aparece en tres semanas cuando ya no recuerdas
esa linea. De ahi la regla: **un solo dueno por objeto.**

**Donde se reusa:** es la causa numero 1 de bugs raros en Python.
Una lista pasada a una funcion y modificada adentro cambia la original. Dos
clientes apuntando al mismo objeto `Address`. El clasico `def f(items=[])`,
donde la lista se crea **una vez** y se comparte entre todas las llamadas.
Todos son el mismo concepto: **asignar no copia, comparte.**

---

### 3.3 Orden de construccion — de abajo hacia arriba

**Que es:** las piezas que no dependen de nada se crean primero; las que
dependen de otras, despues.

**Por que existe:** no puedes pasar como argumento algo que todavia no existe.
`Arm("right_arm", right_hand)` sin `right_hand` definida da
`NameError: name 'right_hand' is not defined`.

**Analogia:** no puedes nombrar al gerente de un equipo que no has contratado.

**Codigo:**

```python
head = Head("head")                                  # sin dependencias
left_arm = Arm("left_arm", Hand("left_hand"))        # necesita una mano
torso = Torso("torso", head, left_arm, ...)          # necesita todo lo anterior
```

**Que ocurre al ejecutar:** se construye de la punta hacia el centro: mano ->
brazo -> torso -> humano.

**Como verificar:** si no sabes que crear primero, el diseno esta mal: tienes
una dependencia circular.

**Que problema futuro evita:** dependencias circulares, que son imposibles de
construir e imposibles de serializar.

**Donde se reusa:** el orden de construccion **revela las dependencias del
sistema**. Es la misma logica de `docker compose depends_on`, de las
migraciones de base de datos y de la inyeccion de dependencias en backend.

---

### 3.4 Fachada — una entrada simple a una estructura compleja

**Que es:** una clase que ofrece acceso directo a partes profundas, ocultando
el camino.

**Por que existe:** `torso.left_leg.foot.name` contiene una **suposicion sobre
la estructura interna**. Si manana agregas el tobillo:

```python
torso.left_leg.ankle.foot.name
```

...y tu app tiene 40 lugares que leen pies, son 40 correcciones, y basta
olvidar una para tener un `AttributeError` en produccion. Eso es
**acoplamiento**: el codigo de afuera depende de detalles que no le incumben.

**Analogia:** la recepcion del hospital. Si el laboratorio se muda de piso,
recepcion se actualiza y tu no cambias nada.

**Codigo:**

```python
class Human:
    """Punto de entrada al cuerpo. Conoce el camino hasta cada parte."""

    def __init__(self, name, torso):
        self.name = name
        self.torso = torso       # UN solo reporte directo

    @property
    def left_foot(self):
        return self.torso.left_leg.foot
```

Lo que **no** se debe hacer:

```python
class Human:
    def __init__(self, name, torso, head, left_arm):   # ❌ duplica la verdad
```

El torso ya tiene la cabeza. Con dos copias, una queda desactualizada y no
sabes cual creer. Regla: **un dato vive en un solo lugar.**

**Que ocurre al ejecutar:** el metodo no crea nada — devuelve la referencia al
objeto que ya existe. Devuelve el control remoto, no un televisor nuevo.

**Como verificar:** `jordan.left_foot.name` imprime `left_foot` sin que el
codigo de afuera mencione `torso` ni `left_leg`.

**Que problema futuro evita:** agregar `Ankle` pasa de 40 cambios a **1**:

```python
def left_foot(self):
    return self.torso.left_leg.ankle.foot   # unica linea que sabe la verdad
```

**Donde se reusa:** `account.get_open_deals()` en el CRM. El endpoint de una
API es la fachada de la base de datos. **Ley de Demeter** ("no hables con
extranos"): si ves tres puntos seguidos en una linea (`a.b.c.d`), es senal de
acoplamiento — en ingles le dicen *train wreck*.

El principio de fondo: **el codigo de afuera depende de lo que prometes (la
interfaz), no de como lo cumples (la implementacion).**

---

### 3.5 `@property` — el metodo disfrazado de atributo

**Que es:** un decorador que hace que un metodo se lea sin parentesis, como si
fuera un atributo guardado.

**Por que existe:** sin el, tu interfaz es incoherente:

```python
print(jordan.name)              # sin parentesis (dato guardado)
print(jordan.get_head().name)   # con parentesis (hay que ir a buscarlo)
```

Desde afuera ambas son lo mismo: "dame una caracteristica de este humano". La
diferencia de sintaxis solo revela un detalle de implementacion que no deberia
importarle a quien usa la clase.

**Analogia:** el tablero del carro. La gasolina es una medicion directa; los
kilometros restantes son un calculo. Los dos se leen igual: mirando el tablero.

**Codigo:**

```python
    @property
    def left_hand(self):
        return self.torso.left_arm.hand
```

```python
print(jordan.left_hand.name)    # sin parentesis
```

Nota de nombres: se le quita el `get_`. **Convencion de Python: atributos y
properties son sustantivos (`head`, `total`, `is_full`); los metodos con
parentesis son verbos (`add_passenger()`, `take_damage()`).**

**Que ocurre al ejecutar** — esto es lo que evita que parezca magia. Al escribir
`jordan.head`:

1. ¿Existe `head` en el diccionario de instancia (`jordan.__dict__`)? No.
2. ¿Existe en la clase `Human`? Si, y no es una funcion normal: es un objeto
   `property`.
3. Un `property` define un comportamiento especial al ser leido, asi que Python
   **llama** a la funcion que envuelve con `self = jordan`, y devuelve el
   resultado.

Consecuencia practica: **se ejecuta en cada lectura.** Si una property hiciera
una consulta a base de datos y la leyeras en un ciclo de 1000 vueltas, son 1000
consultas. Regla: **una property debe ser barata.** Si el calculo es costoso,
usa un metodo con parentesis — los parentesis avisan "esto hace trabajo".

**Como verificar:** que imprima igual que con `get_*()`, y que esto falle:

```python
jordan.head = Head("other_head")
# AttributeError: property 'head' of 'Human' object has no setter
```

Definiste como se **lee**, nunca como se **escribe**. Eso es deseable: la
cabeza le pertenece al torso, nadie deberia cambiarla por la puerta de atras.
Existe `@head.setter`, pero no se agrega hasta que un requisito real lo pida.

**Que problema futuro evita:** poder convertir un atributo guardado en un valor
calculado (o al revés) **sin que una sola linea del codigo que te usa cambie**.

**Donde se reusa:** `deal.total` calculado desde sus lineas, en vez de un campo
guardado que se desincroniza. `dataset.row_count` que cuenta al momento y nunca
miente. En React es el mismo principio con otro nombre: *derived state* — no
guardas lo que puedes calcular, porque dos copias de la verdad siempre terminan
peleando.

---

### 3.6 Funcion fabrica y scope — donde viven las variables

**Que es:** una funcion cuyo unico trabajo es armar un objeto complejo y
devolverlo listo.

**Por que existe:** las lineas de construccion sueltas tienen tres defectos:

1. **Se repiten.** Segundo humano -> copias 7 lineas y cambias nombres a mano.
2. **Dejan variables sueltas en el nivel global.** `head`, `left_arm`, `torso`
   siguen existiendo despues de armar a Jordan, y cualquiera puede tomarlas:
   el bug de la referencia compartida esperando.
3. **Obligan a saber el orden.** Ese conocimiento no deberia salir de la clase.

**Analogia:** no armas un carro en tu garaje cada vez. Vas a la planta, pides
"un Corolla azul", y sale ensamblado.

**Codigo:**

```python
def build_human(name):
    """Arma un cuerpo completo y devuelve el Human listo para usar."""
    torso = Torso(
        "torso",
        Head("head"),
        Arm("left_arm", Hand("left_hand")),
        Arm("right_arm", Hand("right_hand")),
        Leg("left_leg", Foot("left_foot")),
        Leg("right_leg", Foot("right_foot")),
    )
    return Human(name, torso)


if __name__ == "__main__":
    jordan = build_human("Jordan")
```

Detalle de forma: la **coma final** despues del ultimo argumento es legal en
Python y deseable — si manana agregas un parametro, el diff de Git muestra una
linea agregada en vez de dos modificadas.

**Que ocurre al ejecutar — aqui esta el concepto de memoria:**

1. Python abre un **scope local**: un espacio de nombres propio de la funcion.
2. Se crean 11 objetos en memoria.
3. `torso` es una variable **local**: existe solo dentro de la funcion.
4. `return Human(name, torso)` crea el `Human`, que guarda una referencia al
   torso.
5. La funcion termina. **La variable `torso` deja de existir.** Pero el objeto
   torso NO se borra: sigue vivo porque el `Human` lo referencia.

La regla que gobierna esto: Python borra un objeto cuando **nadie lo
referencia** (*reference counting*). Mientras alguien tenga un control remoto
apuntando al televisor, el televisor no se tira.

Resultado neto: `head`, `left_arm` y `torso` ya no existen como variables
globales. Eliminaste el defecto #2 sin escribir codigo defensivo — solo
cambiando **donde viven** las variables.

**`if __name__ == "__main__":`** es la linea que separa **definir** de
**ejecutar**. Al correr `python3 human.py`, Python pone `__name__ = "__main__"`
y el bloque se ejecuta. Al hacer `import human` desde otro archivo, `__name__`
vale `"human"` y el bloque **no** corre. Sin esa guarda, un
`from human import Human` ejecutaria tus prints.

**Como verificar** — la prueba que junta todo:

```python
jordan = build_human("Jordan")
ana = build_human("Ana")

print(jordan.left_hand is ana.left_hand)              # False
print(jordan.left_hand.name, ana.left_hand.name)      # left_hand left_hand
```

Los nombres son **iguales** (`==` seria `True`) pero los objetos son
**distintos** (`is` da `False`). Cada llamada fabrica su propio juego de 11
objetos. Si le rompes la mano a Ana, Jordan no siente nada.

**Que problema futuro evita:** 7 lineas repetidas en cada test, en cada
pantalla, en cada script.

**Donde se reusa:** `build_account(data)` armando cuenta + contactos + deals
desde un JSON. `Student.from_dict(row)` leyendo un CSV. En tests,
`build_human("test")` te da un objeto valido en una linea. En otros stacks le
dicen *factory*, *builder*, *seed*, *fixture* o *dependency injection*: cinco
nombres para "alguien mas se encarga de ensamblar".

El principio: **separa construir de usar.** Una clase define *que es* una cosa;
la fabrica sabe *como se ensambla*.

---

### 3.7 Recursion y polimorfismo — recorrer sin conocer la estructura

**Que es:** recursion es una funcion que se llama a si misma para resolver una
version mas pequena del mismo problema. Polimorfismo es que objetos distintos
respondan al mismo mensaje, cada uno a su manera.

**Por que existe:** imprimir el cuerpo entero a mano son 11 lineas que dependen
de la anatomia exacta:

```python
print(jordan.torso.left_arm.hand.name)    # ... y 10 mas
```

Agregar `Neck` obliga a editar esa lista. Agregar 5 dedos por mano son 10
lineas mas, a mano. Y si lees un cuerpo desde un JSON sin saber cuantas partes
trae, la tecnica no existe. El problema de fondo: **estas escribiendo el camino
a mano cuando la estructura ya sabe su propio camino.**

**Analogia:** el CEO no cuenta empleados. Le dice a cada gerente "cuentame los
tuyos y reporta". Quien no tiene gente reporta 1 y ahi se detiene.

**Codigo** — primero cada clase responde una sola pregunta:

```python
class Hand:
    def children(self):
        return []                   # caso base


class Arm:
    def children(self):
        return [self.hand]          # caso recursivo


class Torso:
    def children(self):
        return [
            self.head,
            self.left_arm,
            self.right_arm,
            self.left_leg,
            self.right_leg,
        ]
```

Y la funcion que recorre, **fuera** de las clases:

```python
def show_body(part, level=0):
    """Imprime la parte y todas sus descendientes, indentadas por nivel."""
    print("  " * level + part.name)

    for child in part.children():
        show_body(child, level + 1)
```

Lo que `show_body` **no** hace, y es la decision completa:

```python
if isinstance(part, Arm):        # ❌ nunca se escribio esto
    recorrer part.hand
elif isinstance(part, Leg):
    recorrer part.foot
```

Si preguntara "¿de que tipo eres?", `show_body` tendria que conocer las 7
clases, y cada clase nueva le agregaria un `elif`. En vez de eso **hace una
pregunta y confia en la respuesta**: `part.children()`. No sabe ni le importa
si mira un brazo o un pie. **El nombre compartido del metodo es lo que hace
posible el polimorfismo.**

**Que ocurre al ejecutar:**

```
show_body(jordan, 0)      imprime "Jordan"           children() → [torso]
  show_body(torso, 1)     imprime "  torso"          children() → 5 partes
    show_body(head, 2)    imprime "    head"         children() → []  ← SE DETIENE
    show_body(l_arm, 2)   imprime "    left_arm"     children() → [l_hand]
      show_body(l_hand,3) imprime "      left_hand"  children() → []  ← SE DETIENE
```

Dos cosas que hacen que funcione:

- **El caso base no es un `if`.** El `for` simplemente no da ninguna vuelta
  cuando la lista esta vacia, y la funcion termina sola. Las recursiones mas
  limpias tienen el caso base implicito en la estructura de datos.
- **`level` es la profundidad.** `"  " * level` convierte ese numero en
  sangria: el dibujo del arbol es un efecto secundario gratis.

Detalle de memoria: cada llamada pendiente ocupa un espacio en la *pila de
llamadas* (*call stack*). Con 11 partes la pila llega a 4 niveles. Python corta
a los ~1000 — suficiente para cualquier arbol razonable, insuficiente para
recorrer una lista de un millon de elementos. **La recursion es para
estructuras jerarquicas, no para recorridos lineales largos.**

**Como verificar:** `python3 human.py` imprime 11 lineas dibujando el cuerpo
por sangria:

```
Jordan
  torso
    head
    left_arm
      left_hand
    right_arm
      right_hand
    left_leg
      left_foot
    right_leg
      right_foot
```

Ese dibujo no esta escrito en ninguna parte: salio de la estructura.

**Que problema futuro evita:** agrega dedos a `Hand` y haz que su `children()`
los devuelva. `show_body` imprime los 10 dedos **sin tocar una sola linea de
`show_body`**. Nombre del principio: **abierto a extension, cerrado a
modificacion.** El codigo que no se toca no se rompe.

**Donde se reusa:** arbol de carpetas (contar archivos, sumar tamanos). JSON
anidado de profundidad desconocida — lo vas a necesitar si o si. En el CRM:
`account.children()` -> contactos -> deals -> actividades, con un solo
`show_tree()` para exportar, contar o buscar. En React el DOM es un arbol y el
render es recursivo. En SQL, categorias con `parent_id` y `WITH RECURSIVE`.

---
### 3.8 Que es OOP — la cadena clase / instancia / objeto / referencia

**Que es:** OOP = *Object-Oriented Programming*, en espanol POO. No es un
objeto ni un archivo: es un **paradigma**, una forma de organizar el codigo.

**Por que existe:** antes se programaba con datos por un lado y funciones por
otro. El `student_control` original era exactamente eso:

```python
student = {"name": "John", "spanish": 85}   # los datos
calculate_average(student)                  # la funcion, en otra parte
```

Funciona con 3 funciones. Con 30 se cae por tres razones concretas:

1. **Nada garantiza la forma del dato.** `student["nombre"]` en vez de
   `student["name"]` no da error al escribirlo: explota en ejecucion, quiza
   meses despues. Un diccionario acepta cualquier llave.
2. **El dato no sabe nada de si mismo.** El diccionario no sabe calcular su
   promedio; tienes que acordarte de que existe una funcion suelta que lo hace.
3. **Un cambio se propaga a todas partes.** Renombras `spanish` y tienes que
   cazar los 20 lugares donde se uso esa llave.

OOP responde con una idea sola: **guarda juntos los datos y el comportamiento
que les pertenece.** Y `student.nombre` **si** falla de inmediato con
`AttributeError`, porque un objeto tiene atributos definidos, no llaves
arbitrarias.

**Analogia:** el molde de galletas. La **clase** es el molde: define la forma,
no te la puedes comer. El **objeto** es cada galleta: existe, ocupa espacio, es
distinta de las demas. La **variable** es la etiqueta con la que senalas una
galleta especifica. Un molde, mil galletas.

**Codigo — la cadena completa:**

```python
class Student:                    # 1. CLASE: el molde
    def __init__(self, name):     # 2. CONSTRUCTOR: corre al fabricar cada objeto
        self.name = name          # 3. ATRIBUTO: dato propio de ESE objeto

ana = Student("Ana")              # 4. INSTANCIACION: nace un OBJETO en memoria
#                                 # 5. ana = REFERENCIA a su direccion
```

**Que ocurre al ejecutar — lo que casi nadie explica:**

- La clase `Student` vive **una sola vez** en memoria. Ahi viven los **metodos**.
- Cada objeto vive en su propia direccion y guarda **solo sus atributos**.
- Por eso 500 estudiantes no ocupan 500 copias de `average()`: ocupan 500
  juegos de datos + un juego de metodos compartido.
- `ana` no contiene el objeto: contiene su direccion.

**Los 4 pilares, con la verdad de cuanto importa cada uno:**

| Pilar | Que es | Donde se uso en esta tarea |
|---|---|---|
| **Encapsulacion** | datos + comportamiento en la misma caja | `Student` guarda notas y sabe traducirse |
| **Abstraccion** | usar algo sin conocer su interior | `jordan.left_foot` sin saber la cadena interna |
| **Herencia** | una clase reutiliza otra | no se uso (pendiente, Paso 8) |
| **Polimorfismo** | mismo mensaje, cada clase responde a su manera | `children()` en `show_body` |

Encapsulacion y abstraccion son el 90% del valor de OOP y se usan todos los
dias. **Herencia es la que mas se abusa**: los principiantes crean jerarquias
de 5 niveles que nadie entiende. Se usa solo cuando dos clases comparten codigo
real.

**El criterio que de verdad sirve** — no es "OOP es mejor", es saber cuando:

| Usa un diccionario cuando... | Usa una clase cuando... |
|---|---|
| es data de paso (fila de CSV, JSON de API) | la cosa tiene identidad propia y vida larga |
| las llaves varian o no las conoces | los campos son fijos y conocidos |
| solo la lees y la mandas a otro lado | tiene comportamiento propio (validar, calcular) |

Y no hay que elegir uno: hay que **traducir en la frontera**.

---

### 3.9 Serializacion — `to_dict()`, `from_dict()` y `@classmethod`

**Que es:** convertir un objeto en una estructura plana que se puede guardar, y
reconstruirlo al leerla.

**Por que existe:** un CSV no sabe de objetos. Y un objeto no cabe en un
archivo de texto. Hay que traducir en los dos sentidos. Sin esto, dos opciones
del menu crasheaban:

```
TypeError: 'Student' object is not subscriptable
AttributeError: 'Student' object has no attribute 'keys'
```

**Analogia:** el expediente en papel. La persona no entra al archivador: entran
sus datos en una ficha. Al recontratarla, reconstruyes al empleado leyendo la
ficha. El de ayer y el de hoy son dos personas distintas con los mismos datos.

**La decision central — ¿donde vive la conversion?**

| Opcion | Consecuencia |
|---|---|
| En `data.py` (la capa CSV) | `data.py` tiene que conocer los 6 campos. Agregas "matematicas" -> editas `model.py` **y** `data.py`. Si manana exportas a JSON, ese archivo tambien. |
| **En `Student` (la clase)** ✅ | La clase conoce su propia forma. `data.py` solo sabe "pidele a cada objeto su diccionario". Agregas un campo -> editas **un** archivo. |

El criterio: **la informacion vive junto a quien la posee.**

**Codigo:**

```python
    def to_dict(self) -> dict:
        """Return the student as a plain dict, ready for csv.DictWriter."""
        return {
            "name": self.name,
            "section": self.section,
            "spanish": self.spanish,
            "english": self.english,
            "social_studies": self.social_studies,
            "science": self.science,
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Student":
        """Build a Student from a CSV row."""
        return cls(
            name=row["name"],
            section=row["section"],
            spanish=int(row["spanish"]),
            english=int(row["english"]),
            social_studies=int(row["social_studies"]),
            science=int(row["science"]),
        )
```

Y `data.py` se vuelve tonto, que es lo deseable:

```python
            for student in student_list:
                writer.writerow(student.to_dict())
```

```python
            for row in reader:
                students.append(Student.from_dict(row))
```

**`self` vs `cls` — la diferencia que importa:**

| | `self` | `cls` |
|---|---|---|
| Que recibe | el objeto concreto | la clase |
| Cuando | el objeto ya existe | el objeto **aun no existe** |
| Se llama desde | `ana.to_dict()` | `Student.from_dict(row)` |
| Nombre del patron | metodo de instancia | **constructor alternativo** |

`from_dict` no puede recibir `self` porque su trabajo es *crear* el objeto: no
hay nada a que apuntar todavia. Recibe `cls`, que es la clase misma, y `cls(...)`
la llama como constructor.

**Que ocurre al ejecutar — el detalle que hace que esto importe:** fijate en
`int(row["spanish"])`.

Un CSV es **texto**. No existen numeros en un CSV: existe el caracter `8`
seguido del caracter `5`. Al leerlo, `row["spanish"]` vale `"85"`, el string. Y
`"85" < 60` revienta con `TypeError`. El reporte de reprobados habria fallado
sobre cualquier dato importado.

Por eso `from_dict` es el lugar correcto para convertir: **la frontera del
sistema es donde se valida y se convierte el tipo.** Adentro, todo son objetos
con tipos correctos. Afuera, texto. En el borde, un traductor.

**Como verificar — la prueba de ida y vuelta (*round-trip test*):**

```python
s = Student("John", "10A", 85, 90, 80, 95)
row = s.to_dict()
clone = Student.from_dict({k: str(v) for k, v in row.items()})

print(clone.to_dict() == row)                   # True
print(type(clone.spanish).__name__)             # int
```

Exportar e importar son **inversos**: la prueba correcta no es que exportar no
de error, es que `objeto -> dict -> objeto` devuelva lo mismo. Esa es la forma
estandar de probar cualquier serializacion.

**Que problema futuro evita:** que las notas lleguen como texto y toda
comparacion numerica falle en silencio o con un `TypeError` lejano.

**Donde se reusa:** es el concepto central de persistencia.
`datetime.fromisoformat()`, `dict.fromkeys()`, `pd.DataFrame.from_records()` —
todos son el mismo patron. En backend: serializers de Django REST, schemas de
Pydantic, `JSON.parse` / `JSON.stringify` en el borde de una API.

El principio: **un objeto no se guarda. Se serializan sus atributos y se
reconstruye al volver.** El objeto que exportaste y el que importaste son dos
objetos distintos (`is` -> `False`) con el mismo contenido.

---

### 3.10 Atributo de clase — una sola fuente de la verdad

**Que es:** un atributo que pertenece a la clase, no a cada instancia.

**Por que existe:** `data.py` tenia la lista de las 6 columnas **escrita dos
veces**: una en exportar, otra en importar. Dos copias de la misma verdad.

El bug que eso garantiza: agregas la materia "matematicas", actualizas la lista
de exportar y olvidas la de importar. Exportas 7 columnas, al importar la
validacion dice "formato invalido" y no entiendes por que. Pierdes una hora.

**Analogia:** el formato de la ficha de expediente es uno para la empresa
entera, no uno por empleado.

**Codigo:**

```python
class Student:
    # Contrato con el CSV: nombre y orden de las columnas.
    FIELDS = (
        "name",
        "section",
        "spanish",
        "english",
        "social_studies",
        "science",
    )
```

```python
            writer = csv.DictWriter(file, fieldnames=list(Student.FIELDS))
```

**Que ocurre al ejecutar / tres decisiones en tres lineas:**

- **Por que atributo de clase y no de instancia:** las columnas son iguales
  para los 500 estudiantes. Un atributo de clase vive **una vez**, en la clase.
  Los de instancia (`self.name`) son los que varian por objeto.
- **Por que tupla `()` y no lista `[]`:** una tupla es inmutable. Es un
  **contrato**, no una coleccion de trabajo. Impide que alguien le haga
  `.append()` por accidente a 3 archivos de distancia. **El tipo que eliges
  comunica tu intencion.**
- **Por que MAYUSCULAS:** convencion de Python para constantes. Le dice a quien
  lee: "esto no cambia en ejecucion".

**Como verificar:** `grep -c '"social_studies"' data.py` debe dar 0 — el nombre
de la columna ya no aparece ahi.

**Que problema futuro evita:** agregar un campo pasa de editar 3 lugares a
editar 1.

**Donde se reusa:** cualquier constante compartida: `MAX_RETRIES`,
`DEFAULT_TIMEOUT`, los `choices` de un campo, el esquema de una tabla. Mismo
principio que `FILENAME = "students.csv"` sacado de dentro de dos funciones.

---

### 3.11 Separacion de capas

**Que es:** cada archivo tiene una sola responsabilidad y solo habla con la
capa vecina.

**Por que existe:** `import_students` construia el diccionario campo por campo
con sus `int()` a mano. Esa logica estaba en el lugar equivocado: la capa de
disco no deberia saber que es un estudiante.

**Analogia:** recepcion habla con la gente, las gerencias aplican reglas, el
expediente define que es un empleado, el archivo guarda papel.

**Codigo / el mapa mental:**

```
menu.py      → UI            habla con el humano: input() y print()
actions.py   → logica        reglas: validar, promediar, filtrar
model.py     → modelo        que ES un estudiante
data.py      → persistencia  archivos, formatos, errores de disco
```

**Como verificar:** la prueba de que las capas estan bien separadas es que
**puedes cambiar una sin tocar las otras.** Quieres guardar en SQLite en vez de
CSV: reescribes `data.py` completo y `model.py`, `actions.py` y `menu.py` no se
enteran.

**Que problema futuro evita:** el cambio que obliga a tocar los 6 archivos.

**Donde se reusa:** es la misma arquitectura de backend:
frontend -> API -> servicio -> repositorio -> base de datos. Y en el stack que
estas aprendiendo: componente React -> endpoint Next -> Prisma -> PostgreSQL.

---

### 3.12 Docstring vs comentario

**Que es:** dos formas de escribir texto en el codigo que **no son
equivalentes**.

```python
class Human:
    """Punto de entrada al cuerpo."""   # docstring: vive DENTRO del objeto
    # This is the entry point...        # comentario: lo borra el interprete
```

**Por que importa:** el comentario existe solo en el archivo de texto. El
docstring queda guardado en `Human.__doc__` y es lo que leen `help(Human)`, el
autocompletado de VS Code y los generadores de documentacion.

**Como verificar:** `print(Human.__doc__)`. Con comentario `#` imprime `None`.

**La regla:** comentario para explicar una decision rara dentro del codigo;
**docstring para declarar el proposito de una clase o funcion.**

---

### 3.13 Importar del modulo dueno

**Que es:** importar cada cosa del archivo donde esta definida, no de un
intermediario.

**Por que existe:** `main.py` hacia `from actions import Student`. Funciona —
Python lo permite, porque `actions` importo `Student` y queda accesible a
traves de el. Pero es **falso documentalmente**: dice "Student vive en actions"
y vive en `model`. Si manana `actions.py` deja de necesitar `Student`, borras
ese import y rompes `main.py` sin entender por que.

**Codigo:**

```python
from actions import Student    # ❌ intermediario
from model import Student      # ✅ el dueno
```

**La regla:** **el import es documentacion ejecutable de tus dependencias.**

Lo mismo aplica a los *type hints*: `menu.py` decia
`def run_menu(student_list: list[dict])` cuando ya eran objetos. Un type hint
equivocado es **peor** que no tenerlo: Python no lo verifica, asi que miente en
silencio y te hace razonar mal.

---
## 4. Errores que cometi

Cada error real vale mas que tres conceptos teoricos. Estos son textuales.

| Error | Que significa | Causa raiz | Como reconocerlo |
|---|---|---|---|
| `zsh: no such user or named directory: cd` | el shell vio `~algo` y busco un usuario llamado `algo` | la tilde quedo **antes** del `cd`: se ejecuto `~cd ~/python/...` | si dice `no such user`, es una tilde mal puesta. **Nunca es tu codigo.** Se evita usando la ruta completa |
| `IndentationError: unexpected indent` | linea corrida a la derecha sin bloque padre | pegue el bloque de verificacion con 4 espacios cuando el `if __name__` todavia no existia | error de **sintaxis**: Python no ejecuta ni una linea. Si aparece antes de cualquier salida tuya, es de forma, no de logica |
| `TypeError: 'Student' object is not subscriptable` | *subscriptable* = "que acepta corchetes" | quedo codigo viejo de diccionarios: `student["name"]` sobre un objeto | un diccionario usa `[]`, un objeto usa `.`. Tras migrar a objetos, **todo `[` sobrante es un bug** |
| `AttributeError: 'Student' object has no attribute 'keys'` | `csv.DictWriter` le pide `.keys()` a cada fila | se le pasaron objetos donde esperaba diccionarios | la libreria te dice que metodo esperaba. Eso te dice que forma de dato queria |
| `AttributeError: property 'head' of 'Human' object has no setter` | la property es de solo lectura | intente asignar `jordan.head = ...` habiendo definido solo la lectura | `has no setter` siempre significa "esto es una property de solo lectura" |
| README desactualizado | la documentacion miente | se migro a objetos y la seccion "Estructura" no menciona `model.py` | la documentacion desactualizada es **peor que la ausente**: hace desconfiar del resto del documento |

### Otros tres errores de criterio, no de sintaxis

| Problema | Por que es un problema |
|---|---|
| Codigo mio en `__pycache__/human/human.py` | `__pycache__/` esta en `.gitignore`: ese archivo **nunca** se iba a commitear. `__pycache__` es basura que Python genera sola |
| Dos clases `Student` (`model.py` y `student.py`) | dos definiciones de la misma clase es peor que ninguna: vas a editar la que no se usa, veras que "no pasa nada", y perderas una tarde |
| Dejar el experimento del Paso 2 en el archivo | `right_hand.name = "broken_hand"` era un experimento, no diseno. Codigo de experimento que se queda se vuelve ruido que en dos semanas no sabras si es intencional o un bug. **El codigo de aprendizaje y el del producto no viven en el mismo lugar** |

---

## 5. Decisiones de diseno

### Decision 1 — `Foot` en singular, no `Feet`

| | |
|---|---|
| **Decision** | la clase se llama `Foot`, aunque el enunciado decia `Feet` |
| **Contexto** | la tarea listaba las clases: Head, Torso, Arm, Hand, Leg, **Feet** |
| **Razon** | `Feet` es el **plural** de `Foot`. Una clase nombra *una* cosa |
| **Alternativas** | seguir el enunciado al pie de la letra |
| **Impacto** | consistencia con la convencion de Python: **clases en singular** (`Student`, no `Students`), listas en plural (`self.students`) |
| **Futuro** | declarado explicitamente en el cuerpo del PR. **Cuando te desvias del enunciado, lo declaras y lo justificas; si no, parece un descuido** |

### Decision 2 — la conversion CSV vive en `Student`, no en `data.py`

| | |
|---|---|
| **Decision** | `to_dict()` y `from_dict()` como metodos de `Student` |
| **Contexto** | hay que traducir objeto <-> diccionario en los dos sentidos |
| **Razon** | la informacion vive junto a quien la posee: `Student` es el unico que debe saber que campos tiene un estudiante |
| **Alternativas** | armar el diccionario dentro de `data.py` (era lo que habia) |
| **Impacto** | agregar un campo se edita en **un** archivo en vez de dos o tres |
| **Futuro** | si manana se exporta a JSON, `data_json.py` reusa el mismo `to_dict()` sin duplicar nada |

### Decision 3 — `to_dict()` explicito en vez de `getattr`

| | |
|---|---|
| **Decision** | escribir los 6 campos a mano en lugar de un diccionario por comprension con `getattr` |
| **Contexto** | se podia escribir en una linea: `{f: getattr(self, f) for f in Student.FIELDS}` |
| **Razon** | los 6 campos explicitos se leen de un vistazo y no requieren entender reflexion |
| **Alternativas** | la version de una linea; o `@dataclass`, que eliminaria el `__init__` completo |
| **Impacto** | mas lineas, menos conceptos nuevos. **Codigo corto no es codigo claro** |
| **Futuro** | `@dataclass` es un atajo honesto *despues* de dominar el `__init__` explicito. No antes |

### Decision 4 — `Human` solo guarda el torso

| | |
|---|---|
| **Decision** | `Human.__init__(self, name, torso)` y nada mas |
| **Contexto** | la tentacion era `Human(name, torso, head, left_arm, ...)` |
| **Razon** | el torso ya tiene la cabeza. Dos copias del mismo dato se desincronizan y no sabes cual creer |
| **Alternativas** | duplicar las referencias en `Human` para acceso directo |
| **Impacto** | un dato vive en un solo lugar; el acceso corto se logra con properties, sin duplicar |
| **Futuro** | insertar `Neck` o `Ankle` cambia **una linea** por property |

### Decision 5 — commit nuevo en vez de `--amend`

| | |
|---|---|
| **Decision** | corregir hacia adelante con un commit nuevo |
| **Contexto** | habia que mover `human/human.py` a `human.py` con el commit ya publicado |
| **Razon** | `--amend` sobre algo publicado exige `git push --force`, que **reemplaza** la historia del remoto |
| **Alternativas** | `--amend` + `--force` (tecnicamente seguro en una rama solo mia y sin PR) |
| **Impacto** | historial con una linea extra, cero riesgo |
| **Futuro** | **reescribe libremente lo que solo existe en tu maquina; una vez publicado, corrige hacia adelante.** El historial no tiene que ser perfecto, tiene que ser cierto |

### Decision 6 — `human_reference.py` fuera del PR

| | |
|---|---|
| **Decision** | borrar del repo la version avanzada que escribio la IA |
| **Contexto** | 208 lineas con clase base, `yield from` y serializacion, que yo no escribi |
| **Razon** | **un PR es una declaracion de autoria**: dice "esto lo hice yo y lo sostengo". No podia explicarlo si me preguntaban |
| **Alternativas** | dejarlo como referencia dentro del repo |
| **Impacto** | el PR contiene solo codigo que entiendo |
| **Futuro** | se reconstruye en los Pasos 8 y 9, escribiendolo yo |

### Decision 7 — lo que decidi NO hacer

Esto es la mitad del trabajo de ingenieria y casi nadie lo explica:

| No se hizo | Por que |
|---|---|
| `@dataclass` | concepto nuevo; el objetivo era practicar clases a mano |
| validacion extra en `from_dict` | ya existe: `int()` lanza `ValueError` y `data.py` lo captura. Agregar mas seria duplicar proteccion |
| reordenar el menu (la opcion 7 "Exit" esta en medio) | es un cambio de UI que nadie pidio. **Arreglas lo que esta roto; no reescribes lo que simplemente no te gusta** |
| aplanar `student_control_2/student_control/` | cosmetico, sin impacto funcional |

---

## 6. Codigo final

### `past-exercises/ejercicios_OOP/human.py`

```python
class Hand:
    def __init__(self, name):
        self.name = name

    def children(self):
        return []


class Foot:
    def __init__(self, name):
        self.name = name

    def children(self):
        return []


class Head:
    def __init__(self, name):
        self.name = name

    def children(self):
        return []


class Arm:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def children(self):
        return [self.hand]


class Leg:
    def __init__(self, name, foot):
        self.name = name
        self.foot = foot

    def children(self):
        return [self.foot]


class Torso:
    def __init__(self, name, head, left_arm, right_arm, left_leg, right_leg):
        self.name = name
        self.head = head
        self.left_arm = left_arm
        self.right_arm = right_arm
        self.left_leg = left_leg
        self.right_leg = right_leg

    def children(self):
        return [
            self.head,
            self.left_arm,
            self.right_arm,
            self.left_leg,
            self.right_leg,
        ]


class Human:
    """Punto de entrada al cuerpo. Conoce el camino hasta cada parte."""

    def __init__(self, name, torso):
        self.name = name
        self.torso = torso

    @property
    def head(self):
        return self.torso.head

    @property
    def left_hand(self):
        return self.torso.left_arm.hand

    @property
    def right_hand(self):
        return self.torso.right_arm.hand

    @property
    def left_foot(self):
        return self.torso.left_leg.foot

    @property
    def right_foot(self):
        return self.torso.right_leg.foot

    def children(self):
        return [self.torso]


def build_human(name):
    """Arma un cuerpo completo y devuelve el Human listo para usar."""
    torso = Torso(
        "torso",
        Head("head"),
        Arm("left_arm", Hand("left_hand")),
        Arm("right_arm", Hand("right_hand")),
        Leg("left_leg", Foot("left_foot")),
        Leg("right_leg", Foot("right_foot")),
    )
    return Human(name, torso)


def show_body(part, level=0):
    """Imprime la parte y todas sus descendientes, indentadas por nivel."""
    print("  " * level + part.name)

    for child in part.children():
        show_body(child, level + 1)


if __name__ == "__main__":
    jordan = build_human("Jordan")

    show_body(jordan)
```

### `student_control_2/student_control/model.py`

```python
class Student:
    """Represent a student and their grades.

    The class owns the translation between the object and the plain dict
    that the CSV layer needs. Nothing else in the program should know the
    shape of a student row.
    """

    # Contrato con el CSV: nombre y orden de las columnas.
    FIELDS = (
        "name",
        "section",
        "spanish",
        "english",
        "social_studies",
        "science",
    )

    def __init__(
        self,
        name: str,
        section: str,
        spanish: int,
        english: int,
        social_studies: int,
        science: int,
    ):
        self.name = name
        self.section = section
        self.spanish = spanish
        self.english = english
        self.social_studies = social_studies
        self.science = science

    def to_dict(self) -> dict:
        """Return the student as a plain dict, ready for csv.DictWriter."""

        return {
            "name": self.name,
            "section": self.section,
            "spanish": self.spanish,
            "english": self.english,
            "social_studies": self.social_studies,
            "science": self.science,
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Student":
        """Build a Student from a CSV row.

        Every value read from a CSV arrives as text, so grades are
        converted back to int here. A bad value raises ValueError and the
        data layer reports it.
        """

        return cls(
            name=row["name"],
            section=row["section"],
            spanish=int(row["spanish"]),
            english=int(row["english"]),
            social_studies=int(row["social_studies"]),
            science=int(row["science"]),
        )
```

### `student_control_2/student_control/data.py` — las dos partes clave

```python
import csv
import os

from model import Student

FILENAME = "students.csv"


def export_students(student_list: list[Student]) -> None:
    ...
            writer = csv.DictWriter(file, fieldnames=list(Student.FIELDS))
            writer.writeheader()

            for student in student_list:
                writer.writerow(student.to_dict())


def import_students() -> list[Student] | None:
    ...
            if reader.fieldnames != list(Student.FIELDS):
                print("The CSV file has an invalid format.")
                return None

            for row in reader:
                students.append(Student.from_dict(row))
```

---

## 7. El metodo

Lo que importa no son los fixes. Es el **orden** en que se hicieron. Esta
seccion es la mas transferible: el codigo envejece, el metodo no.

**1. Leer antes de tocar.** Se leyeron los 6 archivos completos antes de
escribir una linea. No puedes arreglar un sistema cuyas conexiones no conoces.
Costo: 5 minutos. Ahorro: no romper algo que no sabias que dependia de eso.

**2. Reproducir el fallo antes de arreglarlo.** No "esto parece mal", sino el
error en pantalla:

```
TypeError: 'Student' object is not subscriptable
```

Si no puedes reproducir un bug, no sabes si existe — y no vas a saber si lo
arreglaste. **Primero el error, despues el fix.**

**3. Preguntarle al codigo, no a tu memoria.** Para encontrar los restos de la
migracion no se leyeron 294 lineas a ojo:

```bash
grep -n 'student\[' actions.py
```

Un diccionario se accede con `[]`, un objeto con `.`. **Cuando cambias una
representacion de datos, busca el patron sintactico de la representacion vieja**
y verifica que no quede ninguno. Y se volvio a correr el mismo grep al
terminar, para probar que quedo vacio. Eso es una prueba, no una esperanza.

**4. Ordenar por impacto, no por facilidad.** Primero lo que esta roto en
produccion (los crashes), despues la deuda estructural (duplicacion), al final
lo cosmetico (la extension `.py`). **Nunca empieces por lo bonito.**

**5. Un cambio, una verificacion.** Despues de cada fix se corrio algo que lo
probaba. Si haces los 6 cambios y luego pruebas, un error te deja con 6
sospechosos. Asi puedes decir "este cambio produjo este resultado".

**6. Probar la ida y la vuelta, no una mitad.** Para la serializacion no basto
que exportar no diera error:

```python
clone.to_dict() == row     # True
```

**7. Probar el programa real, no solo las piezas.** Al final se simulo un
usuario completo:

```bash
printf '1\nAna Lopez\n10A\n85\n...\n7\n' | python3 main.py
```

Las piezas pueden funcionar y el conjunto estar roto. Y se hizo **en una
copia**, para no dejar un `students.csv` de prueba en el proyecto.

**8. Antes de reemplazar, verifica que el patron identifica lo que crees.** Al
editar archivos con un script, cada reemplazo llevo esta guarda:

```python
assert src.count(old) == 1, f"patron ambiguo o ausente: {old[:40]!r}"
```

0 veces = mi suposicion era falsa. 2 veces = el reemplazo tocaria algo que no
quiero. Y todo en un solo `write_text()` al final: si un `assert` falla, el
archivo queda intacto. Se cambia todo o no se cambia nada — eso es
**atomicidad**, la misma idea de una transaccion de base de datos.

**9. Antes de borrar, comprueba quien lo usa.** Antes de eliminar `student.py`:

```bash
grep -rn "import student" .     # nadie
```

Y que su contenido fuera un subconjunto de `model.py`. **Nunca borres por
intuicion.**

---

## 8. Comandos usados

| Comando | Que hace | Por que se uso |
|---|---|---|
| `pwd` | imprime la carpeta actual | **nunca ejecutes el comando siguiente sin verificar que el anterior te dejo donde creias**. La mitad de los errores de principiante son comandos correctos en la carpeta equivocada |
| `ls` / `ls -la` | lista archivos | verificar que el `mv` o el `rm` hizo lo esperado |
| `cd /ruta/completa` | cambia de carpeta | se uso la ruta completa en vez de `~` tras el error de la tilde |
| `mv viejo nuevo` | mueve o renombra | `bus_py` -> `bus.py`; guardar `human.py` como `human_reference.py` |
| `rm archivo` | borra | eliminar el duplicado `student.py` |
| `grep -n 'patron' archivo` | busca con numero de linea | encontrar los restos de diccionarios |
| `grep -rn 'patron' .` | busca recursivo | comprobar que nadie importaba `student.py` |
| `python3 archivo.py` | ejecuta | la verificacion de cada paso |
| `git status` | muestra que vas a guardar antes de guardarlo | **el equivalente a mirar el carrito antes de pagar.** Siempre antes de un commit |
| `git add ruta/explicita` | pasa archivos al staging | **nunca `git add .`** con dos carpetas sin seguimiento: habria mezclado dos trabajos independientes |
| `git commit -m "..."` | guarda el cambio | dos commits: un commit = la unidad mas pequena que tiene sentido por si sola |
| `git branch -m nuevo-nombre` | renombra la rama actual | `Ejercicios_OOP` -> `ejercicios-oop`, por consistencia con `main` y `student-control` |
| `git mv viejo nuevo` | mueve y registra el cambio en un paso | con `mv` suelto hay que hacer `git add` dos veces (ruta vieja + ruta nueva) y olvidar una deja el commit a medias |
| `git push -u origin rama` | crea la rama en el remoto | `-u` (*upstream*) enlaza local y remota: de ahi en adelante basta `git push` |
| `gh pr create --base main --title ... --body ...` | abre el pull request | el cuerpo responde: que hice, por que asi, y como verifique que funciona |
| `git ls-files ruta/` | lista los archivos versionados | verificar que entro al commit y que no |
| `git add -n ruta/` | simula un `add` sin modificar nada | ver que se subiria **antes** de subirlo |
| `git status --short --ignored` | incluye lo ignorado | confirmar que `__pycache__` y `.DS_Store` quedaban fuera |

### Dos reglas de Git que salieron de esta sesion

**Git no versiona carpetas, versiona archivos.** Una carpeta no existe en Git
como entidad: existe porque hay un archivo cuya ruta la menciona. Por eso no
hubo que "borrar la carpeta `human/`": al mover el archivo, la carpeta
desaparecio sola. Corolario: Git **no puede** versionar una carpeta vacia; si
necesitas que exista (`logs/`), el truco estandar es un `.gitkeep` vacio.

**Un PR = un cambio con un proposito.** Habia dos carpetas sin seguimiento y
solo una iba en el PR. Un PR que hace dos cosas no se puede revisar ni revertir
por partes. **Agrega por ruta explicita, siempre.**

---

## 9. Pendientes

- [ ] Escribir `count_parts(part)` en `human.py` — misma estructura que
      `show_body`, pero sumando y devolviendo en vez de imprimir. Debe dar 11
- [ ] **Paso 8:** herencia — clase base `BodyPart` para eliminar la repeticion
      de `self.name` y `children()` en las 7 clases
- [ ] **Paso 9:** `to_dict()` en el arbol del cuerpo -> exportar a JSON
- [ ] Merge del PR #3
- [ ] El `student_control/` de la raiz sigue pendiente en su propio PR (#2)

---

## 10. Repaso de 10 minutos

Las cinco ideas que hay que recordar si no se lee nada mas:

1. **Asignar no copia, comparte.** `self.hand = hand` guarda una direccion, no
   un clon. De ahi sale la regla de **un solo dueno por objeto**, y de ahi sale
   la mitad de los bugs raros de Python.

2. **El codigo de afuera debe depender de lo que prometes, no de como lo
   cumples.** Fachada y `@property` existen para eso: cambias el interior y
   nadie afuera se entera. Si ves `a.b.c.d`, es senal de acoplamiento.

3. **Separa construir de usar.** Una clase define *que es* una cosa; la fabrica
   sabe *como se ensambla*. Mezclarlos es lo que hace un proyecto imposible de
   cambiar.

4. **Haz una pregunta y confia en la respuesta.** `part.children()` en vez de
   `isinstance(part, Arm)`. Eso es polimorfismo, y es lo que permite agregar
   clases nuevas sin editar codigo que ya funciona.

5. **Un objeto no se guarda: se serializan sus atributos.** Y la conversion de
   tipos ocurre **en la frontera** del sistema. Afuera texto, adentro objetos
   con tipos correctos, en el borde un traductor.

Y el metodo, en una linea: **lee antes de tocar, reproduce el fallo antes de
arreglarlo, un cambio a la vez, y verifica con el programa real.**
