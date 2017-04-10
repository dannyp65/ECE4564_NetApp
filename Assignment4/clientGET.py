import logging
import asyncio
import pickle

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://localhost/other/block')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        receive_data = pickle.loads(response.payload)
        x = receive_data[0]
        y = receive_data[1]
        z = receive_data[2]
        token = receive_data[3]
        print('Result: %s\n%r %r %r %r'%(response.code, x, y, z, token))

#Making code for player A
#sends block type 1
    if token == 1:
        context = await Context.create_client_context()
        await asyncio.sleep(2)

        payload = (token, x + 1, y, z, 1)
        send_data = pickle.dumps(payload)
        request = Message(code=PUT, payload=send_data)
        request.opt.uri_host = '127.0.0.1'
        request.opt.uri_path = ("other", "block")

        response = await context.request(request).response
        print('Result: %s\n%r'%(response.code, response.payload))

        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
