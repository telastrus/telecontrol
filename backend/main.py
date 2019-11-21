import asyncio, websockets, sys, json

PASSWORD = sys.argv[-1]

def set_speed(speed):
    print("Setting speed to", speed)

def stop_all():
    pass

async def conn(websocket, path):
    active = []
    auth = False
    async for msg in websocket:
        if not auth:
            if msg == 'p' + PASSWORD:
                auth = True
            else:
                print("Unauthorized")
                await websocket.send("b")
        elif msg.startswith('a'):
            data = json.loads(msg[1:])
            set_speed(data['speed'])
            await asyncio.sleep(data['duration'])
            stop_all()
            await websocket.send('o')

srv = websockets.serve(conn, "localhost", 11337)
print(f"Starting server with password {PASSWORD}...")

asyncio.get_event_loop().run_until_complete(srv)
asyncio.get_event_loop().run_forever()