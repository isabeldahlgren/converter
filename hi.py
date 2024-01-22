
class Car:

    def __init__(self, brand) -> None:
        self.brand = brand

    def get_brand(self):
        return self.brand

putte = Car('BMW')
putte.brand = 'Mercedes'
print(putte.brand)
