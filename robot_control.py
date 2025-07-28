import socket
from config import ROBOT_IP, ROBOT_PORT
ROBOT_IP = "192.168.0.2"  # Reemplaza con la IP real del UR5
ROBOT_PORT = 30002  
import math
current_pos = []
import time

def estimate_movel_time(target_pos, velocity, acceleration):
    global current_pos
    if current_pos==[]:
        current_pos = target_pos
    dist_x = target_pos[0] - current_pos[0]
    dist_y = target_pos[1] - current_pos[1]
    dist_z = target_pos[2] - current_pos[2]
    distance = math.sqrt(dist_x**2 + dist_y**2 + dist_z**2)

    # Si la distancia es cero, el tiempo es cero.
    if distance < 1e-6: # Usar una pequeña tolerancia para flotantes
        return 0.0

    # 2. Calcular el tiempo de aceleración/desaceleración y la distancia recorrida en esas fases
    # t_accel = v / a
    # d_accel = 0.5 * a * t_accel^2 = 0.5 * a * (v/a)^2 = 0.5 * v^2 / a
    time_to_reach_max_vel = velocity / acceleration
    distance_during_accel = 0.5 * acceleration * time_to_reach_max_vel**2
    
    time_at_max_speed = (distance - (2 * distance_during_accel)) / velocity
    print(2 * math.sqrt(distance / acceleration), (2 * time_to_reach_max_vel) + time_at_max_speed)
    # El robot necesita acelerar y luego desacelerar, por lo tanto, 2 * distance_during_accel
    if distance <= 2 * distance_during_accel:
        # El movimiento es tan corto que el robot nunca alcanza la velocidad máxima.
        # Recorre toda la distancia acelerando y luego desacelerando.
        # Distancia = 0.5 * a * (t/2)^2 * 2 (ida y vuelta) = a * (t/2)^2
        # t/2 = sqrt(distancia / a)
        # t = 2 * sqrt(distancia / a)
        estimated_time = 2 * math.sqrt(distance / acceleration)
        
    else:
        # El robot acelera, mantiene la velocidad máxima, y luego desacelera.
        time_at_max_speed = (distance - (2 * distance_during_accel)) / velocity
        estimated_time = (2 * time_to_reach_max_vel) + time_at_max_speed

    # Añadir un pequeño colchón/margen de seguridad (ej. 10-20%)
    # Esto compensa imprecisiones, sobrecargas, cambios de orientación, etc.
    safety_margin = 1.2 #1.2 # Añadir un 20%
    return estimated_time * safety_margin + 1

def send_urscript(script):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, ROBOT_PORT))
    s.send(script.encode('utf-8'))
    s.close()

def _move(position, typ, velocity=0.15, acceleration=1.2):
    ##global current_pos
    x, y, z, rx, ry, rz = position
    ##current_pos = position
    script = f'move{typ}(p[{x},{y},{z},{rx},{ry},{rz}], a={acceleration}, v={velocity})\n'
    send_urscript(script)

def move_j(position):
    return _move(position, 'j', 0.6)

def move_l(position):
    velocity = 0.30
    acceleration = 1.2
    _move(position, 'l', velocity, acceleration)
    
def move_p(position):
    _move(position, 'p')