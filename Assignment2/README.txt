Assigment 2 - Little Brother
Group 16 - Team JANK

Interperter: Python 3.6 and above

Initialize process:
  To begin, the message broker Raspberry Pi will turn on in order for the hosts and monitor to connect.  
  RabbitMQ Message Broker Raspberry Pi:
    1. Install RabbitMQ 
    2. Open command prompt and type 'hostname -I' to obtain the Message Broker's IP address
    
  After message broker initialization, hosts and monitor will initialize their respective programs.  
           
  Host Raspberry Pi:
   1. Install all extra libraries on Pi
   2. Using this command to run the host RPi:
      python3 pistatsd.py –b message broker [–p virtual host] [–c login:password] –k routingkey
      
      using the message broker IP address
      virtual host: rabbit_hole 
      login: rabbit
      password: jank
      rountingkey: Host_1 or Host_2
      example: if the message broker ip address is 192.23.32.2 example command line will be follow:
      python3 pistatsd.py –b 192.23.32.2 -p rabbit_hole –c rabbit:jank –k Host_1
   
  Monitor Raspberry Pi:
  1.  Install all extra libraries on Pi.
  2.  Set up GPIO ribbon to connect from the Raspberry Pi to the bread board.  Set up pin 24 to illuminate 
      green LED.  Set up pin 23 to illuminate red LED.  Set up pin 18 to illuminate the blue LED.  Connect a
      330 Ohm resistor to each color input of the LED on the bread board.  Connect the longest pin of the LED 
      to a ground pin on the GPIO of the Raspberry Pi.  
  3.  Using this command to run the monitor RPi:
      python3 pistatsview.py –b message broker [–p virtual host] [–c login:password] –k routingkey
      
      using the message broker ip address
      virtual host: rabbit_hole 
      login: rabbit
      password: jank
      rountingkey: Host_1 or Host_2
      example: if the message broker ip address is 192.23.32.2 example command line will be follow:
      python3 pistatsview.py –b 192.23.32.2 -p rabbit_hole –c rabbit:jank –k Host_1
    
Extra Libraries:
  - json
  - pika
  - time
  - sys
  - pymongo
  - MongoClient
  - GPIO
