import asyncio, websockets, sys, json
from adafruit_motorkit import MotorKit

PASSWORD = sys.argv[-1]

kit = MotorKit()
top = kit.motor1
left = kit.motor2
right = kit.motor3

def x(speed):
    top.throttle = speed
    left.throttle = -speed
    right.throttle = -speed

def y(speed):
    top.throttle = 0
    left.throttle = speed
    right.throttle = -speed

def set_all(speed):
    for i in (top, left, right): i.throttle = speed

ACTIONS = {'xcw': lambda s: x(s),
           'xccw': lambda s: x(-s),
           'ycw': lambda s: y(s),
           'yccw': lambda s: y(-s),
           'zf': lambda s: set_all(s),
           'zb': lambda s: set_all(-s)}

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
            ACTIONS[data['action']](data['speed'])
            await asyncio.sleep(data['duration'])
            set_all(0)
            await websocket.send('o')

srv = websockets.serve(conn, "localhost", 11337)
print(f"Starting server with password {PASSWORD}...")

asyncio.get_event_loop().run_until_complete(srv)
asyncio.get_event_loop().run_forever()