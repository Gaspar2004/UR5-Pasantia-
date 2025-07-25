import socket
from config import ROBOT_IP, ROBOT_PORT
ROBOT_IP = "192.168.0.2"  # Reemplaza con la IP real del UR5
ROBOT_PORT = 30002  

def send_urscript(script):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, ROBOT_PORT))
    s.send(script.encode('utf-8'))
    s.close()

def _move(position, typ):
    x, y, z, rx, ry, rz = position
    script = f'move{typ}(p[{x},{y},{z},{rx},{ry},{rz}], a=1.2, v=0.15)\n'
    send_urscript(script)

def move_j(position):
    return _move(position, 'j')

def move_l(position):
    return _move(position, 'l')

def move_p(position):
    return _move(position, 'p')

def move_to_position(position):
    return move_l(position)
    """x, y, z, rx, ry, rz = position
    script = f'movel(p[{x},{y},{z},{rx},{ry},{rz}], a=1.2, v=0.15)\n'
    send_urscript(script)"""


