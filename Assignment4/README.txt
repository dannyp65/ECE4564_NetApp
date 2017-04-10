Assigment 4 - Cooperative Multiplayer Minecraft
Team 16 - Team JANK

Interperter: Python 3.5.2 

Initialize process:
  In order to play the game, the players have to obtaint the Server's IP address. The server must be running when the player'code is executed.
    
  Server Raspberry Pi:
    1. Open command prompt and type 'hostname -I' to obtain the Server's IP address 
    2. Make sure that all the extra libraries were installed on your Rapsberry Pi (see Extra Libraries)
    3. Run server.py using python 3 (Ex: python3 server.py)
    
  Player Raspberry Pi:
    1. Make sure that all the extra libraries were installed on your Rapsberry Pi (see Extra Libraries)
    2. Run clientGET#.py "#server_host_addr" using python 3 with # is your player token number and server's IP address.
          Ex: python3 clientGET1.py "187.28.31.1"
    
    
Extra Libraries:
  - socket
  - pickle
  - asyncio
  - aiocoap
  - logging 
  - mcpi.minecraft
  - RPi.GPIO
