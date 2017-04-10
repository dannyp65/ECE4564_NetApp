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

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
