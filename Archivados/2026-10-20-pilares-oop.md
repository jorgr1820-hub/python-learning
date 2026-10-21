# Los 4 pilares de OOP y criterio de diseno — 2026-10-20

## 0. Ficha rapida

| | |
|---|---|
| **Fecha** | 2026-10-20 |
| **Tema** | Los 4 pilares de OOP aplicados a un proyecto de 4 ejercicios: invariantes y sus puertas, Template Method, clases abstractas, herencia multiple y MRO |
| **Archivos tocados** | `past-exercises/ejercicios_OOP/pilares_oop/{accounts.py, shapes.py, multiple_inheritance.py, README.md}` |
| **Estado** | Los 4 ejercicios completos. 12/12 requisitos verificados con un script independiente de las demos |
| **Rama / PR** | `ejercicios-oop`, commit `9da5746` -> PR #3 en `jorgr1820-hub/python-learning` |
| **Conceptos nuevos** | invariante y sus puertas, `@property` de solo lectura, Template Method, `ABC`/`@abstractmethod`, polimorfismo sin `if`, excepciones de dominio, `Decimal` vs `float`, MRO y linealizacion C3, mixins, `__init__` cooperativo, principio de Liskov, objeto de valor inmutable, composicion vs herencia |
| **Pendientes** | predecir `Diamond().who()` antes de correrlo; decidir si `BankAccount.__init__` debe llamar a `super().__init__()`; `change_minimum()`; tests con pytest; y los heredados `count_parts()` y pasos 8-9 de `human.py` |

---

## 1. La analogia maestra

**Todo este tema es una sucursal de banco, y mi trabajo no es atender la
ventanilla: es escribir el reglamento.**

El cajero ejecuta: recibe plata, la cuenta, la entrega. Un cajero bueno es
rapido. Pero el cajero **no decide** que esta permitido, y si decidiera, cada
ventanilla tendria reglas distintas y el banco quebraria.

El gerente escribe el reglamento: *"ninguna cuenta puede quedar bajo su
minimo"*. Esa frase, escrita **una vez**, se cumple en las 40 ventanillas, en
el cajero automatico, en la app, y en las cuentas que inventen el ano que
viene. El gerente no esta presente en ninguna transaccion y esta en todas.

La misma sucursal explica el resto del tema:

- **El reglamento** que nadie puede romper, por ninguna via, es el
  **invariante**. Y las **puertas** del edificio son todas las formas de
  entrar: si pones un guardia solo en la principal, el reglamento no se
  cumple, aunque tengas un guardia.
- **El examen en la puerta.** Para manejar un vehiculo de la empresa hay que
  aprobar dos pruebas. No te dan las llaves hasta que las dos esten
  aprobadas. Eso es una **clase abstracta**: lo contrario es un cartel que
  dice "por favor sepan frenar" y te enteras el dia que haya que frenar.
- **El cargo** de un empleado es uno solo y viene de un organigrama: es
  **herencia simple**. Las **certificaciones extra** (primeros auxilios,
  manejo de carga) son capacidades cruzadas que cualquiera puede tener en
  cualquier combinacion, y no cambian su cargo: son **mixins**.
- **El legajo** que lista las certificaciones en orden, y define cual se
  aplica primero, es el **MRO**.
- **El despachador** grita "arranca ruta" por radio y cada vehiculo arranca a
  su manera sin que a el le importe como: **polimorfismo**.
- **El capo cerrado** del motor y la puerta que solo abre el conductor son el
  **encapsulamiento**: la gasolina entra por la boquilla, no al cilindro.

### Traduccion analogia -> termino tecnico

| En la sucursal | En el codigo | Nombre tecnico |
|---|---|---|
| El cajero que ejecuta | `withdraw()`, `deposit()` | metodo |
| El reglamento que nadie rompe | `balance >= minimo` | **invariante** |
| El gerente que lo escribe una vez | `BankAccount` | clase padre |
| Las entradas del edificio | constructor, asignacion, operaciones | las **puertas** del invariante |
| "Ahorro usa el mismo reglamento con otro piso" | `SavingsAccount` | subclase |
| El gerente pregunta "cual es tu minimo?" | `_minimum_balance()` | **Template Method** / hook |
| Que el cajero no pueda abrir la boveda | `@property` sin setter | encapsulamiento |
| El examen en la puerta | `ABC` + `@abstractmethod` | clase abstracta |
| El cargo en el organigrama | `class SavingsAccount(BankAccount)` | herencia simple |
| Las certificaciones extra | `AuditLogMixin`, `TimestampedMixin` | **mixins** |
| El legajo en orden | `__mro__` | Method Resolution Order |
| El despachador con el radio | el bucle `for` sin un solo `if` | polimorfismo |
| Contratar un servicio externo en vez de certificar | `AuditTrail` guardado como atributo | composicion |

### La frase que resume todo

> El que construye escribe el cajero. El que tiene criterio escribe el
> reglamento, y despues el cajero sale solo.

---

## 2. El mapa

```
pilares_oop/
│
├── accounts.py ──────────── dominio: dinero (conteo exacto -> Decimal)
│   │
│   │   AccountError
│   │     ├── InvalidAmount           monto cero, negativo o float
│   │     ├── InsufficientFunds       el retiro romperia el invariante
│   │     └── OpeningBalanceTooLow    la cuenta naceria violandolo
│   │
│   │   BankAccount
│   │     balance ──────── @property sin setter (PUERTA 2 cerrada)
│   │     deposit()  ──┐
│   │     withdraw() ──┤
│   │                  ▼
│   │            available  =  balance − ¿cual es tu minimo?
│   │                                     │
│   │                          _minimum_balance()   ← LA COSTURA
│   │                             ┌───────┴───────┐
│   │                             ▼               ▼
│   │                       BankAccount      SavingsAccount
│   │                       responde 0       responde min_balance
│   │                                              │
│   └── SavingsAccount(BankAccount) ───────────────┘
│         6 lineas: guarda su minimo y responde el hook.
│         NO reescribe withdraw(), deposit(), validacion ni constructor.
│
├── shapes.py ────────────── dominio: geometria (medicion -> float, math.pi)
│   │
│   │   Shape(ABC)
│   │     @abstractmethod calculate_perimeter()  ─┐ el contrato: sin estos
│   │     @abstractmethod calculate_area()       ─┘ dos, no hay instancia
│   │     describe()      ← concreto: escrito una vez, lo tienen todas
│   │     _positive()     ← el invariante comun, escrito una vez
│   │        ┌──────────────┼──────────────┐
│   │        ▼              ▼              ▼
│   │     Circle         Square        Rectangle
│   │     radius          side         width, height
│   │
│   └── las tres inmutables: las dimensiones son su identidad
│
└── multiple_inheritance.py ─ usa SavingsAccount del primer archivo
    │
    │   A) El diamante           B) Los mixins
    │                                AuditedSavingsAccount  (cuerpo VACIO)
    │        Base                            │
    │       /    \                           ▼  el MRO encadena solo:
    │    Left    Right              AuditLogMixin      registra
    │       \    /                        ▼
    │      Diamond                 TimestampedMixin    marca tiempos
    │                                     ▼
    │   super() no es "mi padre":   SavingsAccount     aplica el minimo
    │   es "el siguiente del MRO"         ▼
    │                                BankAccount       mueve la plata
    │
    └── C) AuditTrail: la misma capacidad por composicion, para comparar
```

---

## 3. Conceptos

### El invariante y sus puertas

**Que es:** una frase que siempre tiene que ser verdad sobre un objeto, y que
no puede dejar de serlo **por ningun camino**. Las **puertas** son todas las
formas concretas de hacerla falsa.

**Por que existe:** porque una validacion y un invariante no son lo mismo. Una
validacion la pones en un lugar; un invariante lo defendes en **todos**. Sin
este concepto uno tapa la via que el enunciado menciona y cree que termino.

**Analogia:** el reglamento del estadio dice "nadie entra sin entrada". Las
puertas son la principal, la de servicio, el porton de camiones y la ventana
del bano. Un guardia solo en la principal no cumple el reglamento.

**Codigo:**

```python
class BankAccount:
    # Invariante: el balance nunca queda bajo el minimo permitido de la cuenta.

    def __init__(self, owner: str, balance: Money = Money("0")) -> None:
        self.owner = owner
        self._balance = self._as_money(balance)
        minimum = self._minimum_balance()          # PUERTA 1
        if self._balance < minimum:
            raise OpeningBalanceTooLow(self._balance, minimum)

    @property
    def balance(self) -> Money:                    # PUERTA 2: no hay setter
        return self._balance

    def deposit(self, amount: Money) -> Money:
        amount = self._as_positive_money(amount)   # PUERTAS 4, 6, 7
        self._balance += amount
        return self._balance

    def withdraw(self, amount: Money) -> Money:
        amount = self._as_positive_money(amount)
        if amount > self.available:                # PUERTA 3
            raise InsufficientFunds(requested=amount, available=self.available)
        self._balance -= amount
        return self._balance
```

**Que ocurre al ejecutar:** cada operacion pasa primero por la conversion y la
validacion del monto, y solo despues toca `self._balance`. El balance real
vive en `_balance` (un atributo de instancia, en el diccionario `__dict__` del
objeto) y el nombre publico `balance` es un descriptor de clase que solo sabe
leerlo: no existe ninguna via de escritura desde afuera.

**Como verificar:**

```bash
python3 accounts.py   # seccion "Las 7 puertas del invariante"
```

