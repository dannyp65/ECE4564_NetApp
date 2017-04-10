import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

import pickle


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
        x = 15
        y = 25
        z = -69.3
        token = 1
        send_data = (x, y, z, token)
        send_pickle = pickle.dumps(send_data)
        return aiocoap.Message(payload=send_pickle)
        

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = ("I've accepted the new payload. You may inspect it here in "\
                "Python's repr format:\n\n%r"%self.content).encode('utf8')
        return aiocoap.Message(payload=payload)

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('other', 'block'), BlockResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
