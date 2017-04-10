import logging
import asyncio
import pickle
import sys

from aiocoap import *

def get_args():
    total = len(sys.argv)
    if total != 2:
        print("ERROR: Incorrect number of arguments")
        sys.exit()
    else:
        return sys.argv[1]

logging.basicConfig(level=logging.INFO)

async def main():
    ip = get_args()
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://' + ip + '/other/block')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        global token
        receive_data = pickle.loads(response.payload)
        x = receive_data[0]
        y = receive_data[1]
        z = receive_data[2]
        token = receive_data[3]
        print('Result: %s\n%r %r %r %r'%(response.code, x, y, z, token))

#Making code for player A
#sends block type 1
    if token == 2:
        context = await Context.create_client_context()
        await asyncio.sleep(2)

        payload = (token, x + 1, y, z, 49)
        send_data = pickle.dumps(payload)
        request = Message(code=PUT, payload=send_data)
        request.opt.uri_host = ip
        request.opt.uri_path = ("other", "block")

        response = await context.request(request).response
        #print('Result: %s\n%r'%(response.code, response.payload))

    if token == 4:
        print("Wall is complete")
        sys.exit()
        
if __name__ == "__main__":
    while 1:
        asyncio.get_event_loop().run_until_complete(main())
