# MultiplayerServer

Simple UDP socket server implementation used in a simple mutliplayer pygame demo with 2 threads.
The server is set up as a multithreaded authoritative server.

## Authoritative server

The server being authoritative means that all actions are calculated on the server side. This means that the server receives each players
inputs and will then update the games state accordingly. Next the server will broadcast this updated gamestate to each client, allowing
for the clients to render it out.

**TODO** client side prediction and reconciliation
