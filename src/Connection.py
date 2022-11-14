
class Connection:
    
    def __init__(self, ip):
        self.ip = ip
        self.status = 'accepted' # or closed
        self.time_start = None
        self.time_close = None
        self.time_delta = None
        self.location = None
        
    def accept(self):
        self.status = 'accepted'
        
    def close(self):
        self.status = 'closed'
        
    def __str__(self):
        return self.ip
    
    def __reps__(self):
        return self.ip
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.ip == other.ip
            
    def __hash__(self):
        return hash(self.ip)  
    
if __name__ == "__main__":
    pass
    
    
    
    
    
    
    
    
        