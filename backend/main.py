import asyncio, websockets, sys, json, argparse, collections#, gpiozero
from datetime import datetime, timedelta
from enum import Enum
#from adafruit_motorkit import MotorKit
class LimitState(Enum):
    UPPER = 1
    LOWER = 2
    ERROR = 3
    OK = 4
    UNKNOWN = 5

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

class Limit:
    def __init__(self, upper, lower, motor):
        self.__state = LimitState.OK
        self.upper = upper
        self.lower = lower
        self.motor = motor
    
    def update_state(self):
        self.__state = LimitState.UNKNOWN
        if self.upper.is_pressed:
            self.__state = LimitState.UPPER
            self.motor.throttle = 0
            return False
        elif self.lower.is_pressed:
            if self.__state == LimitState.UPPER:
                # Emergency stop everything
                self.__state = LimitState.ERROR
                kit.motor1.throttle = 0
                kit.motor2.throttle = 0
                kit.motor3.throttle = 0
                raise Exception("Both limit switches are activated. This is a problem.")
            else:
                self.__state = LimitState.LOWER
            self.motor.throttle = 0
            return False
        else:
            self.__state = LimitState.OK
            return True
            
    
    def request_movement(self, speed):
        if speed == None:
            self.motor.throttle = 0
            return True
        elif (speed > 0 and self.__state != LimitState.UPPER) or (speed < 0 and self.__state != LimitState.LOWER):
            self.motor.throttle = speed
            return True
        else:
            return False

class DummyBtn:
    def __init__(self, i):
        self.is_pressed = False

pin = lambda i: DummyBtn(i)

# TODO: Replace the dummy pins
TOP = Limit(pin(1), pin(2), kit.motor1)
LEFT = Limit(pin(3), pin(4), kit.motor2)
RIGHT = Limit(pin(5), pin(6), kit.motor3)

def x(speed):
    TOP.request_movement(speed)
    LEFT.request_movement(-speed)
    RIGHT.request_movement(-speed)

def y(speed):
    TOP.request_movement(None)
    LEFT.request_movement(speed)
    RIGHT.request_movement(-speed)

def set_all(speed):
    for i in (TOP, LEFT, RIGHT): i.request_movement(speed)

def set_individual(motor, speed):
    getattr(kit, f'motor{motor}').request_movement(speed)

ACTIONS = {'xcw': lambda s: x(s),
           'xccw': lambda s: x(-s),
           'ycw': lambda s: y(s),
           'yccw': lambda s: y(-s),
           'zf': lambda s: set_all(s),
           'zb': lambda s: set_all(-s),
           'm1': lambda s: set_individual(1, s),
           'm2': lambda s: set_individual(2, s),
           'm3': lambda s: set_individual(3, s)}


# Message Codes: o - okay; b - bad password; e - error; a - perform action
async def conn(websocket, path):
    # active = []
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
            if not ACTIONS[data['action']](data['speed']):
                await websocket.send('Invalid move.')
            if data['duration'] > 0:
                end = datetime.now() + timedelta(seconds=data['duration'])
                while datetime.now() < end:
                    for i in (TOP, LEFT, RIGHT):
                        if not i.update_state():
                            limit_triggered = True
                            break
                    if limit_triggered: break
                set_all(0)
            await websocket.send('OK.' if not limit_triggered else 'Limit triggered.')

srv = websockets.serve(conn, "localhost", args.port)
print(f"Starting server with arguments {args}...")

asyncio.get_event_loop().run_until_complete(srv)
asyncio.get_event_loop().run_forever()