```
[tapada ] 1. BankAccount('X', -500)                  OpeningBalanceTooLow
[tapada ] 2. cuenta.balance = -5000                  AttributeError
[tapada ] 3. retirar 999 teniendo 120                InsufficientFunds
[tapada ] 4. deposit(-500), retiro disfrazado        InvalidAmount
[tapada ] 5. SavingsAccount(min=500, balance=100)    OpeningBalanceTooLow
[tapada ] 6. deposit(0)                              InvalidAmount
[tapada ] 7. deposit(10.5) como float                InvalidAmount
el balance no se movio  -> 120  (sigue en 120)
```

**Que problema futuro evita:** objetos en estado invalido circulando por el
sistema. Un balance negativo que nadie puede explicar, y que explota lejos del
lugar donde entro. De las 7 puertas, el enunciado nombraba **una**.

**Donde se reusa:** en todas partes. Constraints de base de datos
(`CHECK balance >= 0`), validadores de DTO en NestJS, reglas de un Service.
En el CRM: un cliente no puede tener email vacio, un pedido no puede tener
total negativo, un usuario no puede quedar sin rol.

---

### Encapsulamiento: `@property` de solo lectura

**Que es:** un atributo que se lee como un dato pero que por detras es un
metodo, y que sin `setter` no se puede escribir desde afuera.

**Por que existe:** para que los datos con reglas no se puedan cambiar sin
pasar por las reglas. Es la diferencia entre ver el saldo de tu cuenta y poder
escribirlo.

**Analogia:** le pedis un dato a la recepcionista y te lo da. No te enteras si
estaba en su escritorio o si llamo a otro piso. Y no podes escribir en su
planilla.

**Codigo:**

```python
@property
def balance(self) -> Money:
    """Se lee, no se escribe."""
    return self._balance

@property
def available(self) -> Money:
    """Calculado, no guardado. Para quien lo usa son iguales."""
    return self._balance - self._minimum_balance()
```

**Que ocurre al ejecutar:** `cuenta.balance` no busca una clave en el
diccionario del objeto: encuentra un descriptor en la clase y ejecuta la
funcion. `cuenta.balance = X` busca el metodo `__set__` del descriptor, no lo
encuentra, y lanza `AttributeError`. `available` demuestra lo otro: para quien
lo usa, un dato guardado y un dato calculado se ven **identicos**, asi que
podes cambiar de uno a otro sin que nadie se entere.

**Como verificar:**

```python
>>> cuenta.balance
Decimal('120')
>>> cuenta.balance = Decimal("999")
AttributeError: property 'balance' of 'BankAccount' object has no setter
```

**Que problema futuro evita:** que alguien cambie el estado sin pasar por las
reglas (puerta 2), y que convertir un dato guardado en un dato calculado
obligue a tocar todo el codigo que lo usaba.

**Donde se reusa:** getters de TypeScript, `@Column` de Prisma con campos
derivados, campos computados de un serializador. En el CRM: el total de un
pedido deberia ser `@property` sobre sus items, no un numero guardado que
puede quedar desincronizado.

---

### Herencia y `super()`

**Que es:** una clase hija recibe los atributos y metodos de la madre, y puede
agregar o reemplazar. `super()` llama a la version de mas arriba.

**Por que existe:** para no escribir la misma regla dos veces. Si esta escrita
dos veces, tarde o temprano una se actualiza y la otra queda vieja y mintiendo.

**Analogia:** el manual del "Vehiculo de la empresa" dice placa, kilometraje y
mantenimiento. El manual del Bus dice "aplica todo el de Vehiculo, mas el
aforo". Nadie reescribe "tiene placa" tres veces.

**Codigo:**

```python
class SavingsAccount(BankAccount):
    def __init__(self, owner, min_balance, balance=Money("0")):
        min_balance = self._as_money(min_balance)
        if min_balance < 0:
            raise InvalidAmount(...)
        self._min_balance = min_balance      # ANTES de super()
        super().__init__(owner, balance)
```

**Que ocurre al ejecutar:** `self._min_balance` se guarda primero y **recien
despues** corre el constructor del padre. Ese orden es obligatorio y no
cosmetico: el `__init__` del padre llama a `_minimum_balance()`, que lee ese
atributo. Invertir las dos lineas da `AttributeError`, y el mensaje apunta al
**padre** aunque la causa este en el **hijo**.

**Como verificar:**

```python
>>> s = SavingsAccount("J", Money("500"), Money("1000"))
>>> "deposit" in SavingsAccount.__dict__      # ella no lo define
False
>>> s.deposit(Money("100"))                   # y funciona igual
Decimal('1100')
```

Esa es la prueba fuerte. `isinstance()` solo comprueba lo que **declaraste**;
llamar un metodo que la hija no define comprueba lo que **funciona**.

**Que problema futuro evita:** la regla duplicada. Si `SavingsAccount`
reescribiera `withdraw()`, el dia que se agregue una comision de retiro la
cuenta de ahorro quedaria gratis hasta que alguien lo note.

**Donde se reusa:** `extends` de TypeScript, clases base de NestJS, modelos
abstractos de Prisma. Regla transferible: **si el `__init__` del padre llama a
un metodo que el hijo sobreescribe, el hijo tiene que estar completo antes de
`super()`**.

---

### Template Method: el padre pregunta, el hijo responde

**Que es:** el padre escribe la coreografia completa de una operacion y deja
**huecos con nombre** que el hijo rellena. El hijo cambia un dato, no el
procedimiento.

**Por que existe:** es la respuesta a "como varia el comportamiento sin
duplicar la mecanica". Sin esto, cada subclase reescribe el metodo entero y
copia las partes que no cambian.

**Analogia:** el gerente no escribio un reglamento nuevo para la cuenta de
ahorro. El manual de retiros es el mismo; lo unico distinto es **que cuenta
como disponible**. Pregunta "cual es tu minimo?" y cada cuenta responde.

**Codigo:**

```python
# en el padre
@property
def available(self) -> Money:
    return self._balance - self._minimum_balance()

def withdraw(self, amount: Money) -> Money:
    amount = self._as_positive_money(amount)
    if amount > self.available:          # nunca menciona el minimo
        raise InsufficientFunds(requested=amount, available=self.available)
    self._balance -= amount
    return self._balance

def _minimum_balance(self) -> Money:
    return Money("0")                    # la cuenta base no tiene minimo

# en el hijo: la unica linea que cambia de verdad
def _minimum_balance(self) -> Money:
    return self._min_balance
```

**Que ocurre al ejecutar:** `withdraw()` llama a `self.available`, que llama a
`self._minimum_balance()`. La busqueda de ese metodo arranca en la **clase
real del objeto**, no en la clase donde esta escrito el `withdraw`. Con una
`SavingsAccount` encuentra la version de la hija. El mismo `withdraw()`, dos
comportamientos, cero `if`.

**Como verificar:**

```bash
python3 accounts.py   # seccion "El pago del diseno: polimorfismo"
```

```
BankAccount(owner='Ana', balance=300)                        disponible=300
SavingsAccount(owner='Jordan', balance=500, min_balance=500) disponible=0
```

**Que problema futuro evita:** la mecanica duplicada. Una `CheckingAccount`
con sobregiro de −200 son 4 lineas (su minimo responde `Money("-200")`) y cero
cambios en el padre. Y una comision de retiro se agrega en **un** lugar.

**Donde se reusa:** es uno de los patrones mas usados que existen. Los hooks
del ciclo de vida de React, los lifecycle hooks de NestJS
(`onModuleInit`), `beforeSave` de un ORM. En el CRM: un `BaseService` con el
flujo "validar -> autorizar -> ejecutar -> auditar" donde cada servicio
concreto solo implementa `ejecutar`.

---

### Clase abstracta: `ABC` y `@abstractmethod`

**Que es:** una clase que no se puede instanciar y que **obliga** a sus hijas
a implementar ciertos metodos. Falla al crear el objeto, no al llamarlo.

**Por que existe:** porque "por favor implementa estos dos metodos" escrito en
un comentario no es un contrato. Con tres o mas implementadores, el olvido es
cuestion de tiempo.

**Analogia:** el examen en la puerta. No te dan las llaves del vehiculo hasta
que apruebes frenar y estacionar. Lo contrario es un cartel pidiendo por favor.

**Codigo:**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_perimeter(self) -> float: ...

    @abstractmethod
    def calculate_area(self) -> float: ...

    # Una clase abstracta SI puede tener metodos concretos:
    def describe(self) -> str:
        return (f"{type(self).__name__:<10} "
                f"perimetro={self.calculate_perimeter():>8.2f}  "
                f"area={self.calculate_area():>8.2f}")
```

**Que ocurre al ejecutar:** al crear la clase, la metaclase `ABCMeta` junta
los nombres marcados con `@abstractmethod` en `__abstractmethods__`. Cada
intento de instanciar revisa ese conjunto: si queda algun nombre sin
implementar, lanza `TypeError` **antes** de que exista el objeto.

**Como verificar:**

```
>>> Shape()
TypeError: Can't instantiate abstract class Shape without an implementation
for abstract methods 'calculate_area', 'calculate_perimeter'

>>> Triangle(3, 4, 5)        # implementa solo el perimetro
TypeError: Can't instantiate abstract class Triangle without an
implementation for abstract method 'calculate_area'
```

El mensaje **nombra los metodos que faltan**: por eso el requisito "tiene los
dos metodos abstractos" se verifica con el mismo error, sin test aparte.

**Que problema futuro evita:** la hija incompleta que circula por el sistema y
explota en produccion la primera vez que alguien pide el area. Con `ABC` el
error llega en el momento mas barato posible.

**Donde se reusa:** `interface` de TypeScript, `abstract class` de Java y C#,
los Protocol de Python cuando no podes tocar las clases. En el CRM: una
interfaz `Notifier` que obligue a todo canal nuevo a implementar `send()`.

---

### Polimorfismo

**Que es:** codigo que llama al mismo metodo sobre objetos distintos, y cada
objeto responde con su propia version. En Python no hace falta herencia: basta
que el metodo exista (duck typing).

**Por que existe:** para que el codigo que usa los objetos **no tenga que
cambiar** cuando aparece un tipo nuevo. No es "poder llamar al mismo metodo":
es no volver a tocar el bucle nunca mas.

**Analogia:** el despachador grita "arranca ruta" por radio. El bus arranca con
llave, la van con boton, el camion electrico en silencio. El no sabe ni le
importa, y cuando lleguen motos no cambia de guion.

**Codigo:**

```python
shapes: list[Shape] = [Circle(5), Square(4), Rectangle(3, 7)]

