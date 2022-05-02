# MultiplayerServer

Simple UDP socket server implementation used in a simple mutliplayer pygame demo with 2 threads.
The server is set up as a multithreaded authoritative server.

## Authoritative server

The server being authoritative means that all actions are calculated on the server side. This means that the server receives each players
inputs and will then update the games state accordingly. Next the server will broadcast this updated gamestate to each client, allowing
for the clients to render it out.

The client buffers its inputs and will keep them until the server acknowledges each move. Upon acknowledgement of a move the client will 
replay the moves from the position the server has calculated. This allows the client to move its player freely and more smoothly and update 
the player to the servers authoritative position upon each acknoledgement. Therefore network delay is 'seemingly' removed on the clientside.

**TODO** client side interpolation
