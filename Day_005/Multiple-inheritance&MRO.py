class Father:
    def __init__(self,name):
        self.name=name
    def Father_skill(self):
        print(f"{self.name} is an expert in Driving (Father character)")
class Mother:
    def __init__(self,name):
        self.name=name
    def Mother_skill(self):
        print(f"{self.name} is an expert in Cooking (Mother character)")
class Child(Father,Mother):
    def __init__(self, name):
        super().__init__(name)
    def child_skill(self):
        print(f"{self.name} is an expert in Coding (Child charater)")
##creating an instance
Child1=Child("Anees")
Child1.child_skill()
Child1.Father_skill()
Child1.Mother_skill()
