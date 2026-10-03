# This is the real version 

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
    # This is the entry point to the body. It knows the path to each part.


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


# Constructing the human body
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

