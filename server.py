#!/usr/bin/python

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import network
import pygame
from player import Player
from connection import Connection
import random
import signal


pygame.init()
width, height = 800, 600

class Server:
    CLIENT_TIMOUT = 5
    
    def __init__(self, host: str, port: int):
        self.running = False
        
        self.address = self.host, self.port = host, port
        self.network = network.UdpServer(self.address)
                
        self.entities: dict[bytes, Player] = dict()
        self.connections: dict[network.address, Connection] = dict()
        
        
    def get_id(self, data: bytes):
        return data.split(b":", 1)[0].decode()
        
        
    def accept_connection(self, addr: network.address):
        print(addr, " connected")
        
        id = random.randbytes(8).hex().encode()
        while id in self.entities.keys():
            id = random.randbytes(8).hex().encode()
        
        self.network.send(addr, id)
        
        self.connections[addr] = Connection(addr)
        self.entities[id] = Player(id)
        self.connections[addr].add_entity(id)
        
    
    def delete_connection(self, addr: network.address):
        print(addr, " disconnected")
        for id in self.connections[addr].get_entities():
            del self.entities[id]
            
        del self.connections[addr]
        
    
    def ping(self, addr: network.address):
        self.connections[addr].ping()
        

    def check_timeout(self, delta: float):
        to_delete: list[network.address] = []
        for connection in self.connections.values():
            if connection.has_timeout(delta, Server.CLIENT_TIMOUT):
                to_delete.append(connection.get_address())
        
        for addr in to_delete:
            self.delete_connection(addr)

    
    def handle_player(self, addr: network.address, data: bytes):
        packet, rest = data.split(b";")
        id, up, down, left, right = rest.split(b":")
        # if self.connections[addr].get_packet_number() + 1 != int(packet):
        #     print("Packet lost")
        self.connections[addr].set_packet_number(int(packet))
        self.entities[id].move(int(right) - int(left), int(down) - int(up))
    

    def update_entities(self, delta: float):
        pos_data = bytearray()
        for connection in self.connections.values():
            for id in connection.get_entities():
                self.entities[id].update(delta)
                self.entities[id].check_bounds(width, height)
                
                pos_data.extend(self.entities[id].get_data() + b";")
        
        for connection in self.connections.values():
            data = str(connection.get_packet_number()).encode() + b";" + pos_data
            self.network.send(connection.get_address(), data)
            

    def run(self):
        clock = pygame.time.Clock()
        self.network.start_thread()
        
        counter = 0
        self.running = True
        while self.running:
            delta = clock.tick(20)/1000
            
            while self.network.has_data():
                data, client_addr = self.network.get_data()
                if data == b"connecting":
                    self.accept_connection(client_addr)
                    break
                if data.endswith(b"disconnecting"):
                    self.delete_connection(client_addr)
                    break
                
                self.handle_player(client_addr, data)
                self.ping(client_addr)
            
            self.check_timeout(delta)
            self.update_entities(delta)
                
            
            counter += 1
            if counter % 60 == 0:
                print(f'Tickrate: {int(1/delta):02} tps')
            

        
    def stop(self):
        self.running = False
        print('Shutting down.')
                          
            
                
                
            
if __name__ == "__main__":
    server = Server("127.0.0.1", 3000)
    signal.signal(signal.SIGINT, lambda _1, _2: server.stop())
    
    server.run()