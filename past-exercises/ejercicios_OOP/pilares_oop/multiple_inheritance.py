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
