# Pilares de OOP — los 4 ejercicios

| Archivo | Ejercicios | Dominio | Estado |
|---|---|---|---|
| `accounts.py` | 1 y 2 — `BankAccount`, `SavingsAccount` | dinero | ✅ |
| `shapes.py` | 3 — `Shape` abstracta, `Circle`, `Square`, `Rectangle` | geometría | ✅ |
| `multiple_inheritance.py` | 4 — investigación de herencia múltiple + ejemplo | mixto | ✅ |

---

## Trazabilidad: enunciado → código

En **Dónde** va el nombre (`BankAccount.deposit()`), nunca el número de línea: el nombre no se mueve.

| # | El enunciado pide | Archivo | Dónde | Cómo lo verifico |
|---|---|---|---|---|
| 1 | `BankAccount` tiene un atributo `balance` | `accounts.py` | `BankAccount.balance` (property) | Crear una cuenta con 100 y leer el atributo → devuelve 100, sin error. |
| 2 | `BankAccount` tiene un método para ingresar dinero | `accounts.py` | `BankAccount.deposit()` | Cuenta con 100 → ingresar 50 → el balance queda en **150**. |
| 3 | `BankAccount` tiene un método para retirar dinero | `accounts.py` | `BankAccount.withdraw()` | Cuenta con 100 → retirar 30 → el balance queda en **120**. |
| 4 | `SavingsAccount` hereda de `BankAccount` | `accounts.py` | `class SavingsAccount(BankAccount)` | Sobre una `SavingsAccount`, llamar `deposit()` —que ella no define— y que funcione → prueba que lo heredó, no solo que declaró un padre. Y `isinstance(savings, BankAccount)` → `True`. |
| 5 | `SavingsAccount` tiene `min_balance`, asignable al crearla | `accounts.py` | `SavingsAccount.__init__()` + `.min_balance` | Crear con mínimo 500 y leerlo → 500. Después **dos** cuentas con mínimos distintos (500 y 1000) y que cada una conserve el suyo → prueba que es atributo de instancia y no de clase. |
| 6 | Retirar dejando el balance bajo `min_balance` arroja error | `accounts.py` | `BankAccount.withdraw()` + `SavingsAccount._minimum_balance()` | Mínimo 500, balance 1000 → retirar 600 → **`InsufficientFunds`**. Y el balance **sigue en 1000**: una operación rechazada no deja estado a medias. |
| 7 | Retirar dejando el balance sobre `min_balance` sí funciona | `accounts.py` | `BankAccount.available` | Mínimo 500, balance 1000 → retirar 400 → funciona, queda 600. **El borde:** retirar 100 más deja el balance en 500 exactos y **se permite** (ver decisión del borde). |
| 8 | `Shape` es una clase abstracta | `shapes.py` | `class Shape(ABC)` | Instanciar `Shape()` directo → **`TypeError`**. Y una hija que implemente solo uno de los dos métodos → **`TypeError` al instanciarla**, no al llamarla. |
| 9 | `Shape` tiene `calculate_perimeter` y `calculate_area` abstractos | `shapes.py` | `@abstractmethod` en ambos | El mensaje del `TypeError` de la fila 8 **nombra los métodos que faltan**. |
| 10 | `Circle`, `Square` y `Rectangle` heredan de `Shape` | `shapes.py` | `class Circle(Shape)`, `Square(Shape)`, `Rectangle(Shape)` | `isinstance(figura, Shape)` → `True` para las tres. Y recorrer las tres en **un solo bucle**, **sin un `if`**. |
| 11 | Las tres implementan los dos métodos y calculan bien | `shapes.py` | `.calculate_perimeter()` / `.calculate_area()` de cada una | Valores a mano: `Square(4)` → **16** y **16**. `Rectangle(3, 7)` → **20** y **21**. `Circle(5)` → **31.42** y **78.54**. |
| 12 | Investigación de usos de herencia múltiple + un ejemplo | `multiple_inheritance.py` | docstring del módulo + `AuditedSavingsAccount` | Las 3 secciones (usos legítimos / cuándo no / el peligro). El ejemplo corre, se imprime su `__mro__`, y la clase combinada **sigue respetando el `min_balance`**. |

---

## El invariante y sus 7 puertas

