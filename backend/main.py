import asyncio, websockets

async def conn(websocket, path):
    active = []
    async for msg in websocket:
        vals = msg.split(",")
        for i in set().union(active, vals):
            if i in active and i not in vals:
                print("Deactivating", i)
            elif i not in active and i in vals:
                print("Activating", i)
        active = vals

srv = websockets.serve(conn, "localhost", 11337)
print("Starting server...")

asyncio.get_event_loop().run_until_complete(srv)
asyncio.get_event_loop().run_forever()