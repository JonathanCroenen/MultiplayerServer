import socket, select, queue
import threading


address = tuple[str, int]

class UdpServer:
    def __init__(self, addr: address):
        self.address = addr
        self.host, self.port = addr
        
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_sock.settimeout(1)
        self.recv_sock.bind(self.address)
        
        self.queue: queue.Queue[tuple[bytes, address]] = queue.Queue()
        
        
    def send(self, addr: address, data: bytes):
        self.send_sock.sendto(data, addr)
        
        
    def thread_method(self):
        while True:
            try:
                item = self.recv_sock.recvfrom(1024)
                self.queue.put_nowait(item)
            except TimeoutError:
                pass
                            
                
    def start_thread(self):
        t = threading.Thread(target=self.thread_method, daemon=True)
        t.start()
        
        
    def has_data(self):
        return self.queue.qsize() > 0


    def get_data(self):
        return self.queue.get_nowait()
    
    
    

class UdpClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        
    def send(self, addr: address, data: bytes):
        self.sock.sendto(data, addr)
        
        
    def recv(self, buffer_size: int):
        return self.sock.recvfrom(buffer_size)
    
    
    def data_available(self):
        return len(select.select([self.sock], [], [], 0)[0]) > 0