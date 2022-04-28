import network
import pygame
from player_data import PlayerData
import random



pygame.init()
width, height = 800, 600

class Server:
    CLIENT_TIMOUT = 5
    
    def __init__(self, host: str, port: int):
        self.address = self.host, self.port = host, port
        self.network = network.UdpServer(self.address)
        
        self.players: dict[str, PlayerData] = dict()
        
        
    def get_id(self, data: bytes):
        return data.split(b":", 1)[0].decode()
        
        
    def accept_connection(self, addr: network.address):
        print(addr, " connected")
        
        id = random.randbytes(16).hex()
        while id in self.players.keys():
            id = random.randbytes(16).hex()
        
        self.network.send(addr, id.encode())
        self.players[id] = PlayerData(id, addr)
        
    
    def delete_connection(self, id: str):
        print(self.players[id].addr, " disconnected")
        del self.players[id]
        
    
    def reset_timer(self, id: str):
        self.players[id].last_ping = 0
        

    def check_timeout(self, delta: float):
        to_delete: list[str] = []
        for id, player in self.players.items():
            self.players[id].last_ping += delta
            
            if player.last_ping > Server.CLIENT_TIMOUT:
                to_delete.append(id)
        
        for id in to_delete:
            self.delete_connection(id)

    
    def handle_player(self, data: bytes):
        id, up, down, left, right = data.split(b":")
        self.players[id.decode()].move(int(right) - int(left), int(down) - int(up))
    

    def update_players(self, delta: float):
        pos_data = bytearray()
        for player in self.players.values():
            player.update(delta)
            player.check_bounds(width, height)
            
            pos_data.extend(player.get_data() + b";")
            
        for player in self.players.values():
            self.network.send(player.addr, pos_data)
            

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            delta = clock.tick(60)/1000
            
            while self.network.data_available():
                data, client_addr = self.network.recv(1024)
                
                if data == b"connecting":
                    self.accept_connection(client_addr)
                    break
                
                id = self.get_id(data)
                if data.endswith(b"disconnecting"):
                    self.delete_connection(id)
                    break
                
                self.handle_player(data)
                self.reset_timer(id)
                
            self.check_timeout(delta)
            self.update_players(delta)
                          
            
                
                
            
if __name__ == "__main__":
    server = Server("127.0.0.1", 3000)
    server.run()