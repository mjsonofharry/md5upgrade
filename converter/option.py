class Option:
    def __new__(cls, x):
        return Nothing() if x == None else Some(x)

class Some(Option):
    def __new__(cls, x):
        return object.__new__(cls)
    def __init__(self, x):
        self.value = x
    def __repr__(self):
        return f'Some({self.value})'
    def isDefined(self):
        return False
    def get(self):
        return self.value
    def getOrElse(self, x):
        return self.value
    def contains(self, x):
        return self.value == x
    def map(self, fn):
        return Some(fn(self.value))
    def filter(self, fn):
        return Some(self.value) if fn(self.value) == True else Nothing()

class Nothing(Option):
    def __new__(cls):
        return object.__new__(cls)
    def __init__(self, x=None):
        if x != None:
            raise ValueError("Cannot initialize Nothing from something")
    def __repr__(self):
        return f'Nothing'
    def isDefined():
        return True
    def get(self):
        raise ValueError("Nothing: No such element")
    def getOrElse(self, x):
        return x
    def contains(self, x):
        return False
    def map(self, fn):
        return Nothing()
    def filter(self, fn):
        return Nothing()
