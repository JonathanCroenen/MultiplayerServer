import network

class Connection:
    def __init__(self, addr: network.address):
        self.addr = addr
        self.last_ping = 0.0
        self.entities = set()
        
    def ping(self):
        self.last_ping = 0.0
        
    def has_timeout(self, delta: float, timeout: float):
        self.last_ping += delta
        
        if self.last_ping > timeout:
            return True
        return False
    
    def add_entity(self, id: str):
        self.entities.add(id)
        
    def get_entities(self):
        return self.entities