import socket
from config import ROBOT_IP, ROBOT_PORT
ROBOT_IP = "192.168.0.2"  # Reemplaza con la IP real del UR5
ROBOT_PORT = 30002  

def send_urscript(script):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, ROBOT_PORT))
    s.send(script.encode('utf-8'))
    s.close()

def _move(position, typ, velocity=0.15):
    x, y, z, rx, ry, rz = position
    script = f'move{typ}(p[{x},{y},{z},{rx},{ry},{rz}], a=1.2, v={velocity})\n'
    send_urscript(script)

def move_j(position):
    return _move(position, 'j', 0.4)

def move_l(position):
    velocity = 0.15
    x, y, z, rx, ry, rz = position
    distance = (x**2 + y**2 + z**2) ** 0.5
    estimated_time = distance / velocity
    _move(position, 'l', velocity)
    time.sleep(estimated_time * 1.1)

def move_p(position):
    _move(position, 'p')