for shape in shapes:
    print(shape.describe())          # cero ifs

total = sum(s.calculate_area() for s in shapes)
```

**Que ocurre al ejecutar:** en cada vuelta, `shape` apunta a un objeto de otra
clase. `shape.describe()` resuelve en `Shape`, y el `calculate_area()` que
`describe()` llama por dentro se resuelve en la clase **real** del objeto. El
bucle nunca pregunta de que tipo es nada.

**Como verificar:**

```bash
python3 shapes.py
```

```
Circle     perimetro=   31.42  area=   78.54
Square     perimetro=   16.00  area=   16.00
Rectangle  perimetro=   20.00  area=   21.00
area total = 115.54
```

**Que problema futuro evita:** la cadena de `if tipo == "circulo" elif ...`,
que obliga a volver al mismo archivo cada vez que se agrega un tipo. La senal
de olor es exactamente esa: **si estas preguntando de que tipo es algo,
probablemente el objeto deberia responderlo el mismo**.

**Donde se reusa:** en todo. El `children()` de `human.py` del 4 de octubre ya
era esto. En el CRM: una lista de notificadores (email, SMS, WhatsApp) que se
recorre llamando `send()`, y agregar Telegram es una clase nueva y cero
cambios en el codigo que notifica.

---

### Herencia multiple: MRO y mixins

**Que es:** heredar de dos o mas padres a la vez. El **MRO** (Method
Resolution Order) es la lista plana y ordenada de clases que Python calcula
con el algoritmo de linealizacion C3 para decidir quien responde cada llamada.
Un **mixin** es una clase chica que agrega **una capacidad ortogonal**.

**Por que existe:** para combinar capacidades cruzadas sin meterlas en la
jerarquia principal. "Ser cuenta de ahorro" y "llevar un log de auditoria" son
dos ejes que no se tocan: cualquier cuenta podria auditarse, y auditarse no la
convierte en otro tipo de cuenta.

**Analogia:** el cargo de un empleado es uno solo y sale del organigrama. Sus
certificaciones (primeros auxilios, manejo de carga) son extras combinables
que no cambian su cargo. El legajo las lista en orden: ese orden es el MRO.

**Codigo:**

```python
class TimestampedMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     # cooperativo
        now = _now()
        self.created_at = now
        self.updated_at = now

    def deposit(self, amount):
        result = super().deposit(amount)
        self.touch()
        return result


class AuditLogMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.audit_log: list[dict] = []

    def deposit(self, amount):
        new_balance = super().deposit(amount)   # super() ANTES de registrar
        self._record("deposit", amount, new_balance)
        return new_balance


class AuditedSavingsAccount(AuditLogMixin, TimestampedMixin, SavingsAccount):
    """Cuerpo vacio a proposito: cero logica propia."""
```

**Que ocurre al ejecutar:** `account.deposit(250)` entra por
`AuditLogMixin.deposit`, cuyo `super()` **no es su padre** sino el siguiente
del MRO: `TimestampedMixin.deposit`. El `super()` de ese llega a
`BankAccount.deposit`, que mueve la plata. Al volver, cada capa hace lo suyo en
orden inverso. Tres clases que no se conocen entre si, encadenadas sin que
ninguna sepa quien sigue.

La idea que cambia todo:

> `super()` **no** significa "mi clase padre". Significa **"la siguiente clase
> en el MRO del objeto real"**.

Y los mixins van **a la izquierda** de la clase base: el MRO se recorre de
izquierda a derecha, asi que interceptan antes de que la cuenta real trabaje.

**Como verificar:**

```bash
python3 multiple_inheritance.py
```

```
MRO: AuditedSavingsAccount -> AuditLogMixin -> TimestampedMixin
     -> SavingsAccount -> BankAccount -> object

log (2 entradas; el retiro rechazado NO esta):
  deposit      250  -> balance 1250
  withdraw     300  -> balance 950
```

Y el diamante, en 12 lineas: con `Left(Base)`, `Right(Base)` y
`Diamond(Left, Right)`, el `super()` escrito dentro de `Left` **llama a
`Right`**, que no es su padre y que `Left` ni conoce. `Base` aparece una sola
vez en el MRO: el diamante no la duplica.

**Que problema futuro evita:** repetir la misma capacidad en cada clase que la
necesita. Pero el riesgo real es el **orden**: invertirlo (la clase base
primero) **no lanza error** — los mixins quedan inertes, en silencio, y la
auditoria simplemente no existe.

**Donde se reusa:** Django (`class UserList(LoginRequiredMixin, ListView)`),
DRF, los decoradores e interceptores de NestJS. Java y C# **prohiben** la
herencia multiple de clases: decidieron que el poder no compensaba el riesgo.
Eso dice cuanto cuidado merece.

---

### Composicion vs herencia

**Que es:** en vez de heredar una capacidad, guardar un objeto que la tiene y
pedirsela.

**Por que existe:** porque la herencia es un compromiso fuerte y permanente, y
la mayoria de las veces que uno quiere "reutilizar codigo" lo que necesita es
un colaborador, no un padre.

**Analogia:** certificar al empleado (herencia) o contratar un servicio
externo (composicion). El certificado va con el a todas partes y es invisible;
al servicio hay que llamarlo, y se puede cambiar de proveedor.

**Codigo:**

```python
class AuditTrail:
    def __init__(self) -> None:
        self.entries: list[dict] = []

    def record(self, action: str, amount, balance) -> None:
        self.entries.append({"at": _now(), "action": action,
                             "amount": amount, "balance": balance})

