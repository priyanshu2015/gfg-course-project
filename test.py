from abc import ABC, abstractmethod

def func():
    print("hello")


class TypeChoice:
    SUV = "SUV"
    SEDAN = "SEDAN"
    HATCHBACK = "HATCHBACK"


class Car(ABC):
    # encapsulation
    # public class variable
    type = None
    # protected variable
    _brand = None
    # private
    __type_choice_list = [TypeChoice.SUV, TypeChoice.SEDAN, TypeChoice.HATCHBACK]

    def __init__(self, type):
        if type not in self.__type_choice_list:
            raise Exception
        self.type = type

    @abstractmethod
    def get_brand(self):
        # raise NotImplementedError
        pass

    def describe(self):
        print("I am an instance of class Car")


class BMW(Car):
    def __init__(self, type):
        self.type = type
        self._brand = "BMW"

    def describe(self):
        print("I am an instance of class BMW")
        super().describe()

    # method overriding
    def get_brand(self):
        return self._brand


class Mercedes(Car):
    def __init__(self, type):
        self.type = type
        self._brand = "Mercedes"

    # method overriding
    def get_brand(self):
        return self._brand

    def describe(self):
        print("I am an instance of class Mercedes")
        super().describe()


class Random(BMW, Mercedes):
    pass


#c = Car("SUV")
b = BMW("SUV")
m = Mercedes("SUV")
print(b.get_brand())
print(m.get_brand())
b.describe()

r = Random("SUV")
r.describe()


def add(x, y, z=0):
    print(x + y + z)


add(2, 3)
add(2, 3, 5)