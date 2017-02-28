Assigment 2 - Little Brother
Team 16 - Team JANK

Interperter: Python 3.6 and above

Initialize process:
  To begin, the message broker will be initialized in order for the hosts and monitor to connect.  
    Message broker command line format:
  
  After message broker initialization, hosts and monitor will initialize their respective programs.  
    Host command line format:
    Monitor command line format:
  
     Note: 
           
           
  RabbitMQ Message Broker Raspberry Pi:
    1. Install RabbitMQ 
    2. 
  Host Raspberry Pi:
    1. Open command prompt and type 'hostname -I' to obtain the Server's IP address for your tweet format
    2. Make sure that all the extra libraries were installed on your Rapsberry Pi (see Extra Libraries)
    3. Run server.py using python 3 (Ex: python3 server.py)
  Client Raspberry Pi:
    1. Make sure that all the extra libraries were installed on your Rapsberry Pi (see Extra Libraries)
    2. Run client.py using python 3 (Ex: python3 client.py)
    
  Twitter: Use any twitter account to tweet questions with format above (and the correct servers ip address)
    the answer will be tweeted back with user's twitter account tagged in it.
    
Extra Libraries:
  - json
  - pika
  - time
  - sys
  - pymongo
  - MongoClient