# uso: explicito, hay que acordarse
trail = AuditTrail()
plain.deposit(Money("200"))
trail.record("deposit", Money("200"), plain.balance)
```

**Que ocurre al ejecutar:** nada automatico. Si el que llama se olvida de
`record()`, no hay log y nadie protesta. Con el mixin, en cambio, el registro
ocurre dentro de `deposit()` y es imposible de olvidar — pero tambien es
invisible, y en seis meses uno no se acuerda de que existe.

**Como verificar:** la seccion C de `multiple_inheritance.py` corre las dos
versiones de la misma capacidad, una al lado de la otra.

**La bisagra:**

| | Mixin | Composicion |
|---|---|---|
| Para quien usa la clase | **invisible** | **explicito** |
| Ventaja | imposible de olvidar | facil de seguir y de leer |
| Riesgo | el MRO se vuelve dificil; uno olvida que existe | facil olvidar llamarlo |
| Elegilo si | la capacidad debe envolver metodos existentes de forma transparente | queres compartir el log entre objetos, configurarlo o apagarlo en caliente |

**Que problema futuro evita:** jerarquias de 6 niveles donde para entender una
clase hay que leer 6 archivos (el "problema del yo-yo").

**Donde se reusa:** es la regla mas citada del diseno orientado a objetos:
**"preferi composicion sobre herencia"**. Inyeccion de dependencias en NestJS,
el `Repository` que un `Service` recibe en el constructor. En el CRM: el
Service **tiene** un Repository, no **es** un Repository.

---

## 4. Errores que cometi

| Error | Que significa | Causa raiz | Como reconocerlo |
|-------|---------------|------------|------------------|
| `class BankAccount(): self.balance` | `NameError: name 'self' is not defined` | Confundir el molde con la galleta. El cuerpo de la clase corre una vez, al importar, cuando no existe ninguna instancia: `self` todavia no significa nada | Si escribis `self.` y no estas dentro de un `def`, esta mal. El estado nace en `__init__` |
| El helper de la demo no atrapaba `AttributeError` | `AttributeError: property 'radius' of 'Circle' object has no setter` cortó el script a mitad, con traceback | El `except (TypeError, ValueError)` no incluia el error que lanza una property sin setter. Escribi el `except` pensando en los errores que **yo** iba a provocar, no en los que el codigo **puede** lanzar | Un script que corre a medias y muere en el medio. Los `except` con tupla explicita hay que revisarlos cada vez que se agrega un caso nuevo |
| Afirmé que invertir el orden de los mixins daria `AttributeError` | **Falso.** No lanza nada: `deposit()` se resuelve en `BankAccount`, que aparece antes que los mixins en el MRO, asi que los mixins quedan **inertes y mudos**. `hasattr(obj, 'audit_log')` -> `False`, y el deposito funciona igual | Razoné bien la cadena de `__init__` y no previne la resolucion de `deposit`. Deduje en vez de correr | Cuando una prediccion suena solida pero nunca se ejecuto. **Un sistema que falla en silencio es peor que uno que falla fuerte** |
| `s.replace(viejo + " |", nuevo)` con `assert viejo in s` | El README no se actualizo y **el assert paso igual**: validé un string y reemplacé otro distinto | La verificacion y la operacion no miraban lo mismo. Un assert que no comprueba exactamente lo que vas a hacer da falsa confianza | "Dice que funciono pero el archivo no cambio". Verificar el **resultado** (celdas vacias restantes), no la intencion |

Los dos ultimos son los que mas ensenan, y los dos son la misma leccion:
**"lo razone y tiene sentido" no es verificacion**.

---

## 5. Decisiones de diseno

### 1. El tipo del dinero

| | |
|---|---|
| **Decision** | `Decimal`, con el alias semantico `Money = Decimal` |
| **Contexto** | Hay que guardar balances y montos, y compararlos contra un minimo |
| **Razon** | El dinero es un **conteo exacto**, no una medicion. `Decimal` hace aritmetica decimal exacta: `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` de verdad |
| **Alternativas** | **`float`**: `0.1 + 0.2 == 0.30000000000000004`. No es feo, es que **el error se acumula**: un sistema con millones de transacciones descuadra el cierre por centavos que no estan en ninguna parte. **`int` de centavos** (`10050` = $100.50): tecnicamente lo mas robusto y lo que usan Stripe y los bancos, descartado aqui porque obliga a dividir por 100 en cada lectura y a recordar siempre la unidad, ruido que distrae del tema del ejercicio |
| **Impacto** | Hay que escribir `Money("100.50")` con string, no `100.50`. Mas verboso a cambio de exactitud |
| **Futuro** | Migrar a centavos enteros es cambiar **una linea** (el alias), porque el resto del archivo habla de `Money` y no de `Decimal` |

### 2. Cerrar la puerta al `float`

| | |
|---|---|
| **Decision** | `raise InvalidAmount` si el monto que llega es un `float` |
| **Contexto** | Ya elegimos `Decimal`, pero nada impide que alguien pase `10.5` |
| **Razon** | `Decimal(10.5)` produce `Decimal('10.5000000000000000277555756...')`: el error del float entra por la ventana. Elegir el tipo correcto **no alcanza** |
| **Alternativas** | **Confiar en la convencion** ("todos sabemos que va Decimal"): un invariante que depende de que todos se acuerden no es un invariante, es una esperanza. **Convertir el float en silencio**: esconde el problema y lo hace irrastreable |
| **Impacto** | `cuenta.deposit(10.5)` falla con un mensaje que explica que usar en su lugar |
| **Futuro** | Si algun dia se acepta `float` desde una API externa, la conversion se hace **en el borde** (el controller), no dentro del dominio |

### 3. Como falla la clase

| | |
|---|---|
| **Decision** | Lanzar excepciones de una jerarquia propia: `AccountError` -> `InvalidAmount`, `InsufficientFunds`, `OpeningBalanceTooLow` |
| **Contexto** | El enunciado pide "arroje un error". En `bus.py` la misma situacion se resolvio con `return False` |
| **Razon** | La pregunta que decide es **"si el que llama ignora esta respuesta, que tan grave es?"**. Un pasajero fantasma en una lista: molesto. Plata que desaparece sin que nadie se entere: inaceptable. Y la jerarquia permite atrapar fino (`except InsufficientFunds`) o grueso (`except AccountError`) sin listar las hijas |
| **Alternativas** | **`return False`**: silenciable, y en dinero el error silencioso es el peor. **`print`**: acopla la clase a la consola y la vuelve inutil en una API, un test o una app movil. **`assert`**: **`python -O` borra todos los asserts** — las reglas de negocio desaparecerian justo en produccion. **`ValueError` genérico**: el que llama no distingue "monto invalido" de "fondos insuficientes" sin parsear el texto del mensaje, que se rompe si alguien lo traduce |
| **Impacto** | Quien use estas clases tiene que manejar excepciones, no revisar booleanos |
| **Futuro** | `InsufficientFunds` guarda `requested` y `available` como atributos, asi que la capa de arriba puede responder *"te faltan $100"* sin extraer nada de un string |

### 4. Donde vive la comparacion con el minimo

| | |
|---|---|
| **Decision** | El padre **pregunta** `_minimum_balance()` y el hijo **responde**. `withdraw()` se escribe una sola vez |
| **Contexto** | El ejercicio 2 introduce una segunda cuenta con otro minimo. Es la decision mas importante del proyecto |
| **Razon** | `min_balance = 0` y `min_balance = 500` **no son dos reglas**: son la misma con otro numero. Y el hijo **no puede olvidarse de validar**, porque no es el quien valida: solo responde un numero |
| **Alternativas** | **El hijo sobreescribe `withdraw()` completo**: lo mas intuitivo y una trampa — duplica la mecanica, y el dia que se agregue una comision de retiro la cuenta de ahorro queda gratis tres meses hasta que alguien lo note. **`min_balance` como parametro del padre con default 0**: esta cerca de ser bueno, pero le mete al padre un parametro que su enunciado no pidio, y los padres que cargan datos de sus hijos terminan con 12 parametros opcionales |
| **Impacto** | `SavingsAccount` son 6 lineas. Una indireccion de un metodo, barata y con nombre |
| **Futuro** | Una `CheckingAccount` con sobregiro de −200 son 4 lineas y cero cambios en el padre. Y una comision de retiro se agrega en un solo lugar para todas las cuentas |

### 5. Verificar el invariante al nacer

| | |
|---|---|
| **Decision** | El `__init__` usa el **mismo** hook que `withdraw()` en vez de un `balance < 0` escrito a mano |
| **Contexto** | Hay dos puertas parecidas: una cuenta corriente que nace negativa, y una de ahorro que nace bajo su minimo |
| **Razon** | Son la misma regla otra vez. Con el hook, las puertas 1 y 5 se cierran con **un solo `if`** |
| **Alternativas** | **`< 0` en el padre + `< min_balance` en el hijo**: la misma regla escrita dos veces, en dos clases — exactamente el error que el hook existia para evitar. **Dejar pasar la cuenta mal nacida**: un objeto no debe existir en estado invalido; `available` quedaria negativo y todos los retiros fallarian con un mensaje que no explica nada. **Ajustar el balance al minimo en silencio**: inventar plata que nadie deposito |
| **Impacto** | Obliga al hijo a guardar `_min_balance` **antes** de llamar a `super().__init__()` |
| **Futuro** | El refactor desde la version con `< 0` costo **dos lineas**, porque `_minimum_balance()` ya habia aislado el concepto. Eso es lo que significa "escalable": no adivinar el futuro, dejar el cambio barato |

### 6. El borde ambiguo del enunciado

| | |
|---|---|
| **Decision** | Se **permite** retirar hasta quedar exactamente en el minimo |
| **Contexto** | El enunciado dice dos cosas que se contradicen: *"arroje un error si el balance queda **debajo** del min_balance"* y *"se pueden hacer retiros siempre y cuando el balance quede **arriba** del min_balance"*. Con minimo 500 y balance 1000: se puede retirar 500? |
| **Razon** | Quedar en 500 no es quedar **debajo** de 500. La primera frase es la redactada como regla; la segunda es una aclaracion informal |
| **Alternativas** | **Prohibirlo** (`>` estricto): le haria caso a la segunda frase. Igual de defendible. Lo inaceptable es la tercera opcion: **que lo decida el azar de como tipeaste el operador** |
| **Impacto** | Queda documentado en el docstring del modulo y en el README, y verificado en la demo con un caso explicito |
| **Futuro** | En el trabajo real esta frase se le devuelve a quien escribio el requerimiento. En una tarea, se decide y se deja escrito |

### 7. El contrato de `Shape`

| | |
|---|---|
| **Decision** | `ABC` + `@abstractmethod` en los dos metodos |
| **Contexto** | Tres figuras tienen que implementar perimetro y area |
| **Razon** | Olvidarse de un metodo falla **al instanciar**, en el momento mas barato posible. Y el mensaje del `TypeError` nombra los metodos que faltan |
| **Alternativas** | **Duck typing**: no obliga a nada — sirvio bien en `human.py` con `children()` porque las clases eran pocas y propias, pero con tres o mas implementadores el olvido es cuestion de tiempo. **`raise NotImplementedError`**: falla al **llamar**, no al crear, asi que el objeto roto circula y explota lejos de donde lo crearon. **`typing.Protocol`**: tipado estructural que verifica mypy, no el runtime — es la herramienta correcta cuando **no podes tocar** las clases (librerias de terceros) |
| **Impacto** | Una hija incompleta no se puede crear |
| **Futuro** | Agregar un `Triangle` obliga a implementar los dos metodos antes de poder usarlo |

### 8. `Square` hereda de `Shape`, no de `Rectangle`

| | |
|---|---|
| **Decision** | `class Square(Shape)` |
| **Contexto** | Matematicamente un cuadrado **es un** rectangulo, asi que la prueba "ES-UN" diria `Square(Rectangle)` |
| **Razon** | Lo pide el enunciado, y es el ejemplo canonico de violacion del **principio de sustitucion de Liskov**: una funcion `hacer_mas_ancho(rect)` que haga `rect.width *= 2` es valida para cualquier rectangulo, y aplicada a un cuadrado lo deja con lados distintos — un objeto que miente sobre lo que es |
| **Alternativas** | **`Square(Rectangle)`**: reutiliza el calculo del area y del perimetro. *Matiz honesto:* como estas figuras son **inmutables** (no hay setters que romper), aqui **si** seria legitimo. La inmutabilidad hace segura una herencia que de otro modo seria un bug |
| **Impacto** | `Square` repite dos formulas triviales a cambio de no obligar al lector a razonar todo esto |
| **Futuro** | La prueba de Liskov, para cualquier herencia: **"puedo pasarle el hijo a cualquier funcion escrita para el padre sin que nada se rompa?"**. Si la respuesta es no, no es herencia, por mas que "ES-UN" suene bien |

### 9. Mixin o composicion

| | |
|---|---|
| **Decision** | Mixins en el ejemplo, y la version por composicion (`AuditTrail`) incluida al lado |
| **Contexto** | El ejercicio pide un ejemplo de herencia multiple, pero la misma capacidad se puede resolver sin ella |
| **Razon** | **No hay ganador, hay contexto**, y la unica forma de aprender eso es ver las dos. El mixin es **invisible** (se audita solo, imposible de olvidar); la composicion es **explicita** (facil de seguir, facil de olvidar llamarla) |
| **Alternativas** | **Solo el mixin**: cumple el enunciado y esconde que ahi habia una decision. **Solo composicion**: no cumple el enunciado |
| **Impacto** | El archivo es mas largo y contiene una clase que el enunciado no pide |
| **Futuro** | La regla mas citada del diseno OO es **"preferi composicion sobre herencia"**. El mixin se justifica solo cuando la capacidad debe envolver metodos existentes de forma transparente |

### Las otras decisiones, en breve

| Decision | Elegi | Descarte y por que |
|---|---|---|
| Estructura de archivos | carpeta `pilares_oop/`, un archivo por dominio | Todo junto = 3 motivos de cambio en un archivo; plano en `ejercicios_OOP/` = choca con el `circle.py` viejo que ya tiene otro `Circle`; capas tipo `student_control` = sobre-ingenieria sin UI ni base de datos |
| Donde viven las excepciones | dentro de `accounts.py` | Un `errors.py` global obligaria a `shapes.py` a importar conceptos bancarios. Una excepcion pertenece al dominio que la puede lanzar |
| `balance` publico o property | `@property` sin setter | Publico abre la puerta 2. `get_balance()`/`set_balance()` es ruido estilo Java, no idiomatico en Python |
| `min_balance` editable | `@property` de solo lectura | Un setter rompe el invariante al instante (subir el minimo sobre el balance). Si el negocio lo pide va un `change_minimum()` que valide: **el nombre del metodo documenta que hay reglas, el `=` dice que no hay ninguna** |
| Balance inicial | `balance=Money("0")` por default | Sin parametro, abrir con saldo son dos pasos; obligatorio, hay que escribir `0` siempre. El default **declara cual es el caso normal** |
| Tipo en geometria | `float` y `math.pi` | `Decimal` no aporta: una medida es una **medicion** y pi es irracional, el valor exacto no existe ni en teoria. `3.14159` tiene 5 decimales y hay que *reconocerlo*; `math.pi` **se lee** |
| Dimensiones mutables | no, `@property` sin setter | Las dimensiones **son** la identidad: un circulo con otro radio es otro circulo. Inmutable se puede usar como clave de diccionario y compartir entre listas sin miedo |
| Donde validar medidas positivas | `Shape._positive()`, en el padre | Copiada tres veces, el dia que quieras permitir el 0 hay que acordarse de tres lugares |
| Cuantos mixins en el ejemplo | dos | Con uno no se ve lo que importa: que ambos envuelven el mismo metodo, no se conocen entre si, y el MRO los encadena solo |
| `super()` antes o despues de registrar | antes | Si el retiro es rechazado no se registra nada: se audita lo que **paso**, no lo que se intento. Auditar intentos tambien es valido, pero es **otra decision** y se escribe con `try/except` |
| Rama para el commit | `ejercicios-oop` | `past-exercises/ejercicios_OOP/` **no existe en `main`**: vive solo en esta rama (PR #3). Una rama desde `main` crearia el arbol duplicado y chocaria con el PR abierto |

---

## 6. Codigo final

Los tres archivos completos, tal como quedaron en el commit `9da5746`.

### `accounts.py`

```python
"""Ejercicios 1 y 2 — BankAccount y SavingsAccount.

Dominio: dinero.

INVARIANTE (la frase que esta clase nunca deja de cumplir):
    El balance nunca queda por debajo del minimo permitido de la cuenta.
    BankAccount   -> el minimo es 0
    SavingsAccount -> el minimo es su min_balance

Fijate que la frase NO dice "nunca queda negativo". Dice "bajo el minimo
permitido". Esa redaccion es a proposito: el ejercicio 2 se leyo antes de
escribir el ejercicio 1, y asi los dos casos son la misma regla con otro
numero, en vez de dos reglas parecidas escritas en dos clases.

LIMITE: aqui no se imprime ni se pide input (igual que en bus.py). Las clases
aplican reglas y avisan de las violaciones lanzando excepciones. Quien decida
como mostrarselo a un humano es otra capa.

EL BORDE DEL ENUNCIADO: se permite retirar hasta quedar EXACTAMENTE en el
minimo. El enunciado dice "arroje un error si el balance queda DEBAJO del
min_balance", y quedar en 500 no es quedar debajo de 500. (La frase siguiente
dice "siempre y cuando quede ARRIBA", que diria lo contrario; se eligio la
primera porque es la que esta redactada como regla.)
"""

