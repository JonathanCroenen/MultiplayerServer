#!/usr/bin/python

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import network, pygame
from player import Player

pygame.init()

server_address = host, port = "127.0.0.1", 3000
size = width, height = 800, 600

screen = pygame.display.set_mode(size)


def connect(client: network.UdpClient):
    client.send(server_address, b"connecting")
    return client.recv(1024)[0]


def get_input(id: bytes):
    input_data = bytearray(id)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        input_data.extend(b":1")
    else:
        input_data.extend(b":0")
        
    if keys[pygame.K_DOWN]:
        input_data.extend(b":1")
    else:
        input_data.extend(b":0")
        
    if keys[pygame.K_LEFT]:
        input_data.extend(b":1")
    else:
        input_data.extend(b":0")
        
    if keys[pygame.K_RIGHT]:
        input_data.extend(b":1")
    else:
        input_data.extend(b":0")

    return input_data


def update_players(player_data: bytes, players: dict[bytes, Player], screen: pygame.surface.Surface):
    data = player_data.split(b";")
    for item in data:
        if item == b"": continue
        id, x, y = b"", 0, 0
        try:
            id, x, y = item.split(b":")
        except:
            print(item)
        if id in players:
            players[id].set_pos(int(x), int(y))
        else:
            players[id] = Player(id.decode())
            players[id].set_pos(int(x), int(y))
            
        players[id].draw(screen)


def run():
    client = network.UdpClient()
    id = connect(client)
    
    players: dict[bytes, Player] = dict()
    players[id] = Player(id.decode())
    
    clock = pygame.time.Clock()

    running = True
    while running:
        delta = clock.tick(60)/1000
        screen.fill(pygame.Color(0, 0, 0))
        
        input_data = get_input(id)
        client.send(server_address, input_data)
        
        player_data, _ = client.recv(1024)
        update_players(player_data, players, screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.send(server_address, id + b":disconnecting")
                running = False
                break
            
        pygame.display.flip()
        


run()