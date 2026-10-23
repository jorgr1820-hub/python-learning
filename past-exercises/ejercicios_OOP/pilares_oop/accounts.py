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
