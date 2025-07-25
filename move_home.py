from robot_control import *
from config import *
import time
#move_j(home_position)
def mover_a_celda(i, j):
    pose = celda_a_posicion.get((i, j))
    if pose:
        move_j(pose)
        time.sleep(3)
        #open_gripper()
        time.sleep(2)
        move_j(home_position)
        time.sleep(2)
    else:
        print(f"No hay posición definida para la celda ({i},{j})")



mover_a_celda(0, 0)
time.sleep(2)
mover_a_celda(0, 1)
mover_a_celda(0, 2)
mover_a_celda(1, 1)