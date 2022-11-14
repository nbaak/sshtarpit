


class Country:
    
    def __init__(self, code):
        self.code = code
        self.frequency = 1
        
        
    def count(self):
        self.frequency += 1
    
    def __str__(self):
        return f"{self.code}"
        
    def __lt__(self, other):
        return self.frequency < other.frequency