from decimal import Decimal

# Alias semantico: cuando leas Money en una firma sabes que es plata, no un
# numero cualquiera. Si algun dia migras a centavos enteros, cambias esta
# linea y el resto del archivo sigue hablando de Money.
Money = Decimal


# --------------------------------------------------------------------------
# Errores del dominio
# --------------------------------------------------------------------------

class AccountError(Exception):
    """Raiz de todos los errores de cuentas.

    Existe para que quien use estas clases pueda escribir un solo
    `except AccountError` y atrapar cualquier violacion de regla bancaria,
    sin listar las hijas una por una.
    """


class InvalidAmount(AccountError):
    """El monto no es operable: cero, negativo, o un float. (Puertas 4, 6, 7)"""


class InsufficientFunds(AccountError):
    """El retiro dejaria el balance bajo el minimo. (Puerta 3)"""

    def __init__(self, requested: Money, available: Money) -> None:
        super().__init__(f"Retiro de {requested} rechazado: disponible {available}.")
        # Los datos quedan como atributos, no solo dentro del texto: quien
        # atrape el error puede responder con numeros en vez de parsear strings.
        self.requested = requested
        self.available = available


class OpeningBalanceTooLow(AccountError):
    """La cuenta naceria violando su propio minimo. (Puertas 1 y 5)"""

    def __init__(self, balance: Money, minimum: Money) -> None:
        super().__init__(
            f"No se puede abrir la cuenta con {balance}: el minimo es {minimum}."
        )
        self.balance = balance
        self.minimum = minimum


# --------------------------------------------------------------------------
# Ejercicio 1
# --------------------------------------------------------------------------

class BankAccount:
    """Una cuenta cuyo balance solo cambia por deposito o retiro."""

    def __init__(self, owner: str, balance: Money = Money("0")) -> None:
        self.owner = owner
        self._balance = self._as_money(balance)
        # PUERTA 1: nacer violando el invariante. Se verifica con el MISMO
        # minimo que usa withdraw(), no con un 0 escrito a mano: asi la regla
        # vive en un solo lugar y el hijo la hereda gratis (puerta 5).
        minimum = self._minimum_balance()
        if self._balance < minimum:
            raise OpeningBalanceTooLow(self._balance, minimum)

    # ---- consultas -----------------------------------------------------

    @property
    def balance(self) -> Money:
        """PUERTA 2 tapada: se lee, no se escribe.

        No hay setter a proposito. `cuenta.balance = -5000` lanza AttributeError.
        El balance solo cambia pasando por deposit() o withdraw().
        """
        return self._balance

    @property
    def available(self) -> Money:
        """Cuanto se puede retirar sin romper el invariante.

        Es la costura del diseno: el UNICO lugar donde el minimo entra en la
        cuenta. withdraw() no vuelve a mencionarlo nunca.
        """
        return self._balance - self._minimum_balance()

    # ---- operaciones ---------------------------------------------------

    def deposit(self, amount: Money) -> Money:
        """Ingresa dinero. Retorna el balance nuevo."""
        # PUERTA 4 tapada: sin esta validacion, deposit(-500) seria un retiro
        # disfrazado que nunca pasa por el control de fondos de withdraw().
        amount = self._as_positive_money(amount)
        self._balance += amount
        return self._balance

    def withdraw(self, amount: Money) -> Money:
        """Retira dinero. Retorna el balance nuevo.

        PUERTA 3 tapada. Escrito UNA sola vez: las subclases cambian el
        minimo, no este metodo.
        """
        amount = self._as_positive_money(amount)
        if amount > self.available:
            raise InsufficientFunds(requested=amount, available=self.available)
        self._balance -= amount
        return self._balance

    # ---- punto de extension --------------------------------------------

    def _minimum_balance(self) -> Money:
        """Minimo por debajo del cual el balance no puede quedar.

        Es la pregunta que el padre le hace al hijo: "cual es tu minimo?".
        La cuenta base responde 0. Las subclases sobreescriben SOLO esto.
        """
        return Money("0")

    # ---- validacion ----------------------------------------------------

    @staticmethod
    def _as_money(amount) -> Money:
        """PUERTA 7 tapada: convierte a Money y rechaza float.

        float es inservible para dinero: 0.1 + 0.2 == 0.30000000000000004, y
        el error se acumula. Elegir Decimal no alcanza, porque Decimal(10.5)
        ya arrastra la basura del float: hay que rechazarlo en la entrada.
        Es @staticmethod porque es una regla sobre el dato, no sobre la cuenta.
        """
        if isinstance(amount, float):
            raise InvalidAmount(
                f"No uses float para dinero ({amount!r}). "
                f"Usa Money('{amount}') o un entero."
            )
        return Money(amount)

    @classmethod
    def _as_positive_money(cls, amount) -> Money:
        """PUERTAS 4 y 6 tapadas. cls y no BankAccount: si una hija endurece
        _as_money, se usa la de la hija."""
        amount = cls._as_money(amount)
        if amount <= 0:
            raise InvalidAmount(f"El monto debe ser positivo, llego {amount}.")
        return amount

    def __repr__(self) -> str:
        """type(self) y no "BankAccount": una SavingsAccount se nombra sola."""
        return f"{type(self).__name__}(owner={self.owner!r}, balance={self._balance})"


