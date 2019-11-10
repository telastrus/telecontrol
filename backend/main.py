import asyncio, websockets, sys

PASSWORD = sys.argv[-1]

async def conn(websocket, path):
    active = []
    auth = False
    async for msg in websocket:
        print(msg)
        if not auth and msg != 'p' + PASSWORD:
            await websocket.send("b")
            continue

srv = websockets.serve(conn, "localhost", 11337)
print(f"Starting server with password {PASSWORD}...")

asyncio.get_event_loop().run_until_complete(srv)
asyncio.get_event_loop().run_forever()