> **"El balance nunca queda por debajo del mínimo permitido de esta cuenta."**

La frase no dice "nunca queda negativo". Dice "bajo el mínimo permitido", y eso es
deliberado: el ejercicio 2 se leyó **antes** de escribir el 1, así que los dos casos
son la misma regla con otro número en vez de dos reglas parecidas en dos clases.

El enunciado menciona **una** puerta (la 3). Las otras seis aparecen solo si te
sentás a atacar tu propia clase a propósito.

| # | El ataque | Dónde quedó tapada |
|---|---|---|
| 1 | `BankAccount("X", -500)` → nace violándolo | `__init__` → `OpeningBalanceTooLow` |
| 2 | `cuenta.balance = -5000` → asignación directa | `@property` sin setter → `AttributeError` |
| 3 | `cuenta.withdraw(999)` teniendo 120 | `withdraw()` → `InsufficientFunds` |
| 4 | `cuenta.deposit(-500)` → **retiro disfrazado** que no pasa por el control de fondos | `_as_positive_money()` → `InvalidAmount` |
| 5 | `SavingsAccount(min=500, balance=100)` → el hijo nace violándolo | el mismo `__init__` del padre, usando el hook |
| 6 | `cuenta.deposit(0)` → operación sin sentido | `_as_positive_money()` → `InvalidAmount` |
| 7 | `cuenta.deposit(10.5)` → lo rompe **de a centavos** en el cierre de mes | `_as_money()` → `InvalidAmount` |

La **4** es la que más enseña: tapar `withdraw` y dejar `deposit` sin validar es poner
el guardia en la puerta principal y dejar abierto el portón de los camiones.

---

## Decisiones y alternativas descartadas