# --------------------------------------------------------------------------
# Ejercicio 2
# --------------------------------------------------------------------------

class SavingsAccount(BankAccount):
    """Cuenta de ahorro: el balance nunca queda bajo su min_balance.

    Mira lo que NO hay aqui: no se reescribe withdraw(), ni deposit(), ni la
    validacion de montos, ni la verificacion al nacer. Solo se responde una
    pregunta distinta. Que el hijo salga trivial es la senal de que el padre
    quedo bien disenado.
    """

    def __init__(
        self,
        owner: str,
        min_balance: Money,
        balance: Money = Money("0"),
    ) -> None:
        min_balance = self._as_money(min_balance)
        if min_balance < 0:
            raise InvalidAmount(f"El minimo no puede ser negativo, llego {min_balance}.")
        # ANTES de super(): el __init__ del padre llama a _minimum_balance(),
        # que lee este atributo. Si inviertes las dos lineas -> AttributeError,
        # y el error aparece en el padre aunque la causa este aqui.
        self._min_balance = min_balance
        super().__init__(owner, balance)

    @property
    def min_balance(self) -> Money:
        """Solo lectura. Un setter abriria una puerta nueva: subir el minimo
        por encima del balance dejaria la cuenta violando su invariante al
        instante. Si el negocio lo necesita, se agrega un change_minimum()
        que valide; el nombre del metodo documenta que hay reglas.
        """
        return self._min_balance

    def _minimum_balance(self) -> Money:
        """La unica linea que esta clase cambia de verdad."""
        return self._min_balance

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(owner={self.owner!r}, "
            f"balance={self._balance}, min_balance={self._min_balance})"
        )


# --------------------------------------------------------------------------
# Demostracion: una seccion por fila de la tabla de trazabilidad del README
# --------------------------------------------------------------------------

def _check(label: str, action) -> None:
    """Corre un ataque y reporta si la puerta estaba tapada."""
    try:
        action()
        print(f"    [ABIERTA] {label}")
    except (AccountError, AttributeError) as error:
        print(f"    [tapada ] {label:<42} {type(error).__name__}")


if __name__ == "__main__":
    print("=== Filas 1, 2, 3: atributo balance, ingresar, retirar ===")
    account = BankAccount("Jordan", Money("100"))
    print(f"    balance inicial         -> {account.balance}")
    print(f"    ingresar 50             -> {account.deposit(Money('50'))}  (espera 150)")
    print(f"    retirar 30              -> {account.withdraw(Money('30'))}  (espera 120)")

    print("\n=== Las 7 puertas del invariante ===")
    _check("1. BankAccount('X', -500)", lambda: BankAccount("X", Money("-500")))
    _check("2. cuenta.balance = -5000", lambda: setattr(account, "balance", Money("-5000")))
    _check("3. retirar 999 teniendo 120", lambda: account.withdraw(Money("999")))
    _check("4. deposit(-500), retiro disfrazado", lambda: account.deposit(Money("-500")))
    _check("5. SavingsAccount(min=500, balance=100)",
           lambda: SavingsAccount("X", Money("500"), Money("100")))
    _check("6. deposit(0)", lambda: account.deposit(Money("0")))
    _check("7. deposit(10.5) como float", lambda: account.deposit(10.5))
    print(f"    el balance no se movio  -> {account.balance}  (sigue en 120)")

    print("\n=== Fila 4: SavingsAccount hereda de BankAccount ===")
    savings = SavingsAccount("Jordan", min_balance=Money("500"), balance=Money("1000"))
    print(f"    isinstance(savings, BankAccount) -> {isinstance(savings, BankAccount)}")
    print("    prueba fuerte: llamar un metodo que SavingsAccount no define")
    print(f"    ingresar 100 (deposit es del padre) -> {savings.deposit(Money('100'))}")
    savings.withdraw(Money("100"))

    print("\n=== Fila 5: min_balance es por instancia, no por clase ===")
    other = SavingsAccount("Ana", min_balance=Money("1000"), balance=Money("1200"))
    print(f"    savings.min_balance={savings.min_balance}  other.min_balance={other.min_balance}")
    print("    (si fueran iguales, min_balance seria atributo de clase: bug)")

    print("\n=== Fila 6: retiro bajo el minimo, y que no deje estado a medias ===")
    before = savings.balance
    try:
        savings.withdraw(Money("600"))
    except InsufficientFunds as error:
        print(f"    retirar 600 -> {type(error).__name__}: {error}")
        print(f"    le faltan {error.requested - error.available} para poder")
    print(f"    balance antes={before}  despues={savings.balance}  (no se descontó nada)")

    print("\n=== Fila 7: retiro sobre el minimo, y el borde exacto ===")
    print(f"    retirar 400 -> {savings.withdraw(Money('400'))}  (queda 600, sobre 500)")
    print(f"    disponible ahora -> {savings.available}")
    print(f"    retirar 100 exactos -> {savings.withdraw(Money('100'))}  (queda 500 = el minimo)")
    print("    el borde: quedar EN el minimo esta permitido. Decision documentada.")

    print("\n=== El pago del diseno: polimorfismo ===")
    for item in (BankAccount("Ana", Money("300")), savings):
        print(f"    {item!r:<76} disponible={item.available}")
```

### `shapes.py`

```python
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
```

### `multiple_inheritance.py`

```python
"""Ejercicio 4 — Herencia multiple: usos, peligros y un ejemplo.

==========================================================================
INVESTIGACION
==========================================================================

Herencia multiple = una clase hereda de DOS o mas padres a la vez:
    class Hija(PadreA, PadreB):

Python la permite. Java y C# NO: solo dejan heredar de una clase e
"implementar" varias interfaces. Esa diferencia no es un descuido — los
disenadores de Java decidieron que el poder no compensaba el riesgo.
Python confia en el programador. Eso te dice cuanto cuidado merece.

--------------------------------------------------------------------------
1. USOS LEGITIMOS
--------------------------------------------------------------------------

a) MIXINS — el 90% de los casos reales.
   Una clase chica que agrega UNA capacidad ortogonal: algo que no tiene
   que ver con lo que la clase ES, sino con algo que ademas sabe hacer.
   Ortogonal = cruzado, independiente. "Ser cuenta de ahorro" y "llevar un
   log de auditoria" son dos ejes que no se tocan: cualquier cuenta podria
   auditarse, y auditarse no la convierte en otro tipo de cuenta.
   Casos reales: serializar a JSON, registrar operaciones, cachear,
   comparar, llevar created_at/updated_at, exportar a CSV.

b) CUMPLIR VARIOS CONTRATOS — varios ABC a la vez.
       class Report(Serializable, Printable, Comparable):
   La clase declara "cumplo estas tres interfaces". Es el equivalente en
   Python de los `implements` de Java.

c) FRAMEWORKS QUE COMPONEN COMPORTAMIENTO.
       Django: class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView)
   El orden de izquierda a derecha define quien interviene primero: es
   herencia multiple usada como pila de middleware. Es la analogia del
   guardia de seguridad en la entrada, pero apilado.

--------------------------------------------------------------------------
2. CUANDO **NO** USARLA
--------------------------------------------------------------------------

- Para reciclar un metodo que no es una capacidad ortogonal. Si solo
  necesitas una funcion de otra clase, eso es COMPOSICION: guarda una
  instancia como atributo.
- Cuando dos padres guardan estado con el mismo nombre: se pisan y el bug
  es invisible.
- Cuando dos padres definen el mismo metodo con semanticas distintas: gana
  el de la izquierda y el otro queda muerto, en silencio.
- Si no podes explicar el MRO de tu clase, no la uses.

--------------------------------------------------------------------------
3. EL PELIGRO: EL DIAMANTE Y EL MRO
--------------------------------------------------------------------------

            Base
           /    \\
        Left    Right        <- las dos heredan de Base
           \\    /
          Diamond            <- hereda de las dos

Si Left y Right definen el mismo metodo, cual corre? Y Base, corre una vez
o dos? A eso se le llama "el problema del diamante".

Python lo resuelve con el MRO (Method Resolution Order): una lista plana y
ordenada de clases, calculada con el algoritmo de linealizacion C3, que
garantiza tres cosas:
  - una clase aparece antes que sus padres,
  - se respeta el orden izquierda->derecha de la declaracion,
  - cada clase aparece UNA sola vez.
Se consulta con  MiClase.__mro__  o  MiClase.mro().

LA IDEA CLAVE, la que cambia todo:

    super() NO significa "mi clase padre".
    super() significa "la siguiente clase en el MRO del OBJETO REAL".

Por eso el super() escrito dentro de Left puede apuntar a Right — que no es
su padre, que Left ni conoce, y que podria no existir cuando Left se
escribio. El MRO lo decide el objeto concreto, no la clase donde esta
escrito el super(). Y por eso los mixins funcionan: cada uno hace lo suyo y
le pasa la pelota al siguiente sin saber quien es.

Si el MRO es imposible de calcular, Python se niega a crear la clase:
    TypeError: Cannot create a consistent method resolution order
"""

from datetime import datetime, timezone

from accounts import InsufficientFunds, Money, SavingsAccount


def _now() -> datetime:
    """UTC siempre. Guardar hora local es un bug esperando un cambio de pais."""
    return datetime.now(timezone.utc)


# ==========================================================================
# PARTE A — El diamante, en 12 lineas
# ==========================================================================
# PREDECI EL RESULTADO DE Diamond().who() ANTES DE CORRER ESTE ARCHIVO.
# Escribilo en papel. Si tu prediccion falla, ahi esta la leccion.

class Base:
    def who(self) -> str:
        return "Base"


class Left(Base):
    def who(self) -> str:
        return f"Left -> {super().who()}"


