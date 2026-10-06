# Cree una clase de Circle con:
#  Un atributo de radius (radio).
#. Un método de get_area que retorne su área.


class Circle:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def get_area(self):
        return 3.14159 * self.radius ** 2




circle_1 = Circle(5,"red")
print(circle_1.color)
print(circle_1.radius)
print(circle_1.get_area(), circle_1.color, circle_1.radius) 



circle_2 = Circle(12,"blue")
radius_2 = circle_2.radius
area_2 = circle_2.get_area()
print(f"The Circle_2 is color {circle_2.color}, with radius {radius_2} has an area of {area_2}.")

