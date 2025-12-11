
#Better than Car Record clean and contains neccesary functions. evritying else is hndeled in the car records

class Engine:
    def __init__(self, volume, turbo):
        self.volume = volume   # float or None
        self.turbo = turbo     # bool or None

    def __repr__(self):
        return f"Engine(volume={self.volume}, turbo={self.turbo})"

#Better than Car Record clean and contains neccesary functions. evritying else is hndeled in the car records

class Car:
    def __init__(
        self, ID, price, levy, manufacturer, model, prod_year,
        category, leather_interior, fuel_type, mileage, cylinders,
        gear_box_type, drive_wheels, doors, right_wheel, color, airbags,
        engine: Engine
    ):
        self.ID = ID
        self.price = price
        self.levy = levy
        self.manufacturer = manufacturer
        self.model = model
        self.prod_year = prod_year
        self.category = category
        self.leather_interior = leather_interior
        self.fuel_type = fuel_type
        self.mileage = mileage
        self.cylinders = cylinders
        self.gear_box_type = gear_box_type
        self.drive_wheels = drive_wheels
        self.doors = doors
        self.right_wheel = right_wheel
        self.color = color
        self.airbags = airbags
        self.engine = engine

    def __repr__(self):
        return f"Car(ID={self.ID}, model={self.model}, Price={self.price})"