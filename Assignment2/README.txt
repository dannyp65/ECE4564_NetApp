Assigment 2 - Little Brother
Team 16 - Team JANK

Interperter: Python 3.6 and above

Initialize process:
  To begin, the message broker Raspberry Pi will be turn on in order for the hosts and monitor to connect.  
  RabbitMQ Message Broker Raspberry Pi:
    1. Install RabbitMQ 
    2. Open command prompt and type 'hostname -I' to obtain the Message Broker's IP address
    
  After message broker initialization, hosts and monitor will initialize their respective programs.  
           
  Host Raspberry Pi:
   1. install all extra libraries on Pi
   2. using this command to run the host RPi:
      python3 pistatsd –b message broker [–p virtual host] [–c login:password] –k routing key
      
      using the message broker ip address
      virtual host: rabbit_hole 
      login: rabbit
      password: jank
      rounting key: host1 or host2
      example: if the message broker ip address is 192.23.32.2 example command line will be follow:
      python3 pistatsd –b 192.23.32.2 -p rabbit_hole –c rabbit:jank –k host1
   
  Monitor Raspberry Pi:
  1. install all extra libraries on Pi.
  2.  using this command to run the monitor RPi:
      python3 pistatsview –b message broker [–p virtual host] [–c login:password] –k routing key
      
      using the message broker ip address
      virtual host: rabbit_hole 
      login: rabbit
      password: jank
      rounting key: host1 or host2
      example: if the message broker ip address is 192.23.32.2 example command line will be follow:
      python3 pistatsview –b 192.23.32.2 -p rabbit_hole –c rabbit:jank –k host1
    
Extra Libraries:
  - json
  - pika
  - time
  - sys
  - pymongo
  - MongoClient
