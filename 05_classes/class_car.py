class Car:
    def __init__(self, brand):
        self.brand = brand
        self.speed = 0

    def accelerate(self):
        self.speed += 10

    def brake(self):
        self.speed -= 5


car = Car("Toyota")

car.accelerate()
car.accelerate()
car.brake()

print(car.speed)  # 15