| Decisión | Elegí | Descarté y por qué |
|---|---|---|
| ¿`balance` público o propiedad de solo lectura? | `@property` sin setter | Público abre la puerta 2: `cuenta.balance = -5000` se saltea toda la validación. |
| ¿Con qué tipo guardo la plata? | `Decimal` (alias `Money`) | `float` acumula error (`0.1+0.2 = 0.3000…4`) y descuadra cierres; `int` de centavos es lo más robusto (lo usa Stripe) pero obliga a dividir por 100 en cada lectura. |
| ¿Alcanza con elegir `Decimal`? | No: rechazo `float` en la entrada | `Decimal(10.5)` ya arrastra la basura del float. Elegir el tipo correcto no sirve si no hacés imposible el incorrecto. |
| ¿Cómo aviso que el retiro no se puede? | `raise` | `return False` es silenciable y en dinero un error silencioso es el peor; `print` acopla la clase a la consola e inutiliza su uso en API o test; `assert` **lo borra `python -O`**. |
| ¿Excepción propia o de Python? | jerarquía propia bajo `AccountError` | Con `ValueError` el que llama no puede distinguir "monto inválido" de "fondos insuficientes" sin parsear el texto del mensaje. |
| ¿La cuenta nace en 0 o con depósito inicial? | `balance=Money("0")` por default | Sin parámetro, abrir con saldo son dos pasos; obligatorio, hay que escribir `0` siempre. El default declara cuál es el caso normal. |
| **El borde:** ¿se puede retirar hasta quedar *exactamente* en `min_balance`? | **Sí, se permite** | El enunciado dice "error si queda **debajo** del mínimo", y quedar en 500 no es quedar debajo de 500. La frase siguiente ("siempre y cuando quede **arriba**") diría lo contrario; se eligió la primera porque es la que está redactada como regla. |
| ¿Dónde vive la comparación con el mínimo? | el padre **pregunta** `_minimum_balance()`, el hijo **responde** | Si el hijo sobreescribe `withdraw()` completo, duplica la mecánica: el día que agregues una comisión de retiro, la cuenta de ahorro queda gratis hasta que alguien lo note. |
| ¿Qué pasa si una `SavingsAccount` nace bajo su mínimo? | `raise OpeningBalanceTooLow` | Dejarla pasar crea un objeto que existe en estado inválido; ajustar el balance en silencio al mínimo es inventar plata que nadie depositó. |
| ¿`min_balance` editable después de crear la cuenta? | `@property` de solo lectura | Un setter abre una puerta nueva: subir el mínimo sobre el balance rompe el invariante al instante. Si el negocio lo pide, va un `change_minimum()` que valide — el nombre documenta que hay reglas. |
| ¿Verificar el invariante al nacer con `< 0` o con el hook? | con el hook | `< 0` en el padre más `< min_balance` en el hijo es la misma regla escrita dos veces. Con el hook, las puertas 1 y 5 se cierran con un solo `if`. |
| ¿`float` o tipo exacto para las figuras? | `float` | `Decimal` no aporta nada: una medida es una **medición**, no un conteo, y π es irracional — el valor exacto no existe ni en teoría. El tipo lo dicta el dominio, no la preferencia. |
| ¿`3.14159` o `math.pi`? | `math.pi` | La constante a mano tiene 5 decimales y hay que *reconocerla*; `math.pi` tiene toda la precisión del hardware y **se lee**. |
| ¿`Square` hereda de `Shape` o de `Rectangle`? | `Shape` | Lo pide el enunciado, y `Square(Rectangle)` es el ejemplo canónico de violación de Liskov: una función `hacer_mas_ancho(rect)` escrita para rectángulos dejaría al cuadrado con lados distintos. *Matiz:* como estas figuras son inmutables, `Square(Rectangle)` sería legítimo aquí — la inmutabilidad hace segura una herencia que de otro modo sería un bug. |
| ¿Las dimensiones se pueden cambiar después de crear la figura? | no, `@property` sin setter | Las dimensiones **son** la identidad: un círculo con otro radio es otro círculo. Y una figura inmutable se puede usar como clave de diccionario y compartir entre listas sin miedo. |
| ¿Dónde vive la validación de medida positiva? | `Shape._positive()`, en el padre | Copiada tres veces, el día que quieras permitir el 0 hay que acordarse de tres lugares. |
| ¿Qué capacidad ortogonal usé para el ejemplo de herencia múltiple? | dos: log de auditoría y marcas de tiempo | Con **dos** mixins se ve lo que con uno no: que ambos envuelven el mismo método, no se conocen entre sí, y el MRO los encadena solo. |
| ¿Mixin o composición para auditar? | mixin en el ejemplo, composición incluida al lado (`AuditTrail`) | No hay ganador. El mixin es **invisible** (se audita solo, imposible de olvidar); la composición es **explícita** (fácil de seguir, fácil de olvidar llamarla). Van las dos para poder comparar. |
| ¿Auditar lo que pasó o lo que se intentó? | lo que pasó (`super()` antes del registro) | Si el retiro es rechazado no se registra nada. Auditar los intentos también es válido, pero es otra decisión y se escribe con `try/except` — lo importante es elegirla, no heredarla por accidente. |

---

## Lo agregado (no estaba en el enunciado)

| Qué agregué | Por qué |
|---|---|
| `owner` | Sin dueño, un mensaje de error no sirve: "retiro rechazado" ¿de cuál cuenta? |
| `available` | Un menú necesita mostrar "disponible para retiro: $X" **sin saber si la cuenta tiene mínimo**. Y de paso es la costura que hace que `withdraw()` no mencione el mínimo nunca. |
| `_minimum_balance()` | El punto de extensión que hace trivial el ejercicio 2. No es especulación: el enunciado ya nombró la segunda cuenta. |
| jerarquía de excepciones | Para distinguir el tipo de violación sin parsear mensajes. |
| validación en `__init__` | Puertas 1 y 5, que el enunciado no menciona. |
| `__repr__` | Para que un error a las 2am diga **cuál** cuenta era, no `<object at 0x104f2b3d0>`. |
| rechazo explícito de `float` | Puerta 7: la que rompe el invariante de a centavos. |
| `Shape.describe()` | Método concreto en la clase abstracta: se escribe una vez y lo tienen las tres figuras y las que se agreguen después. |
| `AuditTrail` (composición) | No lo pide el enunciado. Está para poder comparar mixin vs. composición lado a lado, que es la decisión real detrás del ejercicio 4. |
| la clase `Roto` en la demo | Demuestra el modo de fallar del orden invertido, que es silencioso. Vale más que la explicación. |

---

## Cómo correr

```bash
python3 accounts.py
python3 shapes.py                 # pendiente
python3 multiple_inheritance.py   # pendiente
```
