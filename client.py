#!/usr/bin/python

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from typing import Sequence
import sys
import network, pygame
from player import Player

pygame.init()

server_address = host, port = "127.0.0.1", 3000
size = width, height = 800, 600

class Client:
    def __init__(self, width, height):
        self.network = network.UdpClient()
        self.entities: dict[bytes, Player] = dict()
        self.id = b""
        
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size)
        
        self.input_buffer_size = 15
        self.input_buffer: list[Sequence[bool]] = [pygame.key.get_pressed()]*self.input_buffer_size
        self.packet_number = -1


    def connect(self):
        self.network.send(server_address, b"connecting")
        id, addr = b"", ("", 0)
        while addr[0] != server_address[0]:
            id, addr = self.network.recv(1024)
        
        self.id = id
        self.entities[self.id] = Player(self.id)


    def get_input(self):
        keys = pygame.key.get_pressed()

        input_data = bytearray()
        input_data.extend(str(self.packet_number).encode() + b";" + self.id)
        if keys[pygame.K_UP]:
            input_data.extend(b":1")
            self.entities[self.id].move(0, -1)
        else:
            input_data.extend(b":0")
            
        if keys[pygame.K_DOWN]:
            input_data.extend(b":1")
            self.entities[self.id].move(0, 1)
        else:
            input_data.extend(b":0")
            
        if keys[pygame.K_LEFT]:
            input_data.extend(b":1")
            self.entities[self.id].move(-1, 0)
        else:
            input_data.extend(b":0")
            
        if keys[pygame.K_RIGHT]:
            input_data.extend(b":1")
            self.entities[self.id].move(1, 0)
        else:
            input_data.extend(b":0")
        
        self.input_buffer[self.packet_number % self.input_buffer_size] = keys
        self.packet_number += 1

        return input_data


    def accumulate_past_moves(self, packet_number: int):
        x, y = 0, 0
        for i in range(self.packet_number - packet_number - 1):
            keys = self.input_buffer[(packet_number + i + 1) % self.input_buffer_size]
            if keys[pygame.K_UP]: y -= 1
            if keys[pygame.K_DOWN]: y += 1
            if keys[pygame.K_LEFT]: x -= 1
            if keys[pygame.K_RIGHT]: x += 1
            
        return x, y
            

    def reconcile(self, packet_number: int, x: int, y: int):
        self.entities[self.id].set_pos(x, y)
        move_x, move_y = self.accumulate_past_moves(packet_number)
        self.entities[self.id].move(move_x, move_y)
                

    def update_entities(self, entities_data: bytes):
        packet, *entity_data = entities_data.split(b";")
        for data in entity_data:
            if data == b"": continue

            id, x_bytes, y_bytes = data.split(b":")
            x, y = int(x_bytes), int(y_bytes)
            if id == self.id:
                self.reconcile(int(packet), x, y)
            else:
                if id in self.entities:
                    self.entities[id].set_pos(x, y)
                else:
                    self.entities[id] = Player(id)
                    self.entities[id].set_pos(x, y)


    def draw_entities(self, screen: pygame.surface.Surface):
        for entity in self.entities.values():
            entity.draw(screen)
        

    def run(self):
        self.connect()

        clock = pygame.time.Clock()

        running = True
        while running:
            delta = clock.tick(60)/1000
            self.screen.fill(pygame.Color(0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.send(server_address, self.id + b":disconnecting")
                    running = False
                    sys.exit()
                
            while self.network.data_available():
                entities_data, _ = self.network.recv(1024)
                self.update_entities(entities_data)

            input_data = self.get_input()
            self.network.send(server_address, input_data)
            self.entities[self.id].update(delta)
            self.entities[self.id].check_bounds(width, height)
            self.draw_entities(self.screen)
            
            pygame.display.flip()
        


if __name__ == "__main__":
    client = Client(800, 600)
    client.run()