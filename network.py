import socket, select

address = tuple[str, int]

class UdpServer:
    def __init__(self, addr: address):
        self.address = addr
        self.host, self.port = addr
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.address)
        
        
    def send(self, addr: address, data: bytes):
        self.sock.sendto(data, addr)
        
        
    def recv(self, buffer_size: int):
        return self.sock.recvfrom(buffer_size)
    
    
    def data_available(self):
        return len(select.select([self.sock], [], [], 0)[0]) > 0
        
    
    

class UdpClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        
    def send(self, addr: address, data: bytes):
        self.sock.sendto(data, addr)
        
        
    def recv(self, buffer_size: int):
        return self.sock.recvfrom(buffer_size)
    
    
    def data_available(self):
        return len(select.select([self.sock], [], [])[0]) > 0