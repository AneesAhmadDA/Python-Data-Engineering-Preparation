class counter:
    def __init__(self,max):
        self.max=max
        self.current=0
    def __iter__(self):
        return self
    def __next__(self):
        if self.current<self.max:
            self.current+=1
            return self.current
        else:
            raise StopIteration

c=counter(5)
for num in c :
    print(num)        

##this is the generator function part
def gen(n1,n2):
    for i in range(n1,n2+1):
        yield i

value=gen(10,20)
print(next(value))
print(next(value))
print(next(value))
print(next(value))
print(next(value))
print(next(value))
print(next(value))
print(next(value))