class Right(Base):
    def who(self) -> str:
        return f"Right -> {super().who()}"


class Diamond(Left, Right):
    """Cuerpo vacio. Todo su comportamiento sale del MRO."""


# ==========================================================================
# PARTE B — El ejemplo real: mixins sobre el dominio de cuentas
# ==========================================================================

class TimestampedMixin:
    """Capacidad ortogonal: saber cuando se creo y cuando cambio.

    Convenciones de un mixin bien hecho:
      - el nombre termina en Mixin: avisa que no se instancia sola,
      - NO hereda de la clase principal: no sabe que existen las cuentas,
      - su __init__ es COOPERATIVO: *args, **kwargs + super(). Recibe lo que
        no entiende y lo pasa intacto al siguiente del MRO. Es el unico
        patron que sobrevive a la herencia multiple,
      - agrega UNA sola capacidad.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        now = _now()
        self.created_at = now
        self.updated_at = now

    def touch(self) -> None:
        self.updated_at = _now()

    def deposit(self, amount):
        result = super().deposit(amount)
        self.touch()
        return result

    def withdraw(self, amount):
        result = super().withdraw(amount)
        self.touch()
        return result


class AuditLogMixin:
    """Capacidad ortogonal: registrar cada operacion de dinero que ocurre.

    Fijate que envuelve los MISMOS metodos que TimestampedMixin y que ninguno
    de los dos sabe del otro. El MRO los encadena solo.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.audit_log: list[dict] = []

    def deposit(self, amount):
        # super() va ANTES del registro a proposito: si lanza excepcion, no se
        # registra nada. Se audita lo que PASO, no lo que se intento.
        # (Auditar los intentos tambien es valido, pero es otra decision y se
        #  escribe con try/except. Lo importante es elegirla, no heredarla.)
        new_balance = super().deposit(amount)
        self._record("deposit", amount, new_balance)
        return new_balance

    def withdraw(self, amount):
        new_balance = super().withdraw(amount)
        self._record("withdraw", amount, new_balance)
        return new_balance

    def _record(self, action: str, amount, balance) -> None:
        self.audit_log.append(
            {"at": _now(), "action": action, "amount": amount, "balance": balance}
        )


class AuditedSavingsAccount(AuditLogMixin, TimestampedMixin, SavingsAccount):
    """Cuenta de ahorro auditada y con marcas de tiempo.

    El cuerpo esta VACIO a proposito: no hay una sola linea de logica propia.
    Todo su comportamiento es la suma de tres piezas escritas por separado
    que no se conocen entre si.

    POR QUE LOS MIXINS VAN A LA IZQUIERDA Y LA CLASE BASE A LA DERECHA:
    el MRO se recorre de izquierda a derecha, asi que los mixins interceptan
    ANTES de que la cuenta real haga el trabajo.

    Si escribieras (SavingsAccount, AuditLogMixin, TimestampedMixin) el MRO
    seria:
        Roto -> SavingsAccount -> BankAccount -> AuditLogMixin
             -> TimestampedMixin -> object

    y pasan DOS cosas, las dos silenciosas:

    1. Los __init__ de los mixins nunca corren. SavingsAccount.__init__ llama
       a super().__init__(), que es BankAccount.__init__, que NO llama a
       super().__init__() porque es la base de su propia jerarquia. Ahi la
       cadena se corta: self.audit_log y self.created_at nunca se crean.

    2. deposit() y withdraw() se resuelven en BankAccount, que aparece ANTES
       que los mixins en el MRO. Los metodos de los mixins nunca se llaman.

    Y aqui esta lo peligroso: NO EXPLOTA. La cuenta funciona perfecto, los
    depositos se acreditan, el invariante se respeta... y la auditoria no
    existe. Los mixins quedan INERTES, sin un solo mensaje de error. Es el
    "bug invisible" de la seccion 2 de la investigacion, en vivo.

    Un error que explota lo arreglas en 5 minutos. Uno que calla puede vivir
    meses en produccion. Por eso el orden no es un detalle de estilo.
    """


# ==========================================================================
# PARTE C — La alternativa: composicion
# ==========================================================================

class AuditTrail:
    """La MISMA capacidad, sin herencia: un objeto que se guarda y se usa.

    LA BISAGRA entre las dos opciones:
        el mixin es INVISIBLE para quien usa la clase (se audita solo);
        la composicion es EXPLICITA (hay que acordarse de llamarla).
    Invisible es comodo y es mas facil de olvidar que existe.
    Explicito es mas verboso y mas facil de seguir.
    No hay ganador: hay contexto.

    Preferi composicion si:
      - queres compartir un mismo log entre varias cuentas,
      - el log necesita configuracion propia (destino, formato, nivel),
      - queres poder apagarlo o cambiarlo en caliente,
      - no queres que la jerarquia de la cuenta crezca.
    Preferi el mixin si:
      - la capacidad debe envolver metodos existentes de forma transparente,
        sin que quien usa la clase tenga que acordarse de nada.
    """

    def __init__(self) -> None:
        self.entries: list[dict] = []

    def record(self, action: str, amount, balance) -> None:
        self.entries.append(
            {"at": _now(), "action": action, "amount": amount, "balance": balance}
        )


# ==========================================================================
# Demostracion
# ==========================================================================

if __name__ == "__main__":
    print("=== A. El diamante: super() no es 'mi padre' ===")
    print("    (si no predijiste el resultado todavia, no sigas leyendo)\n")
    print(f"    Diamond().who() = {Diamond().who()!r}")
    print("    Left llamo a Right, que NO es su padre y que Left ni conoce.")
    print("\n    MRO de Diamond:")
    for position, klass in enumerate(Diamond.__mro__):
        print(f"      {position}. {klass.__name__}")
    print("    Base aparece UNA vez, al final: el diamante no la duplica.")

    print("\n=== B. Fila 12: mixins, tres piezas y cero logica propia ===")
    account = AuditedSavingsAccount(
        "Jordan", min_balance=Money("500"), balance=Money("1000")
    )
    print(f"    {account!r}")
    print("\n    MRO:")
    print("      " + "\n      -> ".join(k.__name__ for k in AuditedSavingsAccount.__mro__))

    account.deposit(Money("250"))
    account.withdraw(Money("300"))

    print("\n    el invariante de la cuenta SIGUE VIGENTE con los mixins puestos:")
    try:
        account.withdraw(Money("600"))        # dejaria 450 < 500
    except InsufficientFunds as error:
        print(f"      retirar 600 -> {type(error).__name__}: {error}")

    print(f"\n    balance final : {account.balance}")
    print(f"    creada        : {account.created_at:%H:%M:%S} UTC")
    print(f"    ultimo cambio : {account.updated_at:%H:%M:%S} UTC")
    print(f"    log ({len(account.audit_log)} entradas; el retiro rechazado NO esta):")
    for entry in account.audit_log:
        print(
            f"      {entry['at']:%H:%M:%S}  {entry['action']:<9}"
            f" {entry['amount']:>6}  -> balance {entry['balance']}"
        )

    print("\n=== El orden importa, y el modo de fallar es lo peligroso ===")

    class Roto(SavingsAccount, AuditLogMixin, TimestampedMixin):
        """El mismo combo con la clase base primero. Los mixins quedan inertes."""

    print("    MRO de Roto (mira donde cae BankAccount):")
    print("      " + " -> ".join(k.__name__ for k in Roto.__mro__))

    broken = Roto("X", min_balance=Money("100"), balance=Money("500"))
    print(f"\n    tiene audit_log?  {hasattr(broken, 'audit_log')}")
    print(f"    tiene created_at? {hasattr(broken, 'created_at')}")

    broken.deposit(Money("50"))
    print(f"    deposit(50) -> balance {broken.balance}  SIN ERROR")
    print("    la cuenta funciona, el invariante se respeta... y no auditó nada.")
    print("    Los mixins quedan INERTES: deposit() se resolvio en BankAccount,")
    print("    que aparece antes que ellos en el MRO.")

    try:
        broken.audit_log
    except AttributeError as error:
        print(f"\n    recien al PEDIR el log aparece el error: {error}")
    print("    Un error que explota se arregla en 5 minutos.")
    print("    Uno que calla vive meses en produccion. Por eso el orden importa.")

    print("\n=== C. La misma capacidad por composicion ===")
    trail = AuditTrail()
    plain = SavingsAccount("Ana", min_balance=Money("100"), balance=Money("500"))
    plain.deposit(Money("200"))
    trail.record("deposit", Money("200"), plain.balance)   # hay que acordarse
    print(f"    {len(trail.entries)} entrada, registrada a mano:")
    entry = trail.entries[0]
    print(f"      {entry['at']:%H:%M:%S}  {entry['action']} {entry['amount']}"
          f" -> balance {entry['balance']}")
    print("    Mas explicito, mas facil de olvidar llamarlo. Esa es la bisagra.")
