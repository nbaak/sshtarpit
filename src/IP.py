


class IP:
    
    def __init__(self, ip):
        self.ip = ip
        self.frequency = 1
        self.country = None
        self.country_code = None
        
        
    def count(self):
        self.frequency += 1
        
    def __str__(self):
        return f"{self.ip}"
        
    def __hash__(self):
        return hash(self.ip)
    
    def __lt__(self, other):
        return  self.frequency < other.frequency