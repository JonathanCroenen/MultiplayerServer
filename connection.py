import network

class Connection:
    def __init__(self, addr: network.address):
        self.addr = addr
        self.last_ping = 0.0
        self.entities: set[bytes] = set()
        
        self.packet_number = -1
        
        
    def ping(self):
        self.last_ping = 0.0
        
        
    def has_timeout(self, delta: float, timeout: float):
        self.last_ping += delta
        
        if self.last_ping > timeout:
            return True
        return False
    
    
    def add_entity(self, id: bytes):
        self.entities.add(id)
        
        
    def get_entities(self):
        return self.entities
    
    
    def get_address(self):
        return self.addr
    
    
    def set_packet_number(self, number: int):
        self.packet_number = number
    
    
    def get_packet_number(self):
        return self.packet_number
    
    
    def get_last_ping(self):
        return self.last_ping