```

---

## 7. El metodo

Esta es la seccion que importa dentro de seis meses. El codigo envejece; esto no.

### Las 5 preguntas, antes de escribir una linea

```
1. ESTADO     ¿Que datos viven en el tiempo?    → atributos
2. ACCIONES   ¿Que los cambia?                  → metodos
3. INVARIANTE ¿Que NUNCA puede ser falso?       → la clave
4. LIMITE     ¿Que NO es asunto de esta clase?  → el borde
5. MANANA     ¿Que va a cambiar?                → la costura
```

La 3 es la que separa a un junior de un senior, y casi nadie la ensena.

Contestadas para `BankAccount`:

1. `balance` (cambia siempre) y `owner` (no lo pedia el enunciado).
2. Ingresar y retirar. Mas dos consultas que aparecieron solas: leer el
   balance y saber cuanto se puede retirar.
3. *"El balance nunca queda por debajo del **minimo permitido** de la
   cuenta."* — no "nunca queda negativo". La redaccion es deliberada.
4. No imprime, no pide input, no sabe de CSV ni de base de datos. Avisa con
   excepciones y otra capa decide que mostrarle al humano.
5. Viene `SavingsAccount` con otro minimo. **Lo que varia es el numero, no la
   mecanica del retiro.**

### El metodo de las puertas: atacar antes de defender

Despues de escribir el invariante, **pensar como el que quiere romperlo**. Hay
tres formas de llegar a cualquier dato: **al nacer**, **asignando directo** y
**operando**. Por cada una, escribir la linea de codigo del ataque.

Resultado en este proyecto:

| | Puertas encontradas | Las que el enunciado nombraba |
|---|---|---|
| `accounts.py` | 7 | 1 |
| `shapes.py` | 7 | 0 |

La mejor de las 14 fue `cuenta.deposit(-500)`: **un deposito negativo es un
retiro disfrazado** que entra por la puerta del deposito y nunca pasa por el
control de fondos. Tapar `withdraw` y dejar `deposit` sin validar es poner el
guardia en la puerta principal y dejar abierto el porton de los camiones.

Un detalle del metodo: las puertas de un objeto **con estado que muta** (una
cuenta) estan en las operaciones; las de un objeto **de valor inmutable** (una
figura) estan casi todas en el constructor, porque despues de construido no
hay nada que atacar. **La naturaleza del objeto te dice donde buscar.**

### Las 13 reglas de criterio

1. **Lee el enunciado completo antes de la primera clase.** El diseno del
   padre lo decide el hijo.
2. **Un default no es comodidad: es una declaracion de cual es el caso
   normal.** Fijate si estas diciendo la verdad.
3. **Elegir el tipo correcto no alcanza: hace imposible el incorrecto.** Un
   invariante que depende de que todos recuerden la convencion no es un
   invariante, es una esperanza.
4. **Sobre-ingenieria** = construir un punto de extension para una variacion
   **imaginaria**. **Diseno** = para una **ya conocida**. Extende por lo que
   ya sabes que viene, nunca por lo que podria venir.
5. **Escalable no es adivinar el futuro: es dejar el cambio barato.**
6. **El unico test de diseno que importa: que el hijo salga trivial.**
7. Si el `__init__` del padre llama a un metodo que el hijo sobreescribe, **el
   hijo tiene que estar completo antes de `super()`**. El error aparece en el
   padre y la causa esta en el hijo.
8. **Entre un setter y un metodo con nombre, elegi el metodo.**
   `change_minimum()` dice que hay reglas; `min_balance = x` dice que no hay
   ninguna.
9. **El tipo correcto lo dicta el dominio, no tu preferencia.** La pregunta no
   es "cual es mas preciso" sino **"esto se cuenta o se mide?"**.
10. **Todo enunciado tiene un borde ambiguo.** Encontralo antes de codificar,
    decidi a proposito, y deja la decision escrita. La diferencia no es
    acertar el borde: es **saber que lo decidiste**.
11. **Separa lo pedido de lo agregado.** Si no podes senalar la linea exacta
    que cumple cada requisito, quien revisa no puede distinguir si entendiste
    o si pegaste algo grande.
12. **"Lo razone y tiene sentido" no es verificacion.** Correlo.
13. **El modo de fallar importa mas que el hecho de fallar.** No preguntes
    solo "puede romperse?" — pregunta **"como se va a enterar alguien?"**. Un
    error que explota se arregla en 5 minutos; uno que calla vive meses.

Las 12 y 13 no salieron de la teoria: salieron de dos errores concretos de
esta sesion, documentados en la seccion 4.

### El orden que funciono

```
leer los 4 enunciados completos
        ↓
las 5 preguntas, en papel, sin codigo
        ↓
la lista de puertas (atacar la clase antes de escribirla)
        ↓
la tabla de trazabilidad: requisito → como lo verifico
   (la columna "como lo verifico" se llena ANTES de codificar:
    si no sabes como comprobarlo, todavia no entendiste el requisito)
        ↓
el codigo (que ya sale solo, porque sabes que tiene que defender)
        ↓
correr y verificar, no deducir
        ↓
documentar las decisiones con sus alternativas descartadas
```

### La cuenta final

Las 9 vinetas del enunciado se cumplen con unas **60 lineas**. El archivo
tiene **842**. Las otras 780 son la respuesta a una pregunta que el enunciado
nunca hace: **"de cuantas formas distintas puede alguien romper esto?"**.

Eso es, en concreto, la diferencia entre construir y tener criterio.

---

## 8. Comandos usados

| Comando | Que hace | Por que se uso |
|---------|----------|----------------|
| `mkdir -p pilares_oop` | crea la carpeta, sin error si ya existe | `-p` hace el comando **idempotente**: se puede repetir sin romper nada |
| `touch pilares_oop/{accounts.py,shapes.py,multiple_inheritance.py,README.md}` | crea los 4 archivos vacios de una vez | la expansion de llaves de zsh evita escribir la ruta 4 veces |
| `python3 accounts.py` | corre el archivo, incluido su bloque `if __name__ == "__main__"` | ese bloque **es** la demostracion: cada seccion del output corresponde a una fila de la tabla de trazabilidad |
| script de verificacion aparte | vuelve a probar los 12 requisitos sin usar las demos | una demo que se escribio junto con el codigo puede estar de acuerdo con el bug. Verificar **independientemente** es otra cosa |
| `git status --short` | estado compacto del repo | antes de cada commit, para ver exactamente que va a entrar |
| `git add -An <carpeta>` | simula el `add` sin hacerlo (`-n` = dry run) | confirmar que el `.gitignore` filtra `__pycache__` **antes** de agregar nada |
| `git ls-tree --name-only main past-exercises/` | lista lo que existe en `main` sin cambiar de rama | asi se descubrio que `ejercicios_OOP/` no esta en `main`, y por eso el commit va en `ejercicios-oop` |
| `git log --oneline main..ejercicios-oop` | los commits de la rama que no estan en main | ver que contiene el PR #3 antes de agregarle algo |
| `git commit -F archivo.txt` | toma el mensaje de un archivo | evita pegar 20 lineas en zsh, que es donde el *bracketed paste* (`^[[200~`) rompe |
| `git push` | sin argumentos | la rama ya tenia upstream (`origin/ejercicios-oop`), y el push **actualiza el PR #3 solo** |
| `grep -nE '^\| [0-9]+ \|.*\| \| \|' README.md` | busca filas de la tabla con celdas vacias | verificar el **resultado** del script que lleno la tabla, no su intencion |

---

## 9. Pendientes

- [ ] **Predecir `Diamond().who()` en papel antes de correr
      `multiple_inheritance.py`.** Es el unico ejercicio que no se puede
      delegar: si la prediccion falla, ahi esta la leccion. La pregunta a
      contestar despues: *a quien apunta el `super()` escrito dentro de
      `Left`?* (No es "a su padre".)
- [ ] Decidir si `BankAccount.__init__` debe llamar a `super().__init__()`.
      Hoy no lo hace y no pasa nada porque es la base de su jerarquia — pero
      **por eso mismo** los mixins tienen que ir a la izquierda. Las dos
      respuestas son defendibles: agregarlo vuelve la clase segura en
      cualquier posicion del MRO; no agregarlo evita un `super()` que solo
      llama a `object.__init__()`.
- [ ] `change_minimum()` en `SavingsAccount`: justificado en el docstring,
      no implementado porque el enunciado no lo pide.
- [ ] Tests con `pytest`. Las demos cumplen la funcion de verificacion, pero
      en un proyecto real irian aparte del codigo que prueban.
- [ ] Actualizar el titulo y la descripcion del PR #3: ya contiene mas que
      "Circle, Student_control_2, Bus y Human".
- [ ] Heredados de `2026-10-04-practica-oop.md`: `count_parts()` en
      `human.py`, y los pasos 8 (herencia con `BodyPart`) y 9 (export a JSON).

---

## 10. Repaso de 10 minutos

Las 5 ideas, si no se lee nada mas:

1. **El invariante y sus puertas.** Escribi la frase que siempre tiene que ser
   verdad, y despues **ataca tu propia clase**: por cada dato hay tres vias
   (nacer, asignar, operar). En este proyecto el enunciado nombraba 1 puerta
   de 14. El junior tapa la que le dicen; el senior enumera primero.

2. **El diseno del padre lo decide el hijo.** Lee el enunciado completo antes
   de la primera clase. `min_balance = 0` y `min_balance = 500` no son dos
   reglas: son la misma con otro numero. Si el hijo necesita reescribir el
   metodo del padre, el padre esta mal — **el unico test de diseno que
   importa es que el hijo salga trivial**.

3. **Elegir el tipo correcto no alcanza: hace imposible el incorrecto.**
   Elegir `Decimal` y dejar pasar un `float` es poner un candado y dejar la
   ventana abierta. Y el tipo lo dicta el dominio: *se cuenta o se mide?*

4. **Extende por lo que ya sabes que viene, nunca por lo que podria venir.**
   Eso separa el diseno de la sobre-ingenieria. Y escalable no es adivinar el
   futuro: es **dejar el cambio barato** (el refactor del constructor costo 2
   lineas porque el hook ya habia aislado el concepto).

5. **Verifica, no deduzcas — y mira el modo de fallar.** Mi prediccion sobre
   el orden de los mixins era razonada y era falsa: invertirlo no lanza error,
   **deja los mixins inertes en silencio**. Un error que explota se arregla en
   5 minutos; uno que calla vive meses en produccion.

> **La analogia, en una linea:** el que construye escribe el cajero; el que
> tiene criterio escribe el reglamento, y despues el cajero sale solo.
