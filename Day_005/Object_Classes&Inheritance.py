#Morning excercise drill warmup
class Animal:
    def __init__(self,name):
        self.name=name
    def behaviour(self):
        print(f"{self.name} is an annimal having the ability to make sounds")
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name) ##use of super here to avoid overridding of parent class
    def speak(self):
        print(f"{self.name} is Barking -->")
class Cat(Animal):
    def __init__(self, name):
        super().__init__(name)
    def speak(self):
        print(f"{self.name} Mewoos -->")
d=Dog("German sheeperd")
c=Cat("Tommy")
d.speak()
c.speak()
c.behaviour()
d.behaviour()
