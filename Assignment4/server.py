import datetime
import logging

import asyncio
import RPi.GPIO as GPIO
import aiocoap.resource as resource
import aiocoap
import pickle
from mcpi.minecraft import Minecraft

mc = Minecraft.create()


class BlockResource(resource.Resource):
    """
    Example resource which supports GET and PUT methods. It sends large
    responses, which trigger blockwise transfer.
    """

    def __init__(self):
        super(BlockResource, self).__init__()
        self.content = ("This is the resource's default content. It is padded "\
                "with numbers to be large enough to trigger blockwise "\
                "transfer.\n" + "0123456789\n" * 100).encode("ascii")

    async def render_get(self, request):
        #return aiocoap.Message(payload=self.content)
        global token
        x, y, z = mc.player.getPos()
        send_data = (x, y, z, token)
        send_pickle = pickle.dumps(send_data)
        return aiocoap.Message(payload=send_pickle)
        

    async def render_put(self, request):
        global counter
        global token
        token += 1
        counter += 1
        if token > 3:
           token = 1
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        data_back = pickle.loads(request.payload)
        token_new = data_back[0]
        x = data_back[1]
        y = data_back[2]
        z = data_back[3]
        block_type = data_back[4]
        print(counter)
        print(x, y, z, block_type)
        if counter < 10:
            mc.setBlock(x, y, z, block_type)
            mc.player.setPos(x - 1, y, z + 1)
        elif counter == 10:
            mc.setBlock(x, y, z, block_type)
            mc.player.setPos(x - 1, y, z)
        elif counter < 21:
            mc.setBlock(x, y + 1, z, block_type)
            mc.player.setPos(x - 1, y, z - 1)
        elif counter == 21:
            token = 4
            mc.postToChat("Finished Building Wall!")
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
        return aiocoap.Message(payload=payload)
        print("ERROR: parameters -b and -k need to be set")
        sys.exit()

# calculates the thresholds and enables the GPIO pins to light up LED
def LEDLight(user_token):
    #turn off all LEDs
    GPIO.output(24,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
    if user_token == 3:
        #turn on green
        print('LED is green\n')
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
    elif user_token == 2:
        #turn on blue
        print('LED is yellow\n')
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(18,GPIO.HIGH)
    elif user_token == 1:
        #turn on red
        print('LED is red\n')
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
    else:
        #turn on yellow = green + red
        print('LED is yellow\n')
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)  
        
def init_LED():
    print("Setting up GPIO pins for the LED")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)
    GPIO.output(24,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
    
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    init_LED()
    global token
    token = 1
    global counter
    counter = 0
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('other', 'block'), BlockResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
