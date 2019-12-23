import asyncio, websockets, sys, json, argparse, collections#, gpiozero
from datetime import datetime, timedelta
#from adafruit_motorkit import MotorKit


parser = argparse.ArgumentParser()
parser.add_argument("--password", "-p", type=str, default="")
parser.add_argument("--port", "-P", type=int, default=11337)
args = parser.parse_args()
PASSWORD = args.password
try:
    kit = MotorKit()
except:
    class MotorKit():
        def __init__(self):
            Motor = collections.namedtuple('Motor', 'throttle')
            self.motor1 = Motor(throttle=0)
            self.motor2 = Motor(throttle=0)
            self.motor3 = Motor(throttle=0)
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

def set_individual(motor, speed):
    getattr(kit, f'motor{motor}').throttle = speed

ACTIONS = {'xcw': lambda s: x(s),
           'xccw': lambda s: x(-s),
           'ycw': lambda s: y(s),
           'yccw': lambda s: y(-s),
           'zf': lambda s: set_all(s),
           'zb': lambda s: set_all(-s),
           'm1': lambda s: set_individual(1, s),
           'm2': lambda s: set_individual(2, s),
           'm3': lambda s: set_individual(3, s)}

#for i in [1, 2, 3]: ACTIONS[f'm{i}'] = lambda s: getattr(kit, f'motor{i}') = s

class DummyBtn:
    def __init__(self, i):
        self.is_pressed = False

pins = [DummyBtn(i) for i in [1, 2, 3, 4, 5, 6]] # TODO: Replace the [1, 2, 3, 4, 5, 6]


# Message Codes: o - okay; b - bad password; e - error; a - perform action

async def conn(websocket, path):
    active = []
    auth = PASSWORD == ''
    async for msg in websocket:
        if not auth:
            if msg == 'p' + PASSWORD:
                auth = True
            else:
                print("Unauthorized")
                await websocket.send("b")
        elif msg.startswith('a'):
            limit_triggered = False
            data = json.loads(msg[1:])
            ACTIONS[data['action']](data['speed'])
            if data['duration'] > 0:
                end = datetime.now() + timedelta(seconds=data['duration'])
                while datetime.now() < end:
                    for i in pins:
                        if i.is_pressed:
                            limit_triggered = True
                            break
                    if limit_triggered: break
                set_all(0)
            await websocket.send('o' if limit_triggered else 'e')

srv = websockets.serve(conn, "localhost", args.port)
print(f"Starting server with arguments {args}...")

asyncio.get_event_loop().run_until_complete(srv)
asyncio.get_event_loop().